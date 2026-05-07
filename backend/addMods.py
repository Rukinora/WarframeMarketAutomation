from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from loadConfig import get_config_val
#opens warframe link
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
def add(modlist, driver):
    wait = WebDriverWait(driver, 10)
    for mod in modlist:
        try:
            wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.modal--Csf66")))

            plus_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.big-red__button"))
            )
            plus_button.click()

            item_input = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Select Item']"))
            )
            item_input.click()
            item_input.send_keys(mod)
            
            from selenium.webdriver.common.action_chains import ActionChains

            place_order = wait.until(
                EC.presence_of_element_located((By.XPATH, "//h2[text()='Place order']"))
            )

            ActionChains(driver).move_to_element(place_order).click().perform()

            price_input = wait.until(
                EC.visibility_of_element_located((By.ID, "orderItemPrice"))
            )
            price_input.click()
            price_input.send_keys(get_config_val("min_plat_price"))

            quantity_input = wait.until(
                EC.visibility_of_element_located((By.ID, "orderQuantity"))
            )
            quantity_input.click()
            quantity_input.send_keys(1)

            rank_input = wait.until(
                EC.visibility_of_element_located((By.ID, "orderRank"))
            )
            rank_input.click()
            rank_input.send_keys(0)

            post_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Post']]"))
            )
            post_button.click()

            close_buttons = wait.until(
                EC.presence_of_all_elements_located((By.XPATH, "//button[.//span[text()='Close']]"))
            )

            for btn in close_buttons:
                if btn.is_displayed():
                    driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                    driver.execute_script("arguments[0].click();", btn)
                    break

        except Exception as e:
            print(f"\n❌ Failed on mod: {mod}")
            print(f"Error: {e}\n")
    
    