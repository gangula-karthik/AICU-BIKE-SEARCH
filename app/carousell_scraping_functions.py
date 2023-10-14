import requests
import pandas as pd
import time
import matplotlib.pyplot as plt
import re
import numpy as np
from collections import Counter
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def initialize_driver(url: str) -> webdriver.Chrome:
    """
    Initializes a new instance of the Chrome driver, opens the specified URL, 
    and returns the driver instance.

    The function utilizes the ChromeDriverManager to handle the installation of 
    the ChromeDriver executable, which is necessary for Selenium WebDriver to 
    interact with the Chrome browser.

    Parameters:
    -----------
    url : str
        The URL to open in the Chrome browser.

    Returns:
    --------
    webdriver.Chrome
        The initialized Chrome driver instance with the specified URL loaded.
    """

    # Install and retrieve the path to the ChromeDriver executable
    # using ChromeDriverManager.
    service = ChromeService(executable_path=ChromeDriverManager().install())

    # Initialize a new instance of the Chrome driver.
    driver = webdriver.Chrome(service=service)

    # Open the specified URL in the Chrome browser.
    driver.get(url)

    # Return the initialized Chrome driver instance.
    print("Driver initialized successfully", driver.__class__)
    return driver



def scroll_page(driver: webdriver.Chrome, max_scrolls: int = 10) -> None:
    """
    Scrolls down a webpage in a Selenium WebDriver controlled browser, 
    attempting to click a "Read More" button if found during scrolling. 
    The page is scrolled down by the height of the browser window, 
    pausing for a short duration between each scroll.

    Parameters:
    -----------
    driver : webdriver.Chrome
        The Selenium WebDriver instance controlling the browser.
    
    max_scrolls : int, optional (default=10)
        The maximum number of times to scroll down the page.

    Returns:
    --------
    None

    Examples:
    ---------
    >>> driver = initialize_driver("https://example.com")
    >>> scroll_page(driver, max_scrolls=5)
    # The page at https://example.com should now be scrolled down 5 times.

    Notes:
    ------
    - The function attempts to click a "Read More" button, if present, to 
      expand the content on the page.
    - A pause of 1 second is added between each scroll to allow the page 
      content to load.
    - A pause of 3 seconds is added after clicking the "Read More" button to 
      allow the expanded content to load.
    """

    # Get the height of the screen
    screen_height = driver.execute_script("return window.screen.height;")
    i = 1
    scroll_count = 0

    # Continue scrolling until the maximum scroll count is reached
    while scroll_count < max_scrolls:
        # Scroll down by screen_height * i pixels
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
        time.sleep(1)  # Wait for 1 second
        
        # Attempt to click the "Read More" button if present
        try:
            read_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.D_Mw > div > button")))
            if read_more_button:
                print("Read more button clicked for the", i, "time")
                read_more_button.click()
                time.sleep(3)  # Wait for 3 seconds
        except:
            pass  # If the "Read More" button is not found, continue scrolling
        
        # Increment the scroll count and the scroll multiplier
        scroll_count += 1
        i += 1

    return "Scrolling completed successfully"



def extract_condition_and_description(driver: webdriver.Chrome, link: str):
    """
    Navigates to a specified URL using a Selenium WebDriver instance, extracts the
    condition and description of a product from the page, and then closes the browser.

    Parameters:
    -----------
    driver : webdriver.Chrome
        The Selenium WebDriver instance controlling the browser.
    
    link : str
        The URL of the product page to extract information from.

    Returns:
    --------
    Tuple[Optional[str], Optional[str]]
        A tuple containing two elements:
        - The condition of the product as a string, or None if not found.
        - The description of the product as a string, or None if not found.

    Examples:
    ---------
    >>> driver = initialize_driver("https://example.com")
    >>> condition, description = extract_condition_and_description(driver, "https://example.com/product/1")

    Notes:
    ------
    - Assumes that the condition and description are located at specific XPath or CSS selectors,
      which may need to be updated if the webpage structure changes.
    - Closes and quits the driver after extracting the information.
    """
    driver.get(link)

    try:
        condition = driver.find_element(By.XPATH, "//*[@id='FieldSetField-Container-field_condition_value']/div/div/div/div/span").text
    except:
        condition = None

    try:
        driver.find_element(By.XPATH, "//*[@id='FieldSetField-Container-field_listing_details_bp']/div/div[5]/button").click()
        time.sleep(3)
        description = driver.find_element(By.CSS_SELECTOR, "#FieldSetField-Container-field_details_bottom_sheet > div > div.D_aCt").text
    except:
        description = None

    driver.close()
    driver.quit()

    return condition, description

def extract_product_data(driver: webdriver.Chrome):
    """
    Navigates to a specified URL using a Selenium WebDriver instance, extracts the
    condition and description of a product from the page, and then closes the browser.

    Parameters:
    -----------
    driver : webdriver.Chrome
        The Selenium WebDriver instance controlling the browser.
    
    link : str
        The URL of the product page to extract information from.

    Returns:
    --------
    Tuple[Optional[str], Optional[str]]
        A tuple containing two elements:
        - The condition of the product as a string, or None if not found.
        - The description of the product as a string, or None if not found.

    Examples:
    ---------
    >>> driver = initialize_driver("https://example.com")
    >>> condition, description = extract_condition_and_description(driver, "https://example.com/product/1")

    Notes:
    ------
    - Assumes that the condition and description are located at specific XPath or CSS selectors,
      which may need to be updated if the webpage structure changes.
    - Closes and quits the driver after extracting the information.
    """
    productList = []

    for x in range(1, 3):
        products = driver.find_elements(By.CSS_SELECTOR, f"#main > div.D_Mf > div > section.D_Mr > div.D_Mw > div > div > div:nth-child({x}) > div")
        
        for product in products: 
            # Extract listing link
            try:
                listing_link = product.find_element(By.CSS_SELECTOR, "div > div.D_zX.M_tF > a:nth-child(2)").get_attribute('href')
            except:
                try:
                    listing_link = product.find_element(By.CSS_SELECTOR, "div > div.D_zX > a:nth-child(2)").get_attribute('href')
                except:
                    listing_link = None

            # Extract product name
            try:
                product_name = product.find_element(By.CSS_SELECTOR, "div > div.D_zX > a:nth-child(2) > p.D_pw.D_ov.D_px.D_pA.D_pE.D_pH.D_pJ.D_pF.D_pN").text
            except:
                try:
                    product_name = product.find_element(By.CSS_SELECTOR, "div > div.D_zX > a.D__c.D_pW > div.D__g > div > p").text
                except:
                    product_name = None

            # Extract image URL
            try:
                img_url = product.find_element(By.TAG_NAME, "img").get_attribute('src')
            except:
                img_url = None

            # Extract listing upload date
            try:
                listing_upload_date = product.find_element(By.CSS_SELECTOR, "div > div.D_zX > a.D__c.D_pW > div.D__g > div > p").text
            except:
                listing_upload_date = None

            data = {
                "listing_link": listing_link,
                "product_name": product_name,
                "img_url": img_url,
                "listing_upload_date": listing_upload_date
            }
            print(data)

            productList.append(data)

    return productList


def close_driver(driver: webdriver.Chrome) -> None:
    """
    Closes the specified Selenium WebDriver instance and quits the browser.
    """
    driver.close()
    driver.quit()
    return "Driver closed successfully"