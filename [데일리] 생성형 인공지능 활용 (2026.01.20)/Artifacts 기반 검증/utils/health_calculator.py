"""
Health Calculator Module
Provides functions for calculating health metrics like BMI.
"""


def calculate_bmi(height_cm, weight_kg):
    """
    Calculate BMI and return the category.
    
    Args:
        height_cm: Height in centimeters
        weight_kg: Weight in kilograms
    
    Returns:
        str: BMI category ('저체중', '정상', '과체중', or '비만')
    
    Raises:
        ValueError: If height or weight is invalid (non-numeric, zero, or negative)
        TypeError: If height or weight is not a number
    """
    # Type validation
    if not isinstance(height_cm, (int, float)):
        raise TypeError("키는 숫자여야 합니다")
    
    if not isinstance(weight_kg, (int, float)):
        raise TypeError("몸무게는 숫자여야 합니다")
    
    # Value validation
    if height_cm <= 0:
        raise ValueError("키는 0보다 커야 합니다")
    
    if weight_kg <= 0:
        raise ValueError("몸무게는 0보다 커야 합니다")
    
    # Convert height from cm to meters
    height_m = height_cm / 100
    
    # Calculate BMI
    bmi = weight_kg / (height_m ** 2)
    
    # Determine category based on BMI
    if bmi < 18.5:
        return "저체중"
    elif bmi < 23:
        return "정상"
    elif bmi < 25:
        return "과체중"
    else:
        return "비만"
