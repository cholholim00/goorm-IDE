"""
Unit tests for health_calculator module
Tests normal cases and edge cases including error conditions.
"""

import unittest
import sys
import os

# Add parent directory to path to import utils module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.health_calculator import calculate_bmi


class TestHealthCalculator(unittest.TestCase):
    """Test cases for BMI calculator function"""
    
    def test_underweight(self):
        """Test BMI calculation for underweight category"""
        result = calculate_bmi(170, 50)
        self.assertEqual(result, "저체중")
    
    def test_normal_weight(self):
        """Test BMI calculation for normal weight category"""
        result = calculate_bmi(170, 65)
        self.assertEqual(result, "정상")
    
    def test_overweight(self):
        """Test BMI calculation for overweight category"""
        result = calculate_bmi(170, 70)
        self.assertEqual(result, "과체중")
    
    def test_obese(self):
        """Test BMI calculation for obese category"""
        result = calculate_bmi(170, 80)
        self.assertEqual(result, "비만")
    
    def test_height_zero(self):
        """Test that zero height raises ValueError"""
        with self.assertRaises(ValueError) as context:
            calculate_bmi(0, 70)
        self.assertIn("0보다 커야", str(context.exception))
    
    def test_height_negative(self):
        """Test that negative height raises ValueError"""
        with self.assertRaises(ValueError) as context:
            calculate_bmi(-170, 70)
        self.assertIn("0보다 커야", str(context.exception))
    
    def test_weight_zero(self):
        """Test that zero weight raises ValueError"""
        with self.assertRaises(ValueError) as context:
            calculate_bmi(170, 0)
        self.assertIn("0보다 커야", str(context.exception))
    
    def test_weight_negative(self):
        """Test that negative weight raises ValueError"""
        with self.assertRaises(ValueError) as context:
            calculate_bmi(170, -70)
        self.assertIn("0보다 커야", str(context.exception))
    
    def test_height_string(self):
        """Test that string height raises TypeError"""
        with self.assertRaises(TypeError) as context:
            calculate_bmi("170", 70)
        self.assertIn("숫자여야", str(context.exception))
    
    def test_weight_string(self):
        """Test that string weight raises TypeError"""
        with self.assertRaises(TypeError) as context:
            calculate_bmi(170, "70")
        self.assertIn("숫자여야", str(context.exception))
    
    def test_height_none(self):
        """Test that None height raises TypeError"""
        with self.assertRaises(TypeError):
            calculate_bmi(None, 70)
    
    def test_weight_none(self):
        """Test that None weight raises TypeError"""
        with self.assertRaises(TypeError):
            calculate_bmi(170, None)
    
    def test_float_values(self):
        """Test that float values work correctly"""
        result = calculate_bmi(175.5, 68.5)
        self.assertIn(result, ["저체중", "정상", "과체중", "비만"])
    
    def test_boundary_underweight_normal(self):
        """Test boundary between underweight and normal (BMI = 18.5)"""
        # BMI = 18.5 for height 170cm
        weight = 18.5 * (1.7 ** 2)
        result = calculate_bmi(170, weight)
        self.assertEqual(result, "정상")
    
    def test_boundary_normal_overweight(self):
        """Test boundary between normal and overweight (BMI = 23)"""
        # BMI = 23 for height 170cm
        weight = 23 * (1.7 ** 2)
        result = calculate_bmi(170, weight)
        self.assertEqual(result, "과체중")
    
    def test_boundary_overweight_obese(self):
        """Test boundary between overweight and obese (BMI = 25)"""
        # BMI = 25 for height 170cm - exactly 25 is still overweight
        weight = 25 * (1.7 ** 2)
        result = calculate_bmi(170, weight)
        self.assertEqual(result, "과체중")
    
    def test_obese_above_25(self):
        """Test obese category (BMI > 25)"""
        # BMI slightly above 25 for height 170cm
        weight = 25.1 * (1.7 ** 2)
        result = calculate_bmi(170, weight)
        self.assertEqual(result, "비만")


if __name__ == '__main__':
    unittest.main()
