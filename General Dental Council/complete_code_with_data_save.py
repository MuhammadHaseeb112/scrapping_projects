from playwright.sync_api import sync_playwright
import pandas as pd
import time

def search(page, F_name, L_name):
    print(f"\tSearching for First_name: {F_name}, Last_name: {L_name}")
    page.goto(link)

    page.wait_for_selector("#FirstName", timeout=15000)

    # fill first name
    first_name = page.query_selector("#FirstName")
    first_name.click()
    first_name.fill(str(F_name))

    # fill Last name
    last_name = page.query_selector("#Surname")
    last_name.click()
    last_name.fill(str(L_name))

    # search_button
    search_button = page.query_selector("button[type='submit']")
    search_button.click()


def extract_table_data(page):
    rows = page.query_selector_all("tbody tr")
    Rows_NO = len(rows) -1
    surname = page.query_selector("tbody tr:nth-child(2) td:nth-child(1)").inner_text()
    Forenames = page.query_selector("tbody tr:nth-child(2) td:nth-child(2)").inner_text()
    Registration_No = page.query_selector("tbody tr:nth-child(2) td:nth-child(3)").inner_text()
    Status = page.query_selector("tbody tr:nth-child(2) td:nth-child(4)").inner_text()
    Registrant_Type = page.query_selector("tbody tr:nth-child(2) td:nth-child(5)").inner_text()

    return surname, Forenames, Registration_No, Status, Registrant_Type, Rows_NO


# Load Excel
GDC_data = pd.read_excel("Missing first or last name (4).xlsx")

# Add new empty columns
GDC_data["Surname Extracted"] = ""
GDC_data["Forenames Extracted"] = ""
GDC_data["Registration No"] = ""
GDC_data["Status"] = ""
GDC_data["Registrant Type"] = ""
GDC_data["Rows_NO"] = ""

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    link = "https://olr.gdc-uk.org/SearchRegister"

    for index, row in GDC_data[0:5].iterrows():
        page = browser.new_page()
        F_name = row['First Name']
        L_name = row['Last Name']
        print(f"Searching Row {index} \n\tExtract data for First_name: {F_name}, Last_name: {L_name}")

        success = False
        try:
            search(page, F_name, L_name)
            page.wait_for_selector("#search-results", timeout=5000)
            table = page.query_selector("#search-results")
            if table:
                print("\tSearch table found.")
                data = extract_table_data(page)
                success = True
        except:
            try:
                search(page, str(F_name)[0], L_name)
                page.wait_for_selector("#search-results", timeout=5000)
                table = page.query_selector("#search-results")
                if table:
                    print("\tFallback to first initial of first name.")
                    data = extract_table_data(page)
                    success = True
            except:
                try:
                    search(page, F_name, str(L_name)[0])
                    page.wait_for_selector("#search-results", timeout=5000)
                    table = page.query_selector("#search-results")
                    if table:
                        print("\tFallback to first initial of last name.")
                        data = extract_table_data(page)
                        success = True
                except:
                    print("\tAll attempts failed.")

        if success:
            GDC_data.loc[index, "Surname Extracted"] = data[0]
            GDC_data.loc[index, "Forenames Extracted"] = data[1]
            GDC_data.loc[index, "Registration No"] = data[2]
            GDC_data.loc[index, "Status"] = data[3]
            GDC_data.loc[index, "Registrant Type"] = data[4]
            GDC_data.loc[index, "Rows_NO"] = data[5]

        page.close()

    browser.close()

# Save updated data to Excel
GDC_data.to_excel("GDC_with_Extracted_Data2.xlsx", index=False)
print("✅ Data saved to 'GDC_with_Extracted_Data.xlsx'")
