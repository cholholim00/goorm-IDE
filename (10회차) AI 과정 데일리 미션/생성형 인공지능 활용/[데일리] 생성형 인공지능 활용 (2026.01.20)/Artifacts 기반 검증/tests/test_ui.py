"""
UI Tests for BMI Calculator Streamlit App using Playwright
Tests the web interface functionality including input validation and result display.
"""

import unittest
import time
from playwright.sync_api import sync_playwright, expect


class TestBMICalculatorUI(unittest.TestCase):
    """Test cases for BMI Calculator Streamlit UI"""
    
    @classmethod
    def setUpClass(cls):
        """Set up Playwright browser before all tests"""
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)
        cls.context = cls.browser.new_context()
        cls.page = cls.context.new_page()
        cls.base_url = "http://localhost:8501"
        
        # Navigate to the app
        cls.page.goto(cls.base_url)
        # Wait for Streamlit to load
        time.sleep(3)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        cls.context.close()
        cls.browser.close()
        cls.playwright.stop()
    
    def setUp(self):
        """Reset the page before each test"""
        self.page.reload()
        time.sleep(2)
    
    def test_page_title(self):
        """Test that the page title is correct"""
        self.assertIn("BMI 계산기", self.page.title())
    
    def test_page_has_header(self):
        """Test that the page has the correct header"""
        header = self.page.locator("h1").first
        expect(header).to_contain_text("BMI 계산기")
    
    def test_input_fields_exist(self):
        """Test that height and weight input fields exist"""
        # Check for number input fields
        inputs = self.page.locator('input[type="number"]')
        count = inputs.count()
        self.assertGreaterEqual(count, 2, "Should have at least 2 number input fields")
    
    def test_calculate_button_exists(self):
        """Test that the calculate button exists"""
        button = self.page.locator('button:has-text("계산하기")')
        expect(button).to_be_visible()
    
    def test_normal_weight_calculation(self):
        """Test BMI calculation for normal weight category"""
        # Find input fields by their labels
        height_input = self.page.locator('input[type="number"]').first
        weight_input = self.page.locator('input[type="number"]').nth(1)
        
        # Clear and enter values
        height_input.click()
        height_input.fill("")
        height_input.type("170")
        
        weight_input.click()
        weight_input.fill("")
        weight_input.type("65")
        
        # Click calculate button
        calculate_button = self.page.locator('button:has-text("계산하기")')
        calculate_button.click()
        
        # Wait for results
        time.sleep(2)
        
        # Check that results are displayed
        page_content = self.page.content()
        self.assertIn("결과", page_content)
        self.assertIn("정상", page_content)
    
    def test_underweight_calculation(self):
        """Test BMI calculation for underweight category"""
        height_input = self.page.locator('input[type="number"]').first
        weight_input = self.page.locator('input[type="number"]').nth(1)
        
        height_input.click()
        height_input.fill("")
        height_input.type("170")
        
        weight_input.click()
        weight_input.fill("")
        weight_input.type("50")
        
        calculate_button = self.page.locator('button:has-text("계산하기")')
        calculate_button.click()
        
        time.sleep(2)
        
        page_content = self.page.content()
        self.assertIn("저체중", page_content)
    
    def test_overweight_calculation(self):
        """Test BMI calculation for overweight category"""
        height_input = self.page.locator('input[type="number"]').first
        weight_input = self.page.locator('input[type="number"]').nth(1)
        
        height_input.click()
        height_input.fill("")
        height_input.type("170")
        
        weight_input.click()
        weight_input.fill("")
        weight_input.type("70")
        
        calculate_button = self.page.locator('button:has-text("계산하기")')
        calculate_button.click()
        
        time.sleep(2)
        
        page_content = self.page.content()
        self.assertIn("과체중", page_content)
    
    def test_obese_calculation(self):
        """Test BMI calculation for obese category"""
        height_input = self.page.locator('input[type="number"]').first
        weight_input = self.page.locator('input[type="number"]').nth(1)
        
        height_input.click()
        height_input.fill("")
        height_input.type("170")
        
        weight_input.click()
        weight_input.fill("")
        weight_input.type("80")
        
        calculate_button = self.page.locator('button:has-text("계산하기")')
        calculate_button.click()
        
        time.sleep(2)
        
        page_content = self.page.content()
        self.assertIn("비만", page_content)
    
    def test_bmi_value_displayed(self):
        """Test that BMI numerical value is displayed"""
        height_input = self.page.locator('input[type="number"]').first
        weight_input = self.page.locator('input[type="number"]').nth(1)
        
        height_input.click()
        height_input.fill("")
        height_input.type("170")
        
        weight_input.click()
        weight_input.fill("")
        weight_input.type("65")
        
        calculate_button = self.page.locator('button:has-text("계산하기")')
        calculate_button.click()
        
        time.sleep(2)
        
        # Check that BMI value is displayed
        page_content = self.page.content()
        self.assertIn("BMI 수치", page_content)
    
    def test_bmi_reference_info_displayed(self):
        """Test that BMI reference information is displayed after calculation"""
        height_input = self.page.locator('input[type="number"]').first
        weight_input = self.page.locator('input[type="number"]').nth(1)
        
        height_input.click()
        height_input.fill("")
        height_input.type("175")
        
        weight_input.click()
        weight_input.fill("")
        weight_input.type("68")
        
        calculate_button = self.page.locator('button:has-text("계산하기")')
        calculate_button.click()
        
        time.sleep(2)
        
        # Check for BMI reference information
        page_content = self.page.content()
        self.assertIn("BMI 기준", page_content)
        self.assertIn("18.5", page_content)
        self.assertIn("23", page_content)
        self.assertIn("25", page_content)
    
    def test_decimal_input_values(self):
        """Test that decimal values work correctly"""
        height_input = self.page.locator('input[type="number"]').first
        weight_input = self.page.locator('input[type="number"]').nth(1)
        
        height_input.click()
        height_input.fill("")
        height_input.type("175.5")
        
        weight_input.click()
        weight_input.fill("")
        weight_input.type("68.5")
        
        calculate_button = self.page.locator('button:has-text("계산하기")')
        calculate_button.click()
        
        time.sleep(2)
        
        # Should display results without error
        page_content = self.page.content()
        self.assertIn("결과", page_content)
    
    def test_multiple_calculations(self):
        """Test performing multiple calculations in sequence"""
        height_input = self.page.locator('input[type="number"]').first
        weight_input = self.page.locator('input[type="number"]').nth(1)
        calculate_button = self.page.locator('button:has-text("계산하기")')
        
        # First calculation
        height_input.click()
        height_input.fill("")
        height_input.type("170")
        weight_input.click()
        weight_input.fill("")
        weight_input.type("65")
        calculate_button.click()
        time.sleep(2)
        
        # Second calculation with different values
        height_input.click()
        height_input.fill("")
        height_input.type("180")
        weight_input.click()
        weight_input.fill("")
        weight_input.type("75")
        calculate_button.click()
        time.sleep(2)
        
        # Should display results
        page_content = self.page.content()
        self.assertIn("결과", page_content)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
