import getpass
import random
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import time
import pandas as pd


def human_like_delay(min_delay=0.5, max_delay=1.5):
    time.sleep(random.uniform(min_delay, max_delay))

chrome_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
user_dir_path = f"C:\\Users\\Haseeb\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
channel = 'chrome'
headless = False
args = ['--ignore-certificate-errors',
        '--ignore-certificate-errors-spki-list',
        '--disable-blink-features=AutomationControlled',
        '--disable-shm-usage',
        '--disable-infobars',
        '--start-maximized',
        '--window-position=-10,0']


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
    
    
    
    
    page.goto('https://www.stoiximan.gr/live/makabi-axi-nazaret-xapoel-boueine/54656691/', timeout=60000)
    webdriver_flag = page.evaluate('''() => {
                return window.navigator.webdriver
            }''')
    time.sleep(10)
    # return False
    print(f'window navigator webdriver value: {webdriver_flag}')
    page.screenshot(path=f'1.png')
    
    print("link is open")
    try:
        login_button = page.query_selector("button[class='tw-whitespace-nowrap tw-p-n tw-text-white tw-cursor-pointer tw-rounded-sm tw-uppercase tw-font-bold tw-text-xxs tw-leading-4 tw-text-center hover:tw-text-white tw-border-solid tw-border-2 tw-border-transparent tw- tw-bg-secondary hover:tw-bg-secondary-hover']")
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
                iframe.query_selector("#username").fill("stavrk")
                iframe.query_selector("input[name='Password']").fill("Stoixi91@")
                page.screenshot(path=f'2.png')
                iframe.query_selector("button[aria-label='login submit']").click()
                print("login_button press")
        except Exception as e:
            print(f"Error : {e}")
            pass    
    except:
        print("login button not found")
        page.screenshot(path=f'4.png')
    
        pass
    time.sleep(20)
    page.screenshot(path=f'3.png')
    
    
    # pressing on 1
    main_section = page.locator(".markets.markets--live.tw-mx-n.tw-mb-m")
    element = main_section.locator('text="1X"')
    element.wait_for(state="visible", timeout=20000)  # Wait until the element is visible
    element.click()
    print("1 Press")
    
    time.sleep(3)
    input = page.query_selector("input[class='stake-input GTM-stakeInput']")
    input.click()
    input.fill("0.5")
    time.sleep(20)
    
    page.screenshot(path=f'example_with_persistent2.png')
    
    
    
    page.close()
    browser.close()
    