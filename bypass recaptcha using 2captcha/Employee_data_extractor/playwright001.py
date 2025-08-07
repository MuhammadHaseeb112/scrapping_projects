from playwright.sync_api import sync_playwright
import json
import time
    

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    link = "https://pser.punjab.gov.pk/"
    page.goto(link)

    
    time.sleep(10)
    # while True:
    #     try:
    #         more_button = page.query_selector("#results_moreBtn")
    #         more_button.click()
    #         print("button press")
    #         print("")
    #         time.sleep(5)
    #     except:
    #         print("break")
    #         time.sleep(5)
    #         break
    # # print(len(links_list))
    # links_list = {}
    # cat_list = []
    # href_list =[]  
    # hourse_ads =  page.query_selector_all(".ownHorses")
    # for add in hourse_ads:
    #     single_data = {}
    #     name1 =  add.query_selector('.fwbold.fs16')
    #     name = name1.inner_text()
    #     prefix = "https://www.ehorses.com"
    #     href = name1.get_attribute('href')
    #     comp_href = prefix+href
    #     print("")
        
    #     single_data['href'] = comp_href
    #     single_data['title'] = name
    #     href_list.append(single_data)
    
    # links_list["horse"] = href_list
    
    # with open('extracted_horse_links.json', 'w', encoding='utf-8') as f:
    #     json.dump(links_list, f, ensure_ascii=False, indent=4)
     
    
    
        
    # page.close()
        
    browser.close()
        
        
# from playwright.sync_api import sync_playwright

# def run(playwright):
#     browser = playwright.chromium.launch(headless=False)
#     page = browser.new_page()

#     page.goto("https://www.ehorses.com/caballoria?page=horses&type=0")
    
#     # Wait for the popup and click the 'Accept' button
#     try:
#         page.wait_for_selector("text='Accept'", timeout=15000)
#         page.click("text='Accept'")
#         print("Cookie consent popup accepted.")
#     except Exception as e:
#         print(f"Failed to close cookie consent popup: {e}")
    
#     # Your additional code here

#     browser.close()

# with sync_playwright() as playwright:
#     run(playwright)
        




