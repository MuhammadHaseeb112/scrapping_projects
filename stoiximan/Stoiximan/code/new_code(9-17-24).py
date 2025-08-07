from datetime import datetime
import pytz
import pandas as pd
import getpass
import random
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import time


def current_date():
    # Getting current date of Greece 'Europe/Athens'
    # Define the timezone for Greece
    greece_timezone = pytz.timezone('Europe/Athens')
    # Get the current date and time in Greece
    greece_time = datetime.now(greece_timezone)
    # Format the date as dd/MM/yyyy
    greece_date = greece_time.strftime('%Y/%m/%d')
    # Print the formatted date
    return greece_date
    
def process_currency_string(s):
    # Remove the "€" symbol
    s = s.replace("€", "").strip()

    # Replace the last comma with a dot
    parts = s.rsplit(',', 1)
    if len(parts) == 2:
        s = parts[0] + '.' + parts[1]

    # Remove any remaining commas
    s = s.replace(',', '')

    # Convert the resulting string to a float or int
    try:
        value = float(s)
        if value.is_integer():
            return int(value)
        return value
    except ValueError:
        raise ValueError(f"Unable to convert the string '{s}' to a number.")
    
    
# human like delay
def human_like_delay(min_delay=1, max_delay=2):
    time.sleep(random.uniform(min_delay, max_delay))
    
    
def login(page, username, password):
    # login
    try:
        login_button = page.query_selector(
            "button[class='tw-whitespace-nowrap tw-p-n tw-text-white tw-cursor-pointer tw-rounded-sm tw-uppercase tw-font-bold tw-text-xxs tw-leading-4 tw-text-center hover:tw-text-white tw-border-solid tw-border-2 tw-border-transparent tw- tw-bg-secondary hover:tw-bg-secondary-hover']")
        login_button.click()

        print("click login button")
        time.sleep(2)

        # iframe_element = page.query_selector("iframe[title='iframe banner']")
        iframe_element = page.query_selector("iframe[src='/myaccount/login']")
        try:
            if iframe_element:
                print("Iframe found, switching context.")

                # Step 2: Access the iframe content
                iframe = iframe_element.content_frame()

                # Step 3: Wait for the username field and fill it
                iframe.wait_for_selector("#username", timeout=20000)
                iframe.query_selector("#username").fill(f"{username}")
                iframe.query_selector("input[name='Password']").fill(f"{password}")
                page.screenshot(path=f'2.png')
                iframe.query_selector("button[aria-label='login submit']").click()
                print("login_button press")
                human_like_delay(3, 5)
        except Exception as e:
            print(f"Error : {e}")
            pass
    except:
        print("login button not found")
        page.screenshot(path=f'4.png')

        pass
    
def calculate_ammount(page):
    try:
        # calculating price
        price = page.query_selector(".tw-font-bold.tw-text-white.tw-mr-xs.tw-whitespace-nowrap")
        account_balance = price.inner_html()
        print(f"account balance string {account_balance}")
        account_balance = process_currency_string(account_balance)
        print(f"account balance string {account_balance} type {type(account_balance)}")
        # price_per_bid =  account_balance/number_of_links
        # print(price_per_bid)
        price_per_bid = round(account_balance / 3, 2)
        return price_per_bid
        # print(f"price_per_bid: {price_per_bid}")
        # price_per_bid = price_per_bid - 0.01
        # print(f"price_per_bid after subtrcting 0.01: {price_per_bid}")

        # formatted_price_per_bid = round(price_per_bid, 2)
    except:
        print("can not access the ammountS")
        return None
   
   
def click_result(page, result, container, link, button):
    
    if link != None:
        link1 = link + button

        # Navigate to the constructed link and wait for the page to load
        page.goto(link1, timeout=60000)
        page.wait_for_load_state('domcontentloaded')
        
        
    result_text = str(result)
    result_text = result_text.strip()
    # container = "Τελικό Αποτέλεσμα"
    # Find the container div with the text "Τελικό Αποτέλεσμα"
    container = page.query_selector(f'div.tw-p-nm:has-text("{container}")')
    print(container.inner_text())
    
    if container:
        print(f"Result = {result_text}")
        
        span_selector = f'span.s-name:has-text("{result_text}")'
        span_element = container.query_selector(span_selector)
        
        if not span_element:
            result_parts = result.split(" ")
            if len(result_parts) != 2:
                print(f"Invalid result format: {result}")
                return
            result_main, result_sub = result_parts
            combined_selector = f'span.s-name:has-text("{result_main}") >> xpath=following-sibling::span[contains(@class, "s-name-sub") and text()="{result_sub}"]'
            span_element = container.query_selector(combined_selector)
            
        if span_element:
            span_element.click()
            print(f'Clicked on span.s-name with text {result_text}')
        else:
            print(f'No span with text {result_text} found inside the container')
    else:
        print(f'Container with "{container}" not found')

def enter_price(bid_ammount):

    input = page.query_selector("input[class='stake-input GTM-stakeInput stake-input--is-multiple']")
    if input:
        input.click()
        time.sleep(0.5)
        input.fill(f"{bid_ammount}")
        print(f"Price:{bid_ammount} Enter")
        time.sleep(2)
    else:
        print("Input field not found")
        return
    # bet button
    bet_button = page.query_selector(".tw-flex.tw-justify-center.tw-transition-transform.tw-duration-slow.tw-ease-out-back.tw-translate-y-0")
    bet_button.click()
    print("Bet Done")
    
data_file =  pd.read_excel("excel\example of excel2.xlsx") # change the excel file name 

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



# main code  
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
    page.goto("https://www.stoiximan.gr/live/", timeout=60000)
    webdriver_flag = page.evaluate('''() => {
                    return window.navigator.webdriver
                    }''')
    human_like_delay(3,5)
    
    login_details = pd.read_excel("excel/login.xlsx")
    
    for index, row in login_details.iterrows():
        username = row['username']
        password = row['password']

        username = "stavrk"
        password = "Stoixi91@"
        # browser.clear_cookies()
        
        login(page, username, password)
        # time.sleep(4)        
        bid_ammount = calculate_ammount(page)
        
        print(bid_ammount)
        
        greece_date = current_date()    
        print("Current date in Greece (yyyy/mm/dd):", greece_date)
    
        # links file 
        data_file = pd.read_excel("excel/example of excel.xlsx")  # change the excel file name
        
        for index, row in data_file.iterrows():
            date = row["DATE (dd/MM/yyyy)"].strftime('%Y/%m/%d')
            link = row["GAME URL"]
            result = row["RESULT"]
            print(f"{date} vs {greece_date}")
            if not pd.isna(row["RESULT"]):
                if date == greece_date:
                    print("")
                    print("date match")
                    try:
                        page.goto(link, timeout=60000)
                        print(link)
                        webdriver_flag = page.evaluate('''() => {
                        return window.navigator.webdriver
                        }''')
                        human_like_delay(3, 5)
                        page.wait_for_load_state("load")  # Wait for the page to load
                        print("Link open")
                        # print(page.url())
                        # current_url = page.url()
                        # if link == current_url:

                        # pressing Results

                        current_url = page.evaluate("window.location.href")
                        # if link == current_url:
                        if result in [1, 'X', 2]:
                            print(f"result in {[1, 'X', 2]}")
                            click_result(page, result, "Τελικό Αποτέλεσμα", None, None)
                        elif result in ['Over 0.5', 'Over 1.5','Over 3.5', 'Over 4.5','Over 5.5', 'Over 6.5','Over 7.5', 'Over 8.5','Over 9.5', 'Under 0.5', 'Under 1.5', 'Under 3.5', 'Under 4.5', 'Under 5.5', 'Under 6.5', 'Under 7.5', 'Under 8.5', 'Under 9.5']:
                            print(f"result in {['Over 0.5', 'Over 1.5', 'Under 3.5', 'Under 4.5']}")
                            click_result(page, result, "Γκολ Over/Under (extra)", link, "?bt=1")
                        elif result in ['0-4', '0-5', '1-5']:
                            print(f"result in {['0-4', '0-5', '1-5']}")
                            click_result(page, result, "Γκολ", link, "?bt=2")
                        elif result in ['Under 2.5']:
                            print(f"result in {['Over 2.5','Under 2.5']}")
                            click_result(page, result, "1ο Ημίχρονο - Γκολ Over/Under", link, "?bt=3")
                        else:
                            print("Invalid result provided")
                        # else:
                        #     print("link not found")
                    except:
                        print(f"game url not found")
    bid_ammount = 1
    enter_price(bid_ammount)

    page.close()
    browser.close()
