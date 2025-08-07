from playwright.sync_api import sync_playwright
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from pathlib import Path

# Load city list
excel_data = pd.read_excel("Copy of uscities.xlsx")

# Output Excel file
output_file = "output.xlsx"
output_columns = ["Input City", "City", "Title", "Street Address", "State", "Postal Code", "Phone", "Store Type"]

# Create the Excel file with columns if it doesn't exist
if not Path(output_file).exists():
    pd.DataFrame(columns=output_columns).to_excel(output_file, index=False)

# Thread lock for writing
write_lock = Lock()

def append_to_excel(row):
    with write_lock:
        df = pd.read_excel(output_file, engine="openpyxl")
        df = df._append(row, ignore_index=True)
        df.to_excel(output_file, index=False, engine="openpyxl")

def process_city(input_city):
    link = "https://www.americanstandard-us.com/pages/where-to-buy?"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(link, timeout=60000)
        page.wait_for_load_state("load")

        try:
            page.wait_for_selector("#__ps-map-location-textbox_0", state="visible", timeout=60000)
            input_field = page.query_selector("#__ps-map-location-textbox_0")
            input_field.click()
            input_field.press("Control+A")
            input_field.press("Backspace")
            time.sleep(1)
            input_field.type(input_city, delay=100)
            page.query_selector("span[aria-label='Search for this product by city or zip code.']").click()
            time.sleep(3)
            print(f"enter input [{input_city}]")

            for store_type, button_selector in [
                ("Showroom", "label[for='__ps-store-type-Showroom_0']"),
                ("Wholesale", "label[for='__ps-store-type-Wholesale_0']"),
                ("Retail", "label[for='__ps-store-type-Retail_0']")
            ]:
                try:
                    page.wait_for_selector(".ps-local-sellers", state="visible", timeout=60000)
                    button = page.query_selector(button_selector)
                    if button:
                        button.click()
                        time.sleep(5)
                        page.wait_for_selector(".ps-local-sellers", state="visible", timeout=60000)
                        ul_element = page.query_selector("#__ps-local-sellers_0")
                        if not ul_element:
                            print(f"No {store_type} stores found in {input_city}")
                            continue
                        li_elements = ul_element.query_selector_all(".ps-local-store-container")

                        for li in li_elements:
                            # Title
                            title_element = li.query_selector("small")
                            title = title_element.inner_text().strip() if title_element else ""

                            # Address parsing
                            try:
                                address_element = li.query_selector(".ps-address div div")
                                raw_address = address_element.inner_text().strip()
                                lines = raw_address.split("\n")

                                if len(lines) >= 2:
                                    street_address = lines[0].strip()
                                    city_state_zip = lines[1].strip()

                                    extracted_city, rest = city_state_zip.split(",", 1)
                                    state_zip_parts = rest.strip().split(" ")
                                    state = state_zip_parts[0]
                                    postal_code = " ".join(state_zip_parts[1:])
                                else:
                                    street_address = extracted_city = state = postal_code = ""
                            except:
                                street_address = raw_address
                                extracted_city = state = postal_code = ""

                            # Phone
                            phone_element = li.query_selector("div[class='ps-address'] div span")
                            phone = phone_element.inner_text().strip() if phone_element else ""

                            # Append data to Excel
                            data_row = {
                                "Input City": input_city,
                                "City": extracted_city,
                                "Title": title,
                                "Street Address": street_address,
                                "State": state,
                                "Postal Code": postal_code,
                                "Phone": phone,
                                "Store Type": store_type
                            }
                            append_to_excel(data_row)
                    else:
                        print(f"{store_type} button not found for {input_city}")
                except Exception as e:
                    print(f"⚠️ Error in store type '{store_type}' for {input_city}: {e}")

        except Exception as e:
            print(f"❌ Failed for {input_city}: {e}")

        page.close()
        browser.close()


# Run cities in parallel (max 3 tabs)
with ThreadPoolExecutor(max_workers=1) as executor:
    futures = []
    for city in excel_data["city"].dropna().unique():
        futures.append(executor.submit(process_city, city))
