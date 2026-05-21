"""
Wait helper functions for robust element waiting with graceful fallback.
Replaces time.sleep() calls with explicit waits that check for element presence/clickability.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def wait_for_element(driver, wait_obj, locator, timeout=None, condition=EC.presence_of_element_located):
    """
    Wait for an element with specified condition.
    
    Args:
        driver: Selenium WebDriver instance
        wait_obj: WebDriverWait instance
        locator: Tuple of (By.X, selector)
        timeout: Optional timeout override (uses wait_obj default if None)
        condition: Expected condition function (default: presence_of_element_located)
    
    Returns:
        Element if found, None if timeout
    
    Raises:
        TimeoutException: Will be caught, returns None
    """
    try:
        if timeout:
            return WebDriverWait(driver, timeout).until(condition(locator))
        return wait_obj.until(condition(locator))
    except TimeoutException:
        return None


def wait_and_click(driver, wait_obj, locator, timeout=None, scroll=False):
    """
    Wait for element to be clickable and click it.
    
    Args:
        driver: Selenium WebDriver instance
        wait_obj: WebDriverWait instance
        locator: Tuple of (By.X, selector)
        timeout: Optional timeout override
        scroll: If True, scroll element into view before clicking
    
    Returns:
        True if clicked successfully, False if element not found or not clickable
    """
    from selenium.webdriver.support import expected_conditions as EC
    
    element = wait_for_element(driver, wait_obj, locator, timeout, EC.element_to_be_clickable)
    
    if not element:
        return False
    
    try:
        if scroll:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        driver.execute_script("arguments[0].click();", element)
        return True
    except Exception:
        return False


def wait_for_all_elements(driver, wait_obj, locator, timeout=None):
    """
    Wait for all elements matching locator.
    
    Args:
        driver: Selenium WebDriver instance
        wait_obj: WebDriverWait instance
        locator: Tuple of (By.X, selector)
        timeout: Optional timeout override
    
    Returns:
        List of elements if found, empty list if timeout
    """
    try:
        if timeout:
            return WebDriverWait(driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
        return wait_obj.until(EC.presence_of_all_elements_located(locator))
    except TimeoutException:
        return []
