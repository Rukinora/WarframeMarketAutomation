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
def update(newList,driver):
    wait = WebDriverWait(driver, 15)
    # print(newList)
    hover_box = driver.find_element(By.CSS_SELECTOR, ".avatarContainer--O6m1G")
    # <div class="combobox-title--I_acz combobox-avatar--cBdaT"><div class="avatarContainer--O6m1G"><img class="avatarImage--Wira1 user__avatar--_0NiC" alt="Avatar" 
    # src="https://warframe.market/static/assets/user/avatar/5e150dc2870b59031b4603e8.png?08f20040295368d57e18295f45266b87"></div>
    # <div class="user-and-status--HjZL3"><span class="nickname--sKj0R">Locamoto</span><div class="user-status--DupbM online-indicator--zLJop">
    # <span class="ingame--OWe2B">Online in game</span></div></div><svg class="wfm-icon icon-caret-left" viewBox="0 0 192 512">
    # <use xlink:href="/static/build/resources/wfm-icons-05e4fc.svg#icon-caret-left"></use></svg></div>
    
    
    # <li class="invisible--G4TBX active">Invisible</li>
    
    # <li class="invisible--G4TBX">Invisible</li>
    actions = ActionChains(driver)
    actions.move_to_element(hover_box).perform()
    time.sleep(3)
    
    invisible_btn = driver.find_element(By.CSS_SELECTOR, ".invisible--G4TBX")
    invisible_btn.click()
    
    
    for mod in newList:
        
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

        #Inputes mod name in search
        input_box.send_keys(mod)
        
        #clicks on edit button from seached mod.
        edit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Edit']]")))
        edit_button.click()
        
        
        # <li class="mini__order--MENE4 with_rank--YZwcZ"><div class="user--iTSO4"><div class="status--MpTqR ingame--F_ShX"></div><div class="name--J4Rgn">fromnda</div></div><div class="reputation--g7bO1"><div class="user__reputation user__reputation--neutral">1<svg class="wfm-icon icon-meh" viewBox="0 0 496 512"><use xlink:href="/static/build/resources/wfm-icons-05e4fc.svg#icon-meh"></use></svg></div></div><div class="platinum--Nh413"><div class="platinum--luI6m end--Bqgxf"><div class="price--LQgqJ sell--UxmH0"><b>8</b><svg class="wfm-icon icon-platinum" viewBox="0 0 215.535 215.535"><use xlink:href="/static/build/resources/wfm-icons-05e4fc.svg#icon-platinum"></use></svg></div></div></div><div class="rank--Fw7TL"><div class="mod-rank--OkkkB"><span>0 of 3</span></div></div><div class="quantity--HmXRR">1<svg class="wfm-icon icon-cubes" viewBox="0 0 512 512"><use xlink:href="/static/build/resources/wfm-icons-05e4fc.svg#icon-cubes"></use></svg></div></li>
        #waits for the list of 5 users info to load
        orders = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.mini__order--MENE4"))
        )
        
        #finds the cheapest sell price for online In game user
        first_online_price = None
        for order in orders:
            status_div = order.find_element(By.CSS_SELECTOR, "div.status--MpTqR")
            status_class = status_div.get_attribute("class")

            if "ingame--F_ShX" in status_class:  # user is online
                price_b = order.find_element(By.CSS_SELECTOR, "div.price--LQgqJ b")
                price_text = price_b.text.strip()

                if price_text:  # make sure it's not empty
                    first_online_price = int(price_text.split()[0])
                    break

        if first_online_price:
            print(f"First online user's price: {first_online_price}")
        else:
            print("No online users found.")
        first_online_price = int(first_online_price)
        PricePerUnit = 0
        minimum = int(get_config_val("min_plat_price"))
        if first_online_price > minimum:
            PricePerUnit = first_online_price
        elif first_online_price <= minimum:
            PricePerUnit = minimum
        
        
        price_input = wait.until(EC.element_to_be_clickable((By.ID, "editOrderItemPrice")))

        price_input.send_keys(Keys.CONTROL + "a")
        price_input.send_keys(Keys.DELETE)
        price_input.click()
        price_input.send_keys(PricePerUnit)
        
        quantity_input = wait.until(EC.element_to_be_clickable((By.ID, "editOrderQuantity")))
        quantity_input.send_keys(Keys.CONTROL + "a")
        quantity_input.send_keys(Keys.DELETE)
        quantity_input.click()
        quantity_input.send_keys(1)
        
        rank_input = wait.until(EC.element_to_be_clickable((By.ID, "editOrderRank")))
        rank_input.send_keys(Keys.CONTROL + "a")
        rank_input.send_keys(Keys.DELETE)
        rank_input.click()
        rank_input.send_keys(0)
        
        update_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Update']]")))
        update_button.click()
        # <button class="btn btn__primary--L8HyD red--sqBa6" tabindex="0" type="button"><div><span>Close</span></div></button>
        
        time.sleep(1)
        # Wait until at least one Close button is visible and clickable
        
        close_buttons = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[.//span[text()='Close']]"))
        )

        # Filter to the first displayed (visible) button
        for btn in close_buttons:
            if btn.is_displayed():
                # Scroll into view
                driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                # Click using JS for safety
                driver.execute_script("arguments[0].click();", btn)
                break