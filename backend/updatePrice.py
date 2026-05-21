from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from loadConfig import get_config_val
from waitHelper import wait_for_element, wait_and_click, wait_for_all_elements
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
def update(newList, driver):
    print("UPDATEPRICE: file/function entered", flush=True)
    print(f"UPDATEPRICE: received {len(newList)} mods", flush=True)

    wait = WebDriverWait(driver, 25)

    try:
        print("UPDATEPRICE: trying to switch status to Invisible", flush=True)

        hover_box = wait_for_element(driver, wait, 
            (By.CSS_SELECTOR, ".avatarContainer--O6m1G"))

        if hover_box:
            ActionChains(driver).move_to_element(hover_box).perform()

            invisible_btn = wait_for_element(driver, wait, 
                (By.CSS_SELECTOR, "ul.online-switch--UKLjA li.invisible--G4TBX"))

            if invisible_btn and "active" not in invisible_btn.get_attribute("class"):
                driver.execute_script("arguments[0].click();", invisible_btn)
                print("UPDATEPRICE: switched to Invisible", flush=True)
            else:
                print("UPDATEPRICE: already Invisible", flush=True)

    except Exception as e:
        print(f"UPDATEPRICE: could not switch status, continuing anyway: {type(e).__name__}: {e}", flush=True)

    for mod in newList:
        print(f"\nUPDATEPRICE: starting mod: {mod}", flush=True)

        try:
            input_box = wait_for_element(driver, wait, 
                (By.ID, "nameSearch"), 
                condition=EC.element_to_be_clickable)
            
            if not input_box:
                print("UPDATEPRICE: search input not found, skipping this mod", flush=True)
                continue

            current_text = input_box.get_attribute("value")

            if current_text:
                try:
                    clear_button = wait_for_element(driver, wait, 
                        (By.CLASS_NAME, "clear-button--Ddryp"), 
                        timeout=5,
                        condition=EC.element_to_be_clickable)
                    if clear_button:
                        driver.execute_script("arguments[0].click();", clear_button)
                        print("UPDATEPRICE: search clear button clicked", flush=True)
                    else:
                        print("UPDATEPRICE: clear button not found, using keyboard clear", flush=True)
                        input_box.send_keys(Keys.CONTROL + "a")
                        input_box.send_keys(Keys.DELETE)
                except Exception as clear_error:
                    print(f"UPDATEPRICE: clear button not found/clickable: {type(clear_error).__name__}", flush=True)
                    input_box.send_keys(Keys.CONTROL + "a")
                    input_box.send_keys(Keys.DELETE)
            else:
                print("UPDATEPRICE: search input already empty", flush=True)

            input_box = wait_for_element(driver, wait, 
                (By.ID, "nameSearch"), 
                condition=EC.element_to_be_clickable)

            if not input_box:
                print("UPDATEPRICE: search input lost, skipping this mod", flush=True)
                continue

            input_box.click()
            input_box.send_keys(Keys.CONTROL + "a")
            input_box.send_keys(Keys.DELETE)
            input_box.send_keys(mod)

            print(f"UPDATEPRICE: searched for mod: {mod}", flush=True)

            edit_button = wait_for_element(driver, wait, 
                (By.XPATH, "//button[.//span[normalize-space()='Edit']]"), 
                condition=EC.element_to_be_clickable)

            if not edit_button:
                print("UPDATEPRICE: edit button not found, skipping this mod", flush=True)
                continue

            if not wait_and_click(driver, wait, 
                (By.XPATH, "//button[.//span[normalize-space()='Edit']]"), 
                scroll=True):
                print("UPDATEPRICE: failed to click edit button, skipping this mod", flush=True)
                continue

            print("UPDATEPRICE: clicked Edit", flush=True)

            orders = wait_for_all_elements(driver, wait, 
                (By.CSS_SELECTOR, "li.mini__order--MENE4"))

            if not orders:
                print(f"UPDATEPRICE WARNING: no market orders found for {mod}, skipping", flush=True)
                try:
                    driver.get(get_config_val("warframe_link"))
                except:
                    pass
                continue

            print(f"UPDATEPRICE: found {len(orders)} market orders", flush=True)

            first_online_price = None

            for order in orders:
                try:
                    status_div = order.find_element(By.CSS_SELECTOR, "div.status--MpTqR")
                    status_class = status_div.get_attribute("class")

                    if "ingame--F_ShX" in status_class:
                        price_b = order.find_element(By.CSS_SELECTOR, "div.price--LQgqJ b")
                        price_text = price_b.text.strip()

                        if price_text:
                            first_online_price = int(price_text.split()[0])
                            break
                except Exception:
                    continue

            if first_online_price is None:
                print(f"UPDATEPRICE WARNING: no online in-game price found for {mod}, skipping", flush=True)
                try:
                    driver.get(get_config_val("warframe_link"))
                except:
                    pass
                continue

            print(f"UPDATEPRICE: first online user's price: {first_online_price}", flush=True)

            minimum = int(get_config_val("min_plat_price"))

            if first_online_price > minimum:
                PricePerUnit = first_online_price
            else:
                PricePerUnit = minimum

            print(f"UPDATEPRICE: final price to set: {PricePerUnit}", flush=True)

            price_input = wait_for_element(driver, wait, 
                (By.ID, "editOrderItemPrice"), 
                condition=EC.element_to_be_clickable)
            
            if not price_input:
                print("UPDATEPRICE: price input not found, skipping this mod", flush=True)
                continue
            
            price_input.click()
            price_input.send_keys(Keys.CONTROL + "a")
            price_input.send_keys(Keys.DELETE)
            price_input.send_keys(str(PricePerUnit))
            print("UPDATEPRICE: filled price", flush=True)

            quantity_input = wait_for_element(driver, wait, 
                (By.ID, "editOrderQuantity"), 
                condition=EC.element_to_be_clickable)
            
            if not quantity_input:
                print("UPDATEPRICE: quantity input not found, skipping this mod", flush=True)
                continue
            
            quantity_input.click()
            quantity_input.send_keys(Keys.CONTROL + "a")
            quantity_input.send_keys(Keys.DELETE)
            quantity_input.send_keys("1")
            print("UPDATEPRICE: filled quantity", flush=True)

            rank_input = wait_for_element(driver, wait, 
                (By.ID, "editOrderRank"), 
                condition=EC.element_to_be_clickable)
            
            if not rank_input:
                print("UPDATEPRICE: rank input not found, skipping this mod", flush=True)
                continue
            
            rank_input.click()
            rank_input.send_keys(Keys.CONTROL + "a")
            rank_input.send_keys(Keys.DELETE)
            rank_input.send_keys("0")
            print("UPDATEPRICE: filled rank", flush=True)

            if not wait_and_click(driver, wait, 
                (By.XPATH, "//button[.//span[normalize-space()='Update']]"), 
                scroll=True):
                print("UPDATEPRICE: update button not found, skipping this mod", flush=True)
                continue

            print("UPDATEPRICE: clicked Update", flush=True)

            close_buttons = wait_for_all_elements(driver, wait, 
                (By.XPATH, "//button[.//span[normalize-space()='Close']]"))

            if close_buttons:
                closed = False
                for btn in close_buttons:
                    if btn.is_displayed():
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                        driver.execute_script("arguments[0].click();", btn)
                        closed = True
                        print("UPDATEPRICE: closed modal", flush=True)
                        break

                if not closed:
                    print("UPDATEPRICE WARNING: no visible Close button found", flush=True)
            else:
                print("UPDATEPRICE WARNING: no close buttons found", flush=True)

            print(f"UPDATEPRICE SUCCESS: updated {mod}", flush=True)

        except Exception as e:
            print(f"\nUPDATEPRICE ERROR: failed on mod: {mod}", flush=True)
            print(f"UPDATEPRICE ERROR DETAILS: {type(e).__name__}: {e}", flush=True)

            try:
                driver.get(get_config_val("warframe_link"))
                time.sleep(3)
                print("UPDATEPRICE: recovered by reloading profile page", flush=True)
            except Exception as recover_error:
                print(f"UPDATEPRICE RECOVERY FAILED: {type(recover_error).__name__}: {recover_error}", flush=True)