from playwright.sync_api import sync_playwright
import time

# Your ZenRows API key
ZENROWS_API_KEY = "0ee4d69c721435140dfd68d46112f4b58b90f91d"
PROXY_URL = f"http://{ZENROWS_API_KEY}:@superproxy.zenrows.com:1337"
http://rH5q5ns7fghx:Bp9V1JiHHAuE@superproxy.zenrows.com:1337
# List of URLs to scrape
URL_list = [
    "https://vancouver.craigslist.org/van/sks/d/port-coquitlam-south-furnace-fireplace/7805985588.html",
    "https://vancouver.craigslist.org/van/sks/d/vancouver-professional-tile/7805985079.html",
    "https://vancouver.craigslist.org/rds/sks/d/surrey-electrician-service-calls-and/7805975816.html",
    "https://vancouver.craigslist.org/rds/sks/d/surrey-lower-west-electrician-no-job-is/7805973890.html",
    "https://vancouver.craigslist.org/nvn/sks/d/north-vancouver-exterior-interior/7805970588.html",
    "https://vancouver.craigslist.org/bnc/sks/d/burnaby-electrician-available/7805966931.html",
    "https://vancouver.craigslist.org/nvn/sks/d/sechelt-tile-installers-flooring/7805950769.html",
    "https://vancouver.craigslist.org/nvn/sks/d/coquitlam-tile-installers-flooring/7805950546.html",
    "https://vancouver.craigslist.org/nvn/sks/d/coquitlam-tile-installers-flooring/7805950230.html"
]

with sync_playwright() as p:
    # Launch browser with ZenRows proxy
    browser = p.chromium.launch(headless=False, proxy={"server": PROXY_URL})
    page = browser.new_page()

    for link in URL_list:
        try:
            print(f"Processing: {link}")
            page.goto(link)
            time.sleep(5)

            # Locate and click the reply button
            reply_button = page.query_selector("button[role='button']")
            if reply_button:
                reply_button.click()
                print("Reply button clicked.")
                time.sleep(30)
            else:
                print("Reply button not found.")

        except Exception as e:
            print(f"Error processing {link}: {e}")

    # Close browser
    page.close()
    browser.close()
