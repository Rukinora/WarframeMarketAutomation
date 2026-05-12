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
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

def add(modlist, driver):
    # Debug -> App has entered addMods.py and returns amount of mods from- 
    # modList in config.
    print("ADDMODS: file/function entered", flush=True)
    print(f"ADDMODS: received {len(modlist)} mods", flush=True)

    wait = WebDriverWait(driver, 20)

    for mod in modlist:
        # Debug -> prints current mod name in config(modList).
        print(f"\nADDMODS: starting mod: {mod}", flush=True)
        
        # If any step is missed for adding the mod, the except: will print out 
        # what went wrong.
        try:
            # Searches for the "Invisible" tag on profile view. To set profile 
            # from either Online-InGame or Online to Invisible.
            time.sleep(1)
            wait.until(
                EC.invisibility_of_element_located(
                    (By.CSS_SELECTOR, "div.modal--Csf66"))
            )
            
            
            
            ### ----- Step 1 ----- ###
            # Debug -> Step1 Start
            print("ADDMODS: waiting for plus button", flush=True) 
            # Locates button element
            plus_button = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "div.big-red__button"))
            )
            # Scrolls element into view
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", plus_button)
            time.sleep(0.5)
            # Clicks button element
            driver.execute_script("arguments[0].click();", plus_button)
            # Debug -> Step1 Done
            print("ADDMODS: clicked plus button", flush=True) 
            
            
            
            ### ----- Step 2 ----- ###
            # Debug -> Step2 Start
            print("ADDMODS: waiting for item input", flush=True)
            # waits to locate item Input element
            item_input = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "input[placeholder='Select Item']"))
            )
            # clicks inside of input element
            item_input.click()
            # select all
            item_input.send_keys(Keys.CONTROL + "a")
            # delete all
            item_input.send_keys(Keys.DELETE)
            # inputs mod name
            item_input.send_keys(mod)
            # Debug -> Entered Mod Name
            print(f"ADDMODS: typed mod name: {mod}", flush=True)
            time.sleep(1)
            # Pressed Enter
            item_input.send_keys(Keys.ENTER)
            # Debug -> Pressed Enter Key In Mod Input element; Step 2 Done
            print("ADDMODS: selecting typed mod / place order area", flush=True)
            time.sleep(1)
            
            
            
            ### ----- Step 3 ----- ###
            # Debug -> Step 3 Start
            print("ADDMODS: waiting for price input", flush=True)
            # waits for the Item Price Input element
            price_input = wait.until(
                EC.element_to_be_clickable((By.ID, "orderItemPrice"))
            )
            # clicks in the input element
            price_input.click()
            # select all
            price_input.send_keys(Keys.CONTROL + "a")
            # delete
            price_input.send_keys(Keys.DELETE)
            # inputs price number from saved config value
            price_input.send_keys(str(get_config_val("min_plat_price")))
            # Debug -> Step 3 End
            print("ADDMODS: filled price", flush=True)



            ### ----- Step 4 ----- ###
            # wait for quantity input element
            quantity_input = wait.until(
                EC.element_to_be_clickable((By.ID, "orderQuantity"))
            )
            # clicks in element
            quantity_input.click()
            # select all
            quantity_input.send_keys(Keys.CONTROL + "a")
            # delete
            quantity_input.send_keys(Keys.DELETE)
            # inputs 1 in the element "Only selling one mod"
            quantity_input.send_keys("1")
            # Debug -> Step 4 End
            print("ADDMODS: filled quantity", flush=True)



            ### ----- Step 5 ----- ###
            # Waits for rank input box
            rank_input = wait.until(
                EC.element_to_be_clickable((By.ID, "orderRank"))
            )
            # Clicks rank input
            rank_input.click()
            # Select all existing text
            rank_input.send_keys(Keys.CONTROL + "a")
            # Deletes old rank
            rank_input.send_keys(Keys.DELETE)
            # Inputs rank 0
            rank_input.send_keys("0")
            # Debug -> rank entered
            print("ADDMODS: filled rank", flush=True)

            
            
            ### ----- Step 6 ----- ###
            # Waits for Post button
            post_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[.//span[normalize-space()='Post']]"))
            )
            # Scrolls Post button into center view
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", post_button)
            time.sleep(0.5)
            # Clicks post button
            driver.execute_script("arguments[0].click();", post_button)
            # Debug -> post button clicked
            print("ADDMODS: clicked Post", flush=True)
            time.sleep(1)

            
            
            ### ----- Step 7 ----- ###
            # Waits for all Close buttons from popup
            close_buttons = wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//button[.//span[normalize-space()='Close']]"))
            )
            # Tracks if a visible close button was found
            closed = False
            # Loops through all close buttons
            for btn in close_buttons:
                # Only clicks visible button
                if btn.is_displayed():
                    # Scroll into view
                    driver.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'});", btn)
                    time.sleep(0.5)
                    # Clicks close button
                    driver.execute_script("arguments[0].click();", btn)
                    closed = True
                    # Debug -> popup closed
                    print("ADDMODS: closed modal", flush=True)
                    break
            # Debug warning if no visible close button found        
            if not closed:
                print(
                    "ADDMODS WARNING: no visible Close button found",
                    flush=True)
            # Debug -> mod successfully posted
            print(f"ADDMODS SUCCESS: posted {mod}", flush=True)

        except Exception as e:
            # Debug -> mod failed
            print(f"\nADDMODS ERROR: failed on mod: {mod}", flush=True)
            # Prints exact selenium/python error
            print(f"ADDMODS ERROR DETAILS: {type(e).__name__}: {e}", flush=True)

            # Recovery system:
            # Reloads warframe profile page so next mod
            # can continue instead of crashing app.
            try:
                driver.get(get_config_val("warframe_link"))
                time.sleep(3)
                print("ADDMODS: recovered by reloading profile page", flush=True)
            # Recovery itself failed
            except Exception as recover_error:
                print(f"ADDMODS RECOVERY FAILED: {recover_error}", flush=True)