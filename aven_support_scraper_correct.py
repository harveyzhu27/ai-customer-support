#!/usr/bin/env python3
"""
Correct Aven Support Page Scraper
Uses the exact selectors found from page analysis
"""

import time
import json
import os
import re
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AvenSupportScraperCorrect:
    def __init__(self, headless: bool = True):
        """
        Initialize the correct scraper
        
        Args:
            headless (bool): Run browser in headless mode
        """
        self.url = "https://www.aven.com/support"
        self.driver = None
        self.headless = headless
        
    def setup_driver(self):
        """Setup Chrome WebDriver with appropriate options"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
        
        # Additional options for better performance and compatibility
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        # Try to find Chrome in common Windows locations
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            r"C:\Users\{}\AppData\Local\Google\Chrome\Application\chrome.exe".format(os.getenv('USERNAME', '')),
            r"C:\Users\{}\AppData\Local\Google\Chrome\Application\chrome.exe".format(os.getenv('USER', '')),
        ]
        
        chrome_found = False
        for chrome_path in chrome_paths:
            if os.path.exists(chrome_path):
                chrome_options.binary_location = chrome_path
                chrome_found = True
                logger.info(f"Found Chrome at: {chrome_path}")
                break
        
        if not chrome_found:
            logger.warning("Chrome not found in common locations. Trying default path...")
        
        try:
            # Use webdriver-manager to automatically download and manage ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info("Chrome WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Chrome WebDriver: {e}")
            logger.error("Please ensure Chrome browser is installed on your system.")
            logger.error("You can download Chrome from: https://www.google.com/chrome/")
            raise
    
    def wait_for_page_load(self, timeout: int = 30):
        """Wait for the page to fully load"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            # Additional wait for dynamic content
            time.sleep(5)
            logger.info("Page loaded successfully")
        except TimeoutException:
            logger.warning("Page load timeout, continuing anyway")
    
    def hide_sticky_navigation(self):
        """Hide the sticky navigation bar that's blocking clicks"""
        try:
            # Try to hide the sticky navigation
            self.driver.execute_script("""
                // Hide sticky navigation elements
                var stickyElements = document.querySelectorAll('nav.sticky, .nav.sticky, [class*="sticky"], [class*="fixed"]');
                for (var i = 0; i < stickyElements.length; i++) {
                    stickyElements[i].style.display = 'none';
                    stickyElements[i].style.visibility = 'hidden';
                    stickyElements[i].style.opacity = '0';
                    stickyElements[i].style.position = 'static';
                }
                
                // Also hide any overlays or modals
                var overlays = document.querySelectorAll('.overlay, .modal, .popup, [class*="overlay"], [class*="modal"]');
                for (var i = 0; i < overlays.length; i++) {
                    overlays[i].style.display = 'none';
                }
            """)
            logger.info("Hidden sticky navigation elements")
        except Exception as e:
            logger.warning(f"Error hiding sticky navigation: {e}")
    
    def scroll_element_into_view_safely(self, element):
        """Scroll element into view while avoiding sticky navigation"""
        try:
            # Get element position
            location = element.location
            size = element.size
            
            # Calculate scroll position to center the element
            window_height = self.driver.execute_script("return window.innerHeight;")
            scroll_y = location['y'] - (window_height / 2) + (size['height'] / 2)
            
            # Add extra space to avoid sticky nav
            scroll_y += 100
            
            # Scroll to position
            self.driver.execute_script(f"window.scrollTo(0, {scroll_y});")
            time.sleep(1)
            
            logger.info(f"Scrolled element into view at position {scroll_y}")
        except Exception as e:
            logger.warning(f"Error scrolling element into view: {e}")
    
    def click_element_safely(self, element, description=""):
        """Click an element safely, handling sticky navigation issues"""
        try:
            # First, scroll the element into view safely
            self.scroll_element_into_view_safely(element)
            
            # Try multiple click methods
            click_success = False
            
            # Method 1: Direct click
            try:
                element.click()
                click_success = True
                logger.info(f"Direct click successful for {description}")
            except Exception as e:
                logger.debug(f"Direct click failed for {description}: {e}")
            
            # Method 2: JavaScript click if direct click failed
            if not click_success:
                try:
                    self.driver.execute_script("arguments[0].click();", element)
                    click_success = True
                    logger.info(f"JavaScript click successful for {description}")
                except Exception as e:
                    logger.debug(f"JavaScript click failed for {description}: {e}")
            
            # Method 3: Action chains if other methods failed
            if not click_success:
                try:
                    from selenium.webdriver.common.action_chains import ActionChains
                    actions = ActionChains(self.driver)
                    actions.move_to_element(element).click().perform()
                    click_success = True
                    logger.info(f"Action chains click successful for {description}")
                except Exception as e:
                    logger.debug(f"Action chains click failed for {description}: {e}")
            
            return click_success
            
        except Exception as e:
            logger.error(f"Error in click_element_safely for {description}: {e}")
            return False
    
    def extract_faq_content(self) -> List[Dict[str, str]]:
        """
        Extract FAQ questions and answers from the page with sections
        
        Returns:
            List[Dict[str, str]]: List of dictionaries with 'section', 'question', 'answer', and 'source_url' keys
        """
        faq_items = []
        
        try:
            # Hide sticky navigation first
            self.hide_sticky_navigation()
            
            # Step 1: Find all sections using the correct selector
            sections = self._find_sections()
            logger.info(f"Found {len(sections)} sections")
            
            # Step 2: Process each section
            for section_name, section_element in sections:
                logger.info(f"Processing section: {section_name}")
                
                # Step 3: Click "SHOW MORE" if present using correct selector
                self._click_show_more_in_section(section_element)
                
                # Step 4: Extract questions and answers from this section
                section_items = self._extract_questions_from_section(section_name, section_element)
                faq_items.extend(section_items)
                
                logger.info(f"Extracted {len(section_items)} items from section '{section_name}'")
            
        except Exception as e:
            logger.error(f"Error extracting FAQ content: {e}")
        
        return faq_items
    
    def _find_sections(self) -> List[tuple]:
        """Find all FAQ sections on the page using correct selector"""
        sections = []
        
        try:
            # Use the exact selector found in analysis: div with class containing 'support-list-section'
            section_elements = self.driver.find_elements(By.CSS_SELECTOR, "div[class*='support-list-section']")
            
            logger.info(f"Found {len(section_elements)} section elements")
            
            for section_element in section_elements:
                # Extract section name from the h5 element within the section
                try:
                    h5_element = section_element.find_element(By.CSS_SELECTOR, "h5")
                    section_name = h5_element.text.strip()
                    if section_name:
                        sections.append((section_name, section_element))
                        logger.info(f"Identified section: {section_name}")
                except:
                    # If no h5 found, use a generic name
                    sections.append((f"Section {len(sections) + 1}", section_element))
            
        except Exception as e:
            logger.error(f"Error finding sections: {e}")
        
        return sections
    
    def _click_show_more_in_section(self, section_element):
        """Click 'SHOW MORE' buttons within a section using correct selector"""
        try:
            # Use the exact selector found in analysis: a with classes 'show-more small spaced-text'
            show_more_elements = section_element.find_elements(By.CSS_SELECTOR, "a.show-more.small.spaced-text")
            
            if show_more_elements:
                logger.info(f"Found {len(show_more_elements)} 'SHOW MORE' elements in section")
                
                for i, element in enumerate(show_more_elements):
                    try:
                        if element.is_displayed() and element.is_enabled():
                            # Use safe click method
                            if self.click_element_safely(element, f"SHOW MORE button {i+1}"):
                                time.sleep(2)  # Wait for content to load
                            
                    except Exception as e:
                        logger.debug(f"Error clicking 'SHOW MORE' element {i+1}: {e}")
                        continue
            else:
                logger.debug("No 'SHOW MORE' buttons found in this section")
            
        except Exception as e:
            logger.error(f"Error clicking show more in section: {e}")
    
    def _extract_questions_from_section(self, section_name: str, section_element) -> List[Dict[str, str]]:
        """Extract questions and answers from a specific section using correct selectors"""
        section_items = []
        
        try:
            # Use the exact selector found in analysis: a with classes 'd-flex justify-content-between mb-2 title'
            question_elements = section_element.find_elements(By.CSS_SELECTOR, "a.d-flex.justify-content-between.mb-2.title")
            
            if question_elements:
                logger.info(f"Found {len(question_elements)} questions in section '{section_name}'")
                
                for question_element in question_elements:
                    try:
                        # Extract question text
                        question_text = question_element.text.strip()
                        
                        if not question_text or len(question_text) < 5:
                            continue
                        
                        logger.info(f"Processing question: {question_text[:50]}...")
                        
                        # Click the question to expand it (since it's an <a> tag)
                        if self.click_element_safely(question_element, "question element"):
                            time.sleep(1)  # Wait for answer to appear
                            
                            # Look for the answer content
                            answer = self._find_answer_content(question_element)
                            
                            if answer:
                                section_items.append({
                                    "section": section_name,
                                    "question": question_text,
                                    "answer": answer,
                                    "source_url": self.url
                                })
                                logger.info(f"Successfully extracted Q&A pair for section '{section_name}'")
                            else:
                                logger.warning(f"No answer found for question: {question_text[:50]}...")
                        
                    except Exception as e:
                        logger.debug(f"Error processing question element: {e}")
                        continue
            else:
                logger.warning(f"No questions found in section '{section_name}'")
            
        except Exception as e:
            logger.error(f"Error extracting questions from section '{section_name}': {e}")
        
        return section_items
    
    def _find_answer_content(self, question_element) -> str:
        """Find the answer content after expanding a question using correct selectors"""
        try:
            # Wait a bit for the answer to appear after clicking
            time.sleep(1)
            
            # Based on the analysis, look for answer in <span p> structure (176 elements found)
            # and <p> elements (214 elements found)
            
            # Method 1: Look for <span p> structure (as shown in the image)
            try:
                # Look in the parent container of the question
                parent = question_element.find_element(By.XPATH, "..")
                
                # Look for <span p> elements
                span_p_elements = parent.find_elements(By.CSS_SELECTOR, "span p")
                for elem in span_p_elements:
                    text = elem.text.strip()
                    if len(text) > 20 and text != question_element.text.strip():
                        logger.info(f"Found answer in span p: {text[:50]}...")
                        return text
                
                # Look for any <p> elements
                p_elements = parent.find_elements(By.CSS_SELECTOR, "p")
                for elem in p_elements:
                    text = elem.text.strip()
                    if len(text) > 20 and text != question_element.text.strip():
                        logger.info(f"Found answer in p: {text[:50]}...")
                        return text
                        
            except Exception as e:
                logger.debug(f"Error looking in parent container: {e}")
            
            # Method 2: Look in next sibling elements
            try:
                for i in range(1, 4):  # Check next 3 siblings
                    try:
                        next_sibling = question_element.find_element(By.XPATH, f"following-sibling::*[{i}]")
                        text = next_sibling.text.strip()
                        if len(text) > 20 and text != question_element.text.strip():
                            logger.info(f"Found answer in sibling {i}: {text[:50]}...")
                            return text
                    except:
                        continue
            except Exception as e:
                logger.debug(f"Error looking in siblings: {e}")
            
            # Method 3: Use JavaScript to find answer content
            try:
                answer_text = self.driver.execute_script("""
                    // Look for answer content near the question element
                    var questionElement = arguments[0];
                    var parent = questionElement.parentElement;
                    
                    // Look for <span p> structure (as shown in the image)
                    var spanPElements = parent.querySelectorAll('span p');
                    for (var i = 0; i < spanPElements.length; i++) {
                        var text = spanPElements[i].textContent.trim();
                        if (text.length > 20 && text !== questionElement.textContent.trim()) {
                            return text;
                        }
                    }
                    
                    // Look for any <p> tags
                    var pElements = parent.querySelectorAll('p');
                    for (var i = 0; i < pElements.length; i++) {
                        var text = pElements[i].textContent.trim();
                        if (text.length > 20 && text !== questionElement.textContent.trim()) {
                            return text;
                        }
                    }
                    
                    // Look in next siblings
                    var nextSibling = questionElement.nextElementSibling;
                    if (nextSibling && nextSibling.textContent.trim().length > 20) {
                        return nextSibling.textContent.trim();
                    }
                    
                    return "";
                """, question_element)
                
                if answer_text:
                    logger.info(f"Found answer via JavaScript: {answer_text[:50]}...")
                    return answer_text
                    
            except Exception as e:
                logger.debug(f"Error with JavaScript answer search: {e}")
            
        except Exception as e:
            logger.debug(f"Error finding answer content: {e}")
        
        return ""
    
    def scrape(self) -> List[Dict[str, str]]:
        """
        Main scraping method
        
        Returns:
            List[Dict[str, str]]: List of FAQ items with sections
        """
        try:
            logger.info(f"Starting to scrape: {self.url}")
            
            # Setup driver
            self.setup_driver()
            
            # Navigate to the page
            self.driver.get(self.url)
            
            # Wait for page to load
            self.wait_for_page_load()
            
            # Extract FAQ content
            faq_items = self.extract_faq_content()
            
            logger.info(f"Successfully extracted {len(faq_items)} FAQ items")
            return faq_items
            
        except Exception as e:
            logger.error(f"Error during scraping: {e}")
            return []
        
        finally:
            if self.driver:
                self.driver.quit()
                logger.info("WebDriver closed")
    
    def save_to_json(self, faq_items: List[Dict[str, str]], filename: str = "aven_support_faq_correct.json"):
        """Save FAQ items to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(faq_items, f, indent=2, ensure_ascii=False)
            logger.info(f"FAQ items saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving to JSON: {e}")
    
    def save_to_txt(self, faq_items: List[Dict[str, str]], filename: str = "aven_support_faq_correct.txt"):
        """Save FAQ items to text file with clear section delineation"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("Aven Support FAQ (Correct Version)\n")
                f.write("=" * 50 + "\n\n")
                
                # Group items by section
                sections = {}
                for item in faq_items:
                    section = item.get('section', 'General')
                    if section not in sections:
                        sections[section] = []
                    sections[section].append(item)
                
                # Write each section
                for section_name, items in sections.items():
                    f.write(f"Section: {section_name}\n")
                    f.write("-" * 30 + "\n\n")
                    
                    for i, item in enumerate(items, 1):
                        f.write(f"Question {i}: {item['question']}\n")
                        f.write(f"Answer {i}: {item['answer']}\n")
                        f.write(f"Source: {item['source_url']}\n")
                        f.write("\n")
                    
                    f.write("\n" + "=" * 50 + "\n\n")
            
            logger.info(f"FAQ items saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving to text: {e}")


def main():
    """Main function to run the correct scraper"""
    # Create scraper instance (set headless=False to see the browser)
    scraper = AvenSupportScraperCorrect(headless=True)
    
    # Scrape the FAQ content
    faq_items = scraper.scrape()
    
    if faq_items:
        # Save results
        scraper.save_to_json(faq_items)
        scraper.save_to_txt(faq_items)
        
        # Print summary
        print(f"\nScraping completed successfully!")
        print(f"Found {len(faq_items)} FAQ items")
        
        # Group by section and display
        sections = {}
        for item in faq_items:
            section = item.get('section', 'General')
            if section not in sections:
                sections[section] = []
            sections[section].append(item)
        
        print(f"\nSections found: {len(sections)}")
        for section_name, items in sections.items():
            print(f"\nSection: {section_name}")
            print(f"  Questions: {len(items)}")
            for i, item in enumerate(items[:2], 1):  # Show first 2 questions per section
                print(f"    {i}. {item['question'][:50]}...")
            if len(items) > 2:
                print(f"    ... and {len(items) - 2} more questions")
    else:
        print("No FAQ items found. The page structure might be different than expected.")


if __name__ == "__main__":
    main() 