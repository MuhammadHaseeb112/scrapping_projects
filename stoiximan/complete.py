from datetime import datetime
import pytz
import pandas as pd
import getpass
import random
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import time



# human like delay 
def human_like_delay(min_delay=1, max_delay=2):
    time.sleep(random.uniform(min_delay, max_delay))
    
# getting price for input
input_price = int(input("Please Enter Price: "))
print(f"Input Price: {input_price}")

print("Getting Current Greece Date")
# Getting current date of Greece 'Europe/Athens'
# Define the timezone for Greece
greece_timezone = pytz.timezone('Europe/Athens')
# Get the current date and time in Greece
greece_time = datetime.now(greece_timezone)
# Format the date as dd/MM/yyyy
greece_date = greece_time.strftime('%Y/%m/%d')
# Print the formatted date
print("Current date in Greece (yyyy/mm/dd):", greece_date)

print("Reading Excel File")
data_file =  pd.read_excel("excel\example of excel.xlsx") # change the excel file name 

chrome_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe' # need to change this path
user_dir_path = f"C:\\Users\\Haseeb\\AppData\\Local\\Google\\Chrome\\User Data\\Default" # need to change this path
channel = 'chrome'
headless = False
args = ['--ignore-certificate-errors',
        '--ignore-certificate-errors-spki-list',
        '--disable-blink-features=AutomationControlled',
        '--disable-shm-usage',
        '--disable-infobars',
        '--start-maximized',
        '--window-position=-10,0']


print("Script Running ...")
# Use system use's chrome cache folder
with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
                    user_data_dir=user_dir_path,
                    channel=channel,
                    executable_path=chrome_path,
                    args=args,
                    accept_downloads=True,
                    headless=False,
                    bypass_csp=True,
                )

    page = browser.new_page()
    # stealth_sync(page)

    for index, row in data_file.iterrows():
        date = row["DATE (dd/MM/yyyy)"].strftime('%Y/%m/%d')
        link = row["GAME URL"]
        result = row["RESULT"]
        # print("")
        
        if not pd.isna(row["RESULT"]):
            if date==greece_date:
                print("")
                print("Dates Match and RESULTS available ")
                try:
                    print("opening link")
                    page.goto(link, timeout=60000)            
                    webdriver_flag = page.evaluate('''() => {
                    return window.navigator.webdriver
                    }''')
                    human_like_delay(3,5)
                    
                    
                    # login section
                    try:
                        login_button = page.query_selector("button[class='tw-whitespace-nowrap tw-p-n tw-text-white tw-cursor-pointer tw-rounded-sm tw-uppercase tw-font-bold tw-text-xxs tw-leading-4 tw-text-center hover:tw-text-white tw-border-solid tw-border-2 tw-border-transparent tw- tw-bg-secondary hover:tw-bg-secondary-hover']")
                        login_button.click()
                        
                        print("TRY To Login")
                        # print("2 seconds wait for login popup")
                        time.sleep(2)
                        
                        # iframe_element = page.query_selector("iframe[title='iframe banner']")
                        iframe_element = page.query_selector("iframe[src='/myaccount/login']")
                        try:
                            if iframe_element:
                                # print("Entering ID and Pass")
                                
                                # Step 2: Access the iframe content
                                iframe = iframe_element.content_frame()
                                
                                # Step 3: Wait for the username field and fill it
                                iframe.wait_for_selector("#username", timeout=20000)
                                iframe.query_selector("#username").fill("stavrk")
                                iframe.query_selector("input[name='Password']").fill("Stoixi91@")
                                page.screenshot(path=f'2.png')
                                iframe.query_selector("button[aria-label='login submit']").click()
                                # print("login_button press")
                                human_like_delay(3,5)
                                
                                print("Login Sucessfull")
                        except Exception as e:
                            # print(f"Error : {e}")
                            pass    
                    except:
                        print("User already login")
                        page.screenshot(path=f'4.png')
                    
                        pass
                    
                    
                    # pressing Results
                    try:
                        print(f"Looking for Result: {result}")
                        
                        time.sleep(3)
                        main_section = page.locator(".markets.markets--live.tw-mx-n.tw-mb-m")
                        element = main_section.locator(f'text="{result}"')
                        element.wait_for(state="visible", timeout=20000)  # Wait until the element is visible
                        element.click()
                        # print(f"Result:{result} Press")
                        human_like_delay(3,4)
                        
                        # Enter price
                        print("Looking For Price Input Field")
                        input = page.query_selector("input[class='stake-input GTM-stakeInput']")
                        input.click()
                        # print("Click on price input")
                        time.sleep(0.5)
                        input.fill(f"{input_price}")
                        print(f"Price:{input_price} Enter")
                        time.sleep(2)
                        
                        # bet button
                        bet_button = page.query_selector(".tw-flex.tw-justify-center.tw-transition-transform.tw-duration-slow.tw-ease-out-back.tw-translate-y-0")
                        bet_button.click()
                        # print("Bet button press")
                        print("Bet Successfull")
                        human_like_delay(1,2)
                    except Exception as e:
                        # print("Except 2")
                        # print(f"Error: {e}")
                        print(f"Error occure Due to link: {link} is expire or Result: {result} not found")
                        pass

                except Exception as e:
                    # print("Except 1")
                    # print(f"Error: {e}")
                    print("Page not load due to antibot services")
                    pass
                
    page.close()
    browser.close()
            
            


