from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def delete(driver):
    wait = WebDriverWait(driver, 10)
    input_box = wait.until(EC.presence_of_element_located((By.ID, "nameSearch")))
    current_text = input_box.get_attribute("value")
    if current_text:  # if there's any text inside
        try:
            clear_button = driver.find_element(By.CLASS_NAME, "clear-button--Ddryp")
# <button class="btn clear-button--Ddryp" tabindex="0"><svg class="wfm-icon icon-backspace" viewBox="0 0 640 512"><use xlink:href="/static/build/resources/wfm-icons-05e4fc.svg#icon-backspace"></use></svg></button>
            clear_button.click()
            print("Remove button clicked!")
        except:
            print("Remove button not found")
    else:
        print("Input is empty, nothing to remove")

    while True:
        try:
            # Find the first order with data-index="0"
            first_order = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-index='0']"))
            )

            # Find the trash button inside this order
            trash_btn = first_order.find_element(By.CSS_SELECTOR, "button.order__trash")

            # Click the trash button
            trash_btn.click()

            # Wait for the Yes button in the confirmation popup
            yes_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Yes']]"))
            )
            yes_button.click()

            # Small pause to let DOM update
            time.sleep(2)
        except:
            # No more orders with data-index="0"
            break

    print("All first-index orders deleted!")
        
    #     while True:
    #     try:
    #         # Wait for at least one trash icon to be present
    #         trash_btn = wait.until(
    #         EC.element_to_be_clickable((By.CSS_SELECTOR, "button.order__trash"))
    #     )

    #         # Scroll into view
    #         driver.execute_script("arguments[0].scrollIntoView(true);", trash_btn)

    #         # Click the trash button
    #         trash_btn.click()

    #         # Wait for the confirmation 'Yes' button and click it
    #         yes_button = wait.until(
    #             EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Yes']]"))
    #         )
    #         yes_button.click()

    #         # Small delay to let the DOM update
    #         time.sleep(1)
    #     except:
    #         # No more trash buttons left
    #         break

    # print("All trash items deleted!")