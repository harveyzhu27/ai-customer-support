#!/usr/bin/env python3
"""
Quick Page Analysis Script
Helps identify the correct HTML structure for questions and answers
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def analyze_page_structure():
    """Analyze the page structure to find questions and answers"""
    
    # Setup driver
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Navigate to the page
        print("Loading page...")
        driver.get("https://www.aven.com/support")
        time.sleep(5)
        
        print("\n" + "="*60)
        print("PAGE STRUCTURE ANALYSIS")
        print("="*60)
        
        # 1. Look for section headers
        print("\n1. SECTION HEADERS:")
        print("-" * 30)
        section_selectors = ["h1", "h2", "h3", "h4", "h5", "h6", "[class*='section']", "[class*='title']"]
        for selector in section_selectors:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                print(f"\nSelector '{selector}' found {len(elements)} elements:")
                for i, elem in enumerate(elements[:3]):  # Show first 3
                    text = elem.text.strip()
                    classes = elem.get_attribute('class')
                    tag = elem.tag_name
                    print(f"  {i+1}. Tag: {tag}, Classes: {classes}, Text: {text[:50]}...")
        
        # 2. Look for questions
        print("\n\n2. POTENTIAL QUESTIONS:")
        print("-" * 30)
        question_selectors = [
            "[class*='question']", 
            "[class*='faq']", 
            "h3", "h4", "h5", "h6",
            "div[class*='item']",
            "a[class*='title']",
            "p[class*='question']"
        ]
        
        for selector in question_selectors:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                print(f"\nSelector '{selector}' found {len(elements)} elements:")
                for i, elem in enumerate(elements[:3]):  # Show first 3
                    text = elem.text.strip()
                    classes = elem.get_attribute('class')
                    tag = elem.tag_name
                    if len(text) > 10:  # Only show substantial text
                        print(f"  {i+1}. Tag: {tag}, Classes: {classes}, Text: {text[:80]}...")
        
        # 3. Look for SHOW MORE buttons
        print("\n\n3. SHOW MORE BUTTONS:")
        print("-" * 30)
        show_more_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'SHOW MORE')]")
        print(f"Found {len(show_more_elements)} elements containing 'SHOW MORE':")
        for i, elem in enumerate(show_more_elements):
            tag = elem.tag_name
            classes = elem.get_attribute('class')
            text = elem.text.strip()
            print(f"  {i+1}. Tag: {tag}, Classes: {classes}, Text: {text}")
        
        # 4. Look for down arrows/expand icons
        print("\n\n4. DOWN ARROWS / EXPAND ICONS:")
        print("-" * 30)
        arrow_selectors = [
            "[class*='arrow']",
            "[class*='chevron']", 
            "[class*='expand']",
            "[class*='toggle']",
            "svg",
            "i[class*='arrow']",
            "i[class*='chevron']"
        ]
        
        for selector in arrow_selectors:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                print(f"\nSelector '{selector}' found {len(elements)} elements:")
                for i, elem in enumerate(elements[:3]):  # Show first 3
                    classes = elem.get_attribute('class')
                    tag = elem.tag_name
                    print(f"  {i+1}. Tag: {tag}, Classes: {classes}")
        
        # 5. Look for answer content
        print("\n\n5. POTENTIAL ANSWER CONTENT:")
        print("-" * 30)
        answer_selectors = [
            "[class*='answer']",
            "[class*='content']", 
            "[class*='body']",
            "span p",
            "p",
            "div[class*='description']"
        ]
        
        for selector in answer_selectors:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                print(f"\nSelector '{selector}' found {len(elements)} elements:")
                for i, elem in enumerate(elements[:3]):  # Show first 3
                    text = elem.text.strip()
                    classes = elem.get_attribute('class')
                    tag = elem.tag_name
                    if len(text) > 20:  # Only show substantial text
                        print(f"  {i+1}. Tag: {tag}, Classes: {classes}, Text: {text[:80]}...")
        
        print("\n" + "="*60)
        print("ANALYSIS COMPLETE")
        print("="*60)
        print("\nPlease share this output with me so I can identify the correct selectors!")
        
        # Keep browser open for manual inspection
        input("\nPress Enter to close the browser...")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    analyze_page_structure() 