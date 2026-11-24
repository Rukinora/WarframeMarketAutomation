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
from waitHelper import wait_for_element, wait_and_click, wait_for_all_elements
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
            wait.until(
                EC.invisibility_of_element_located(
                    (By.CSS_SELECTOR, "div.modal--Csf66"))
            )
            
            
            
            ### ----- Step 1 ----- ###
            # Debug -> Step1 Start
            print("ADDMODS: waiting for plus button", flush=True) 
            # Locates button element
            if not wait_and_click(driver, wait, (By.CSS_SELECTOR, "div.big-red__button"), scroll=True):
                print("ADDMODS: plus button not found, skipping this mod", flush=True)
                continue
            # Debug -> Step1 Done
            print("ADDMODS: clicked plus button", flush=True)
            
            
            
            ### ----- Step 2 ----- ###
            # Debug -> Step2 Start
            print("ADDMODS: waiting for item input", flush=True)
            # waits to locate item Input element
            item_input = wait_for_element(driver, wait, 
                (By.CSS_SELECTOR, "input[placeholder='Select Item']"), 
                condition=EC.element_to_be_clickable)
            if not item_input:
                print("ADDMODS: item input not found, skipping this mod", flush=True)
                continue
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
            # Pressed Enter
            item_input.send_keys(Keys.ENTER)
            # Debug -> Pressed Enter Key In Mod Input element; Step 2 Done
            print("ADDMODS: selecting typed mod / place order area", flush=True)
            
            
            
            ### ----- Step 3 ----- ###
            # Debug -> Step 3 Start
            print("ADDMODS: waiting for price input", flush=True)
            # waits for the Item Price Input element
            price_input = wait_for_element(driver, wait, 
                (By.ID, "orderPrice"), 
                condition=EC.element_to_be_clickable)
            if not price_input:
                print("ADDMODS: price input not found, skipping this mod", flush=True)
                continue
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
            quantity_input = wait_for_element(driver, wait, 
                (By.ID, "orderQuantity"), 
                condition=EC.element_to_be_clickable)
            if not quantity_input:
                print("ADDMODS: quantity input not found, skipping this mod", flush=True)
                continue
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
            rank_input = wait_for_element(driver, wait, 
                (By.ID, "orderRank"), 
                condition=EC.element_to_be_clickable)
            if not rank_input:
                print("ADDMODS: rank input not found, skipping this mod", flush=True)
                continue
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
            if not wait_and_click(driver, wait, 
                (By.XPATH, "//button[.//span[normalize-space()='Post']]"), 
                scroll=True):
                print("ADDMODS: post button not found, skipping this mod", flush=True)
                continue
            # Debug -> post button clicked
            print("ADDMODS: clicked Post", flush=True)

            
            
            ### ----- Step 7 ----- ###
            # Waits for all Close buttons from popup
            close_buttons = wait_for_all_elements(driver, wait, 
                (By.XPATH, "//button[.//span[normalize-space()='Close']]"))
            
            if not close_buttons:
                print("ADDMODS WARNING: no close buttons found", flush=True)
            else:
                # Tracks if a visible close button was found
                closed = False
                # Loops through all close buttons
                for btn in close_buttons:
                    # Only clicks visible button
                    if btn.is_displayed():
                        # Scroll into view
                        driver.execute_script(
                            "arguments[0].scrollIntoView({block: 'center'});", btn)
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