import json
from playwright.sync_api import sync_playwright
import re

# Load JSON data from file
input_file = "extracted_horse_links.json"
with open(input_file, 'r', encoding='utf-8') as f:
    input_data = json.load(f)



def id(page):
    try:
        id = page.query_selector("(//div[@class='shortInfos'])[1]")
        print(id.inner_text())
        id  = id.inner_text()
        return(id)
    except:
        return("")
    
def description(page):    
    # description
    try:
        descriptions = page.query_selector(".descriptions")
        disc = descriptions.query_selector(".selected")
        print(disc.inner_text())
        return(disc.inner_text())
    except:
        return("")
def image_link(page):
    # image_link
    try:
        img_link = page.query_selector(".swiper-wrapper")
        if img_link:
            all_images = img_link.query_selector_all(".swiper-slide")
            image_list = []
            for images in all_images:
                print(images.get_attribute('style'))
                
                # image_list.append(images.get_attribute('style'))
                url_pattern = re.compile(r'url\("([^"]+)"\)')
                match = url_pattern.search(images.get_attribute('style'))
                if match:
                    image_list.append(match.group(1))
                # return None
            
            # Extract the URL from the style attribute
            # match = re.search(r'background-image:url\((.*?)\);', style)
            # if match:
            #     image_url = match.group(1)
            #     print(image_url)
            return(image_list)
    except:
        return("")
        
    # category
    # category = page.query_selector("")
    

        

        

        

            
    


        
def price(page):
    # price
    try: 
        price = page.query_selector("body > div:nth-child(3) > div:nth-child(6) > div:nth-child(1) > div > div:nth-child(2) > div:nth-child(2) > b:nth-child(5)")
        print(price.inner_text())
        return(price.inner_text())
    except:
        return("")

def Location(page):
    
    # Location
    try:
        Location = page.query_selector(".pt3.pr80")
        print(Location.inner_text())
        return(Location.inner_text())
    except:
        return("")
def x_ray(page):
    # x_ray
    try:
        x_ray = page.query_selector("div[id='comp-l69peybg'] h2[class='font_2 wixui-rich-text__text'] span[class='wixui-rich-text__text'] span[class='wixui-rich-text__text'] span[class='color_15 wixui-rich-text__text'] span[class='wixui-rich-text__text']")
        print(x_ray.inner_text())
        return(x_ray.inner_text())
    except:
        return("")
def full_papers(page):
    # full_papers
    try:
        full_papers = page.query_selector("div[id='comp-ljmj8j7z'] h2[class='font_2 wixui-rich-text__text'] span[class='wixui-rich-text__text'] span[class='wixui-rich-text__text'] span[class='color_15 wixui-rich-text__text'] span[class='wixui-rich-text__text']")
        print(full_papers.inner_html())
        return(full_papers.inner_html())
    except:
        return("")


def Further_information(page):
    try:
        Further_Characteristics = page.query_selector(".description")
        print(Further_Characteristics.inner_text())
        return(Further_Characteristics.inner_text())
    except:
        return("")
    
    # new
def bread(page):
    # full_papers
    try:
        main_section =  page.query_selector(".moreDetails")
        all_rows =  main_section.query_selector_all(".row")
        span = all_rows[0].query_selector("span")
        print(span.inner_text())
        single_list = []
        for rows in all_rows:
            single_data = {}
            label = rows.query_selector("label")
            label_text =  label.inner_text()
            span = rows.query_selector("span")
            span_text = span.inner_text()
            single_data[label_text] = span_text
            single_list.append(single_data)
        return(single_list)
    except:
        return("")
    
def gender(page):
    # gender
    try:
        main_section =  page.query_selector(".moreDetails")
        all_rows =  main_section.query_selector_all(".row")
        span = all_rows[1].query_selector("span")
        print(span.inner_text())
        
        return(span.inner_text())
    except:
        return("")
    
def age(page):
    # age
    try:
        main_section =  page.query_selector(".moreDetails")
        all_rows =  main_section.query_selector_all(".row")
        span = all_rows[2].query_selector("span")
        print(span.inner_text())
        
        return(span.inner_text())
    except:
        return("")
    
def color(page):                    
    # color
    try:                            
        main_section =  page.query_selector(".moreDetails")
        all_rows =  main_section.query_selector_all(".row")
        span = all_rows[3].query_selector("span")
        print(span.inner_text())
        
        return(span.inner_text())
    except:
        return("")
    
def Main_discipline(page):
    try:
        main_section =  page.query_selector(".moreDetails")
        all_rows =  main_section.query_selector_all(".row")
        span = all_rows[4].query_selector("span")
        print(span.inner_text())
        
        return(span.inner_text())
    except:
        return("")
    
def Further_Characteristics(page):
    try:
        main_section =  page.query_selector(".moreDetails")
        all_rows =  main_section.query_selector_all(".row")
        span = all_rows[5].query_selector("span")
        print(span.inner_text())
        
        return(span.inner_text())
    except:
        return("")
    
# Start Playwright and open the pages
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()

    for horse in input_data["horse"]:
        page = context.new_page()
        page.goto(horse["href"], timeout=500000)

        print("NEW add")
        print(horse["href"])
        # Extract data and add it to the JSON structure
       
        horse["description"] = description(page)
        horse["horse_id"] = id(page)
        horse["image_link"] = image_link(page)
        horse["price"] = price(page)
        horse["Location"] = Location(page)
        horse["Further_information"] = Further_information(page)

        horse["Basic_Info"] = bread(page)
        # horse["gender"] = gender(page)
        # horse["age"] = age(page)
        # horse["color"] = color(page)
        # horse["Main_discipline"] = Main_discipline(page)
        # horse["Further_Characteristics"] = Further_Characteristics(page)

        
        print("")
        
        
        # break
    
        page.close()
    
    browser.close()

# Save the updated JSON data to a file
output_file = "hourse_output.json"
with open(output_file, 'w') as f:
    json.dump(input_data, f, indent=4)

# print(f"Data has been extracted and saved to {output_file}")
