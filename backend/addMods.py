from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from loadConfig import get_config_val
from selenium.webdriver.common.keys import Keys
#opens warframe link
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
def add(modlist, driver):
    print("ADDMODS: file/function entered", flush=True)
    print(f"ADDMODS: received {len(modlist)} mods", flush=True)

    wait = WebDriverWait(driver, 20)

    for mod in modlist:
        print(f"\nADDMODS: starting mod: {mod}", flush=True)

        try:
            # make sure page/modal is ready
            time.sleep(1)

            wait.until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.modal--Csf66"))
            )

            print("ADDMODS: waiting for plus button", flush=True)
            plus_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.big-red__button"))
            )

            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", plus_button)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", plus_button)
            print("ADDMODS: clicked plus button", flush=True)

            print("ADDMODS: waiting for item input", flush=True)
            item_input = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Select Item']"))
            )

            item_input.click()
            item_input.send_keys(Keys.CONTROL + "a")
            item_input.send_keys(Keys.DELETE)
            item_input.send_keys(mod)
            print(f"ADDMODS: typed mod name: {mod}", flush=True)

            time.sleep(1)

            print("ADDMODS: selecting typed mod / place order area", flush=True)

            # Try pressing Enter first because search dropdowns often accept Enter
            item_input.send_keys(Keys.ENTER)
            time.sleep(1)

            print("ADDMODS: waiting for price input", flush=True)
            price_input = wait.until(
                EC.element_to_be_clickable((By.ID, "orderItemPrice"))
            )

            price_input.click()
            price_input.send_keys(Keys.CONTROL + "a")
            price_input.send_keys(Keys.DELETE)
            price_input.send_keys(str(get_config_val("min_plat_price")))
            print("ADDMODS: filled price", flush=True)

            quantity_input = wait.until(
                EC.element_to_be_clickable((By.ID, "orderQuantity"))
            )
            quantity_input.click()
            quantity_input.send_keys(Keys.CONTROL + "a")
            quantity_input.send_keys(Keys.DELETE)
            quantity_input.send_keys("1")
            print("ADDMODS: filled quantity", flush=True)

            rank_input = wait.until(
                EC.element_to_be_clickable((By.ID, "orderRank"))
            )
            rank_input.click()
            rank_input.send_keys(Keys.CONTROL + "a")
            rank_input.send_keys(Keys.DELETE)
            rank_input.send_keys("0")
            print("ADDMODS: filled rank", flush=True)

            post_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space()='Post']]"))
            )

            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", post_button)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", post_button)
            print("ADDMODS: clicked Post", flush=True)

            time.sleep(1)

            close_buttons = wait.until(
                EC.presence_of_all_elements_located((By.XPATH, "//button[.//span[normalize-space()='Close']]"))
            )

            closed = False
            for btn in close_buttons:
                if btn.is_displayed():
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                    time.sleep(0.5)
                    driver.execute_script("arguments[0].click();", btn)
                    closed = True
                    print("ADDMODS: closed modal", flush=True)
                    break

            if not closed:
                print("ADDMODS WARNING: no visible Close button found", flush=True)

            print(f"ADDMODS SUCCESS: posted {mod}", flush=True)

        except Exception as e:
            print(f"\nADDMODS ERROR: failed on mod: {mod}", flush=True)
            print(f"ADDMODS ERROR DETAILS: {type(e).__name__}: {e}", flush=True)

            # Try to recover before next mod
            try:
                driver.get(get_config_val("warframe_link"))
                time.sleep(3)
                print("ADDMODS: recovered by reloading profile page", flush=True)
            except Exception as recover_error:
                print(f"ADDMODS RECOVERY FAILED: {recover_error}", flush=True)