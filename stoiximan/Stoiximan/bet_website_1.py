from datetime import datetime
import pytz
import pandas as pd
import getpass
import random
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import time


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


def click_result1x2(page, result):
    result_text = str(result)

    # Find the container div with the text "Τελικό Αποτέλεσμα"
    container = page.query_selector('div.tw-self-center:has-text("Τελικό Αποτέλεσμα")')

    if container:
        # Wait for the span.s-name element to be visible within the container
        page.click(f'span.s-name:has-text("{result_text}")')

        # page.wait_for_selector(
        #         f'div.tw-self-center:has-text("Τελικό Αποτέλεσμα") >> xpath=//span[@class="s-name" and contains(text(), "{result_text}")]', timeout=10000)

        # page.wait_for_selector(
        #     f'div.tw-self-center:has-text("Τελικό Αποτέλεσμα") >> xpath=//span[@class="s-name" and contains(text(), "{result_text}")]', timeout=10000)

        # Find the span.s-name inside this container that has the text corresponding to the result
        span_selector = f'span.s-name:has-text("{result_text}")'
        span_element = container.query_selector(span_selector)

        if span_element:
            span_element.click()
            print(f'Clicked on span.s-name with text {result_text}')
        else:
            print(f'No span with text {result_text} found inside the container')
    else:
        print('Container with "Τελικό Αποτέλεσμα" not found')


def click_resultOverUnder(link, page, result):
    # Split the result (e.g., "Over 0.5") into two parts
    result_parts = result.split(" ")
    if len(result_parts) != 2:
        print(f"Invalid result format: {result}")
        return

    result_main, result_sub = result_parts
    print(f'{result_main} - {result_sub}')
    link1 = link + '?bt=1'

    # Navigate to the constructed link and wait for the page to load
    page.goto(link1, timeout=60000)
    page.wait_for_load_state('domcontentloaded')  # Ensures the page is fully loaded

    # Find the container div with the text "Γκολ Over/Under (extra)"
    container = page.query_selector('div.tw-self-center:has-text("Γκολ Over/Under (extra)")')
    container = page.query_selector('div.tw-self-center:has-text("Γκολ Over/Under (extra)")')

    if container:
        print(container.inner_html())  # Print the container's HTML to inspect the structure
    else:
        print('Container with "Γκολ Over/Under (extra)" not found')
    if container:
        # Find both span.s-name (main result) and span.s-name-sub (sub-result) together
        combined_selector = f'span.s-name:has-text("{result_main}") >> xpath=following-sibling::span[contains(@class, "s-name-sub") and text()="{result_sub}"]'

        span_main_element = container.query_selector(combined_selector)

        if span_main_element:
            # Click the main element (this is the element that represents both Over/Under and the number)
            span_main_element.click()
            print(f'Clicked on "{result_main} {result_sub}"')
        else:
            print(f'No matching span with "{result_main} {result_sub}" found inside the container')
    else:
        print('Container with "Γκολ Over/Under (extra)" not found')


# human like delay
def human_like_delay(min_delay=1, max_delay=2):
    time.sleep(random.uniform(min_delay, max_delay))


# getting price for input
# input_price = int(input("Please Enter Price: "))
# print(f"Input Price: {input_price}")

# Getting current date of Greece 'Europe/Athens'
# Define the timezone for Greece
greece_timezone = pytz.timezone('Europe/Athens')
# Get the current date and time in Greece
greece_time = datetime.now(greece_timezone)
# Format the date as dd/MM/yyyy
greece_date = greece_time.strftime('%Y/%m/%d')
# Print the formatted date
print("Current date in Greece (yyyy/mm/dd):", greece_date)

data_file = pd.read_excel("excel/example of excel.xlsx")  # change the excel file name

chrome_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'  # need to change this path
user_dir_path = f"C:\\Users\\stavros\\AppData\\Local\\Google\\Chrome\\User Data\\Default"  # need to change this path
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
    page.goto("https://www.stoiximan.gr", timeout=60000)
    webdriver_flag = page.evaluate('''() => {
                    return window.navigator.webdriver
                    }''')
    human_like_delay(3, 5)

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
                iframe.query_selector("#username").fill("stavrk")
                iframe.query_selector("input[name='Password']").fill("Stoixi91@")
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

    time.sleep(3)
    number_of_links = len(data_file["RESULT"])
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

        # print(f"price_per_bid: {price_per_bid}")
        # price_per_bid = price_per_bid - 0.01
        # print(f"price_per_bid after subtrcting 0.01: {price_per_bid}")

        # formatted_price_per_bid = round(price_per_bid, 2)
    except:
        print("can not access the ammountS")

    # stealth_sync(page)

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
                    print(current_url)
                    print(link)
                    print(link == current_url)
                    if 1==1:#link == current_url:

                        try:
                            # price_per_bid = 1
                            time.sleep(3)
                            print(f'result = {result} {result == 1}')

                            if result in [1, 'X', 2]:
                                print(f"result in {[1, 'X', 2]}")
                                click_result1x2(page, result)
                            elif result in ['Over 0.5', 'Over 1.5', 'Under 3.5', 'Under 4.5']:
                                print(f"result in {['Over 0.5', 'Over 1.5', 'Under 3.5', 'Under 4.5']}")
                                click_resultOverUnder(link, page, result)
                            else:
                                print("Invalid result provided")

                            # if result == 1:
                            #     page.click('div[data-marketid="1871839742"] span.s-name:text("1")')

                            # Ensure result is valid (1, X, or 2)
                            # if result == 1 or result == 'X' or result == 2:
                            #     # Map result to the correct text in the selector
                            #     choice_text = str(result)  # '1' for Home, 'X' for Draw, '2' for Away
                            #
                            #     # Try to find and click the element with data-marketid="1871839742"
                            #     market1_selector = f'div[data-marketid="1871839742"] span.s-name:text("{choice_text}")'
                            #     market1 = page.query_selector(market1_selector)
                            #
                            #     if market1:
                            #         market1.click()
                            #         print(f'Clicked on market 1871839742 for choice {choice_text}')
                            #     else:
                            #         # If not found, click the element with data-marketid="1854376134"
                            #         market2_selector = f'div[data-marketid="1854376134"] span.s-name:text("{choice_text}")'
                            #         market2 = page.query_selector(market2_selector)
                            #
                            #         if market2:
                            #             market2.click()
                            #             print(f'Clicked on market 1854376134 for choice {choice_text}')
                            #         else:
                            #             print("Neither market found")
                            # else:
                            #     print("Invalid result provided")

                            # if result == 1 or result == 'X' or result == 2:
                            #     # Try to find and click the element with data-marketid="1871839742"
                            #     market1 = page.query_selector('div[data-marketid="1871839742"] span.s-name:text("1")')
                            #
                            #     if market1:
                            #         market1.click()
                            #         print("Clicked on market 1871839742")
                            #     else:
                            #         # If not found, click the element with data-marketid="1854376134"
                            #         market2 = page.query_selector(
                            #             'div[data-marketid="1854376134"] span.s-name:text("1")')
                            #
                            #         if market2:
                            #             market2.click()
                            #             print("Clicked on market 1854376134")
                            #         else:
                            #             print("Neither market found")

                            # main_section = page.locator(".markets.markets--live.tw-mx-n.tw-mb-m")
                            # element = main_section.locator(f'text="{result}"')
                            # print(element)
                            # element.wait_for(state="visible", timeout=20000)  # Wait until the element is visible
                            # element.click()
                            print(f"Result:{result} Press")
                            human_like_delay(2, 3)

                            # Enter price
                            # input = page.query_selector("input[class='stake-input GTM-stakeInput']")
                            # input.click()
                            # time.sleep(0.5)
                            # input.fill(f"{price_per_bid}")
                            # print(f"Price:{price_per_bid} Enter")
                            # time.sleep(2)
                            #
                            # # bet button
                            # bet_button = page.query_selector(
                            #     ".tw-flex.tw-justify-center.tw-transition-transform.tw-duration-slow.tw-ease-out-back.tw-translate-y-0")
                            # bet_button.click()
                            human_like_delay(5, 7)
                            print("Bet Done")
                        except Exception as e:
                            print("Except 2")
                            print(f"Error: {e}")
                            print("")
                            pass
                    else:
                        print("game is already finished")
                        pass

                except Exception as e:
                    print("Except 1")
                    print(f"Error: {e}")
                    print("")
                    pass
    # Enter price
    # input = page.query_selector("input[class='stake-input GTM-stakeInput']")
    input = page.query_selector('div.accumulator__stake input.stake-input')
    input.click()
    time.sleep(0.5)
    input.fill(f"{price_per_bid}")
    print(f"Price:{price_per_bid} Enter")
    time.sleep(20)
    #
    # # bet button
    # bet_button = page.query_selector(
    #     ".tw-flex.tw-justify-center.tw-transition-transform.tw-duration-slow.tw-ease-out-back.tw-translate-y-0")
    # bet_button.click()

    page.close()
    browser.close()




