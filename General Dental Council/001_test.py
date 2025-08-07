from playwright.sync_api import sync_playwright
import pandas as pd
import time

def search(page, F_name, L_name):
    # page = browser.new_page()
    print(f"\tSearching for First_name: {F_name}, Last_name: {L_name}")
    page.goto(link)
    
    page.wait_for_selector("#FirstName", timeout=15000)
    
    # fill first name
    first_name = page.query_selector("#FirstName")
    first_name.click()
    first_name.fill(F_name)
    
    # fill Last name
    last_name = page.query_selector("#Surname")
    last_name.click()
    last_name.fill(L_name)
    
    # search_button
    search_button = page.query_selector("button[type='submit']")
    search_button.click()
        
def extract_table_data(page):
    surname = page.query_selector("tbody tr:nth-child(2) td:nth-child(1)").inner_text()
    Forenames = page.query_selector("tbody tr:nth-child(2) td:nth-child(2)").inner_text()
    Registration_No = page.query_selector("tbody tr:nth-child(2) td:nth-child(3)").inner_text()
    Status = page.query_selector("tbody tr:nth-child(2) td:nth-child(4)").inner_text()
    Registrant_Type = page.query_selector("tbody tr:nth-child(2) td:nth-child(5)").inner_text()
        
    print(f"\tsurname: {surname}\n\tForenames: {Forenames}\n\tRegistration_No: {Registration_No}\n\tStatus: {Status}\n\tRegistrant_Type: {Registrant_Type}")
                



GDC_data = pd.read_excel("Missing GDC numbers (1).xlsx")



with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    link = f"https://olr.gdc-uk.org/SearchRegister"

    for index, row in GDC_data.iterrows():
        page = browser.new_page()
        F_name = row['First Name']
        L_name = row['Last Name']
        print(f"Searching Row {index} \n\tExtract data for First_name: {F_name}, Last_name: {L_name}")
        search(page, F_name, L_name)
        
        try:
            page.wait_for_selector("#search-results", timeout=5000)
            table = page.query_selector("#search-results")
            if table:
                print(f"\tSearch table Found for First_name: {F_name}, Last_name: {L_name}")

                extract_table_data(page)
                
        except:
            try:
                # print(f"\tExtract data for First_name: {F_name[0]}, Last_name: {L_name}")
                search(page, F_name[0], L_name)
                page.wait_for_selector("#search-results", timeout=5000)
                table = page.query_selector("#search-results")
                if table:
                    print(f"\tSearch table Found for First_name: {F_name[0]}, Last_name: {L_name}")

                    extract_table_data(page)
                
            except:
                try:
                    # print(f"\tExtract data for First_name: {F_name}, Last_name: {L_name[0]}")
                    search(page, F_name, L_name[0])
                    page.wait_for_selector("#search-results", timeout=5000)
                    table = page.query_selector("#search-results")
                    if table:
                        print(f"\tSearch table Found for First_name: {F_name[0]}, Last_name: {L_name}")

                        extract_table_data(page)
                except:
                    print("there must be some error")

        page.close()
        
    browser.close()

