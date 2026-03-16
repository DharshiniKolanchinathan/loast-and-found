import cv2
import numpy as np
import os
from PIL import Image
from django.conf import settings
from .models import LostItem, FoundItem, MatchResult
from notifications.services import create_notification

def calculate_similarity(img1_path, img2_path):
    """
    Calculates similarity between two images using ORB feature matching.
    Handles various formats (AVIF, WebP, etc.) using Pillow.
    """
    try:
        # Load images using Pillow to ensure compatibility with all formats
        with Image.open(img1_path) as im1, Image.open(img2_path) as im2:
            # Convert to grayscale and then to numpy array
            img1 = np.array(im1.convert('L'))
            img2 = np.array(im2.convert('L'))
        
        if img1 is None or img2 is None:
            return 0.0
        
        # Initialize ORB detector
        orb = cv2.ORB_create()
        
        # Find keypoints and descriptors
        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)
        
        if des1 is None or des2 is None:
            return 0.0
        
        # BFMatcher with default params
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        
        # Match descriptors
        matches = bf.match(des1, des2)
        
        # Filter good matches based on distance
        # For ORB, a distance below 50 is generally considered a good match
        good_matches = [m for m in matches if m.distance < 50]
        
        if not good_matches:
            return 0.0
            
        # Calculate score: percentage of good matches relative to total keypoints
        # Using min(len(kp1), len(kp2)) as it's more robust to scale/crop differences
        score = (len(good_matches) / min(len(kp1), len(kp2))) * 100
        
        # If the images are identical, it should be close to 100
        # If they are totally different, it should be very low
        return min(score, 100.0)
    except Exception as e:
        print(f"Error calculating similarity: {e}")
        return 0.0

def find_matches_for_lost_item(lost_item):
    """
    Compares a lost item with all found items and stores top 3 matches.
    """
    found_items = FoundItem.objects.filter(is_active=True)
    results = []
    
    for found_item in found_items:
        score = calculate_similarity(lost_item.image.path, found_item.image.path)
        if score > 10: # Threshold for a potential match
            results.append((found_item, score))
    
    # Sort and take top 3
    results.sort(key=lambda x: x[1], reverse=True)
    top_3 = results[:3]
    
    # Store in MatchResult and Notify
    for found_item, score in top_3:
        MatchResult.objects.update_or_create(
            lost_item=lost_item,
            found_item=found_item,
            defaults={'similarity_score': score}
        )
        
    if top_3:
        create_notification(
            lost_item.user,
            "Matching Found Item Detected!",
            f"Someone reported found a '{top_3[0][0].name}' that strongly matches your lost '{lost_item.name}'. Check your dashboard to contact them!"
        )
    
    return top_3

def find_matches_for_found_item(found_item):
    """
    Compares a found item with all active lost items and stores top 3 matches.
    """
    lost_items = LostItem.objects.filter(is_active=True)
    results = []
    
    for lost_item in lost_items:
        score = calculate_similarity(found_item.image.path, lost_item.image.path)
        if score > 10: # Threshold for a potential match
            results.append((lost_item, score))
    
    # Sort and take top 3
    results.sort(key=lambda x: x[1], reverse=True)
    top_3 = results[:3]
    
    # Store in MatchResult and Notify
    for lost_item, score in top_3:
        MatchResult.objects.update_or_create(
            lost_item=lost_item,
            found_item=found_item,
            defaults={'similarity_score': score}
        )
        
    if top_3:
        # We need to notify the users who lost the items
        for lost_item, score in top_3:
            create_notification(
                lost_item.user,
                "Potential Match for your Lost Item!",
                f"Someone found an item similar to your lost '{lost_item.name}'. Check your dashboard."
            )
            
    # Also notify the user who found the item that we found potential owners
    if top_3:
        create_notification(
            found_item.user,
            "Matches Found for Reported Item",
            f"We found {len(top_3)} lost items that might match what you found. Thank you for reporting!"
        )
    
    return top_3
