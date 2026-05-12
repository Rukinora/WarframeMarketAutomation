from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time



# Deletes all current market orders shown on the profile page.
def delete(driver):
    # Creates reusable selenium wait object
    wait = WebDriverWait(driver, 10)
    ### ----- Step 1 ----- ###
    # Waits for the search input box at the top of orders list
    input_box = wait.until(
        EC.presence_of_element_located(
            (By.ID, "nameSearch")
        )
    )
    # Gets current text inside search box
    current_text = input_box.get_attribute("value")
    # If search box contains text,
    # remove the filter before deleting orders.
    if current_text:
        try:
            # Debug -> search filter detected
            print(
                "DELETEALL: search filter detected",
                flush=True
            )
            # Finds the small X/clear button
            clear_button = driver.find_element(
                By.CLASS_NAME,
                "clear-button--Ddryp"
            )
            # Clicks clear button
            clear_button.click()
            # Debug -> search filter removed
            print(
                "DELETEALL: remove button clicked",
                flush=True
            )
        except Exception as e:
            # Debug -> failed removing search filter
            print(
                f"DELETEALL ERROR: "
                f"remove button not found: {e}",
                flush=True
            )
    else:
        # Debug -> search box already empty
        print(
            "DELETEALL: input is empty, nothing to remove",
            flush=True
        )
    ### ----- Step 2 ----- ###
    # Loops forever until no more orders exist
    while True:
        try:
            # Debug -> searching for first order
            print(
                "DELETEALL: searching for first order",
                flush=True
            )
            # Waits for first order row on page
            # Warframe Market uses data-index='0'
            first_order = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[data-index='0']")
                )
            )
            # Debug -> order found
            print(
                "DELETEALL: first order found",
                flush=True
            )
            # Finds trash/delete button inside order row
            trash_btn = first_order.find_element(
                By.CSS_SELECTOR,
                "button.order__trash"
            )
            # Scrolls trash button into view
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                trash_btn
            )
            time.sleep(0.5)
            # Clicks trash button
            driver.execute_script(
                "arguments[0].click();",
                trash_btn
            )
            # Debug -> trash button clicked
            print(
                "DELETEALL: clicked trash button",
                flush=True
            )
            ### ----- Step 3 ----- ###
            # Waits for confirmation popup "Yes" button
            yes_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[.//span[text()='Yes']]")
                )
            )
            # Scrolls confirmation button into view
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                yes_button
            )
            time.sleep(0.5)
            # Clicks Yes confirmation
            driver.execute_script(
                "arguments[0].click();",
                yes_button
            )
            # Debug -> confirmed delete
            print(
                "DELETEALL: confirmed delete",
                flush=True
            )
            # Small delay so DOM/page updates properly
            time.sleep(2)

        except Exception as e:
            # Debug -> no more orders found
            print(
                f"DELETEALL: stopping delete loop: {e}",
                flush=True
            )

            # Exits loop
            break
    # Debug -> all orders removed
    print(
        "DELETEALL SUCCESS: all first-index orders deleted!",
        flush=True
    )