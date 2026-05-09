import webbrowser
import argparse
from loadConfig import *
import SyndicateMods
import updatePrice
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#opens warframe link
from selenium import webdriver
import deleteAll
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import addMods
options = Options()
firstRun = True
# 🔥 Dedicated persistent profile
options.add_argument(r"user-data-dir=C:\ChromeAutomationProfile")
options.add_argument("--profile-directory=SeleniumProfile")
# Optional but recommended
options.add_argument("--start-maximized")

options.add_argument("--remote-debugging-port=9222")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)



#which item in the UI "index.html" is being pressed
#specifically what school - Arbiters, Cephalon, etc. and what button. update or remove/update
parser = argparse.ArgumentParser()
parser.add_argument("--item", type=str, required=True)
parser.add_argument("--action", type=str, required=True)
args = parser.parse_args()



modList = SyndicateMods.mods(args.item)

if args.action == "login":
    driver.get("https://warframe.market/")
    
    print("Waiting for user to log in...", flush=True)
    


elif args.action == "update_prices":
    driver.get(get_config_val("warframe_link"))
    modList = SyndicateMods.mods(args.item)
    updatePrice.update(modList, driver)


elif args.action == "add_mods":
    driver.get(get_config_val("warframe_link"))
    modList = SyndicateMods.mods(args.item)
    addMods.add(modList, driver)
    updatePrice.update(modList, driver)


elif args.action == "delete_all_mods":
    driver.get(get_config_val("warframe_link"))
    deleteAll.delete(driver)


elif args.action == "close_browser":
    driver.quit()
    



