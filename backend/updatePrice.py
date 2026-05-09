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
def update(newList, driver):
    print("UPDATEPRICE: file/function entered", flush=True)
    print(f"UPDATEPRICE: received {len(newList)} mods", flush=True)

    wait = WebDriverWait(driver, 25)

    try:
        print("UPDATEPRICE: trying to switch status to Invisible", flush=True)

        hover_box = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".avatarContainer--O6m1G"))
        )

        ActionChains(driver).move_to_element(hover_box).perform()
        time.sleep(1)

        invisible_btn = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul.online-switch--UKLjA li.invisible--G4TBX"))
        )

        if "active" not in invisible_btn.get_attribute("class"):
            driver.execute_script("arguments[0].click();", invisible_btn)
            print("UPDATEPRICE: switched to Invisible", flush=True)
        else:
            print("UPDATEPRICE: already Invisible", flush=True)

    except Exception as e:
        print(f"UPDATEPRICE: could not switch status, continuing anyway: {type(e).__name__}: {e}", flush=True)

    for mod in newList:
        print(f"\nUPDATEPRICE: starting mod: {mod}", flush=True)

        try:
            input_box = wait.until(
                EC.element_to_be_clickable((By.ID, "nameSearch"))
            )

            current_text = input_box.get_attribute("value")

            if current_text:
                try:
                    clear_button = wait.until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "clear-button--Ddryp"))
                    )
                    driver.execute_script("arguments[0].click();", clear_button)
                    print("UPDATEPRICE: search clear button clicked", flush=True)
                    time.sleep(1)
                except Exception as clear_error:
                    print(f"UPDATEPRICE: clear button not found/clickable: {type(clear_error).__name__}", flush=True)
                    input_box.send_keys(Keys.CONTROL + "a")
                    input_box.send_keys(Keys.DELETE)
            else:
                print("UPDATEPRICE: search input already empty", flush=True)

            input_box = wait.until(
                EC.element_to_be_clickable((By.ID, "nameSearch"))
            )

            input_box.click()
            input_box.send_keys(Keys.CONTROL + "a")
            input_box.send_keys(Keys.DELETE)
            input_box.send_keys(mod)

            print(f"UPDATEPRICE: searched for mod: {mod}", flush=True)
            time.sleep(1.5)

            edit_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space()='Edit']]"))
            )

            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_button)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", edit_button)

            print("UPDATEPRICE: clicked Edit", flush=True)

            orders = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.mini__order--MENE4"))
            )

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
                    time.sleep(3)
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

            price_input = wait.until(
                EC.element_to_be_clickable((By.ID, "editOrderItemPrice"))
            )
            price_input.click()
            price_input.send_keys(Keys.CONTROL + "a")
            price_input.send_keys(Keys.DELETE)
            price_input.send_keys(str(PricePerUnit))
            print("UPDATEPRICE: filled price", flush=True)

            quantity_input = wait.until(
                EC.element_to_be_clickable((By.ID, "editOrderQuantity"))
            )
            quantity_input.click()
            quantity_input.send_keys(Keys.CONTROL + "a")
            quantity_input.send_keys(Keys.DELETE)
            quantity_input.send_keys("1")
            print("UPDATEPRICE: filled quantity", flush=True)

            rank_input = wait.until(
                EC.element_to_be_clickable((By.ID, "editOrderRank"))
            )
            rank_input.click()
            rank_input.send_keys(Keys.CONTROL + "a")
            rank_input.send_keys(Keys.DELETE)
            rank_input.send_keys("0")
            print("UPDATEPRICE: filled rank", flush=True)

            update_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space()='Update']]"))
            )

            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", update_button)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", update_button)

            print("UPDATEPRICE: clicked Update", flush=True)

            time.sleep(1.5)

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
                    print("UPDATEPRICE: closed modal", flush=True)
                    break

            if not closed:
                print("UPDATEPRICE WARNING: no visible Close button found", flush=True)

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