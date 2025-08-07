from playwright.sync_api import sync_playwright
import time
import pandas as pd

link = "https://www.americanstandard-us.com/pages/where-to-buy?srsltid=AfmBOooygAas_lhUzJZLUBFrfHCkqCQpsanqUV0I6j-qe3h_WkEtLK-s"

excel_data = pd.read_excel("Copy of uscities.xlsx")


def extract_data(page, categories, input_city):
    page.wait_for_selector("#__ps-local-sellers_0", state="visible", timeout=60000)
    ul_element  = page.query_selector("#__ps-local-sellers_0")
    li_elements =  ul_element.query_selector_all(".ps-local-store-container")
    for li in li_elements:
        
        # title
        title_element = li.query_selector("small")
        if title_element:
            title = title_element.inner_text()
        else:
            title = ""
        
        # address
        try:
            address_element = li.query_selector(".ps-address div div")
            raw_address = address_element.inner_text().strip()
            lines = raw_address.split("\n")

            # Defensive check
            if len(lines) >= 2:
                street_address = lines[0].strip()
                city_state_zip = lines[1].strip()

                # Split city from state/zip using the comma
                city, rest = city_state_zip.split(",", 1)
                city = city.strip()

                # Split rest by space to separate state and postal code
                state_zip_parts = rest.strip().split(" ")
                state = state_zip_parts[0]
                postal_code = " ".join(state_zip_parts[1:])  # in case ZIP has spaces (like Canadian codes)

                print("Street:", street_address)
                print("City:", city)
                print("State:", state)
                print("Postal Code:", postal_code)
            else:
                print("⚠️ Unexpected address format")
        except:
            street_address, city, state, postal_code = "", "", "", ""
            
        # phone number
        phone_element = li.query_selector("div[class='ps-address'] div span")
        if phone_element:
            phone = phone_element.inner_text()
        else:
            phone = ""
            
        # categories, input_city
        print(categories)
        print(input_city)
        
    return title, street_address, city, state, postal_code, phone, input_city, categories





with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    page.goto(link, timeout=60000)
    page.wait_for_load_state("load")
    
    for index, row in excel_data.iterrows():
        input_field = page.query_selector("#__ps-map-location-textbox_0")
        input_field.click()
        input_field.press("Control+A")
        input_field.press("Backspace")
        input_field.fill(row["city"])
        
        page.query_selector("span[aria-label='Search for this product by city or zip code.']").click()
        
        showroom_button = page.query_selector("label[for='__ps-store-type-Showroom_0']")
        wholesale_button = page.query_selector("label[for='__ps-store-type-Wholesale_0']")
        Retail_button = page.query_selector("label[for='__ps-store-type-Retail_0']")
        
        showroom_button.click()
        time.sleep(5)
        extract_data(page, "showroom" , row["city"])
        
        wholesale_button.click()
        time.sleep(5)
        extract_data(page, "wholesale", row["city"])
        
        Retail_button.click()
        time.sleep(5)
        extract_data(page, "Retail", row["city"])
        
    page.close()
    browser.close() 
    
    



