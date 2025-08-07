from playwright.sync_api import sync_playwright
import json
import time
    
employee_ids = [
    "10108",
    "10006",
    "10020",
    "10026",
    "10101",
    "10105",
    "10110",
    "10119",
    "10120",
    "10123",
]


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    link = f"https://secure.theworknumber.talx.com/twneeer/PreAuthenticated/FindEmployer.aspx?ReturnUrl=%2ftwneeer%2f"

    page.goto(link)
    for id in employee_ids:
        input_field = page.query_selector("#txtEmployer")
        if input_field:
            input_field.click()
            input_field.fill(id)
        time.sleep(5)

        # slove the captcha here

        time.sleep(10)

        search_buttion = page.query_selector("#lnkbtnSearch")
        if search_buttion:
            search_buttion.click()
        
        
        
    page.close()
        
    browser.close()



6LfhGqoUAAAAABwg4jK9YFUL4BSXQxUJDs6c0FiU
'sitekey': '6LfhGqoUAAAAABwg4jK9YFUL4BSXQxUJDs6c0FiU'