from concurrent.futures import ThreadPoolExecutor, as_completed
from playwright.sync_api import sync_playwright
import pandas as pd
import requests
import time

API_KEY = "your_2captcha_api_key"
sitekey = "6LfhGqoUAAAAABwg4jK9YFUL4BSXQxUJDs6c0FiU"
URL = "https://secure.theworknumber.talx.com/twneeer/PreAuthenticated/FindEmployer.aspx?ReturnUrl=%2ftwneeer%2f"

# Store results
results = []

def solve_recaptcha(site_key, url):
    response = requests.post("http://2captcha.com/in.php", data={
        "key": API_KEY,
        "method": "userrecaptcha",
        "googlekey": site_key,
        "pageurl": url,
        "json": 1
    })
    request_id = response.json().get("request")
    for _ in range(20):
        time.sleep(5)
        result = requests.get(
            f"http://2captcha.com/res.php?key={API_KEY}&action=get&id={request_id}&json=1"
        ).json()
        if result.get("status") == 1:
            return result.get("request")
    return None

def parse_employer_address(raw_address):
    try:
        lines = raw_address.strip().split("\n")
        street = lines[0].strip()
        city_state = postal_code = ""
        if len(lines) > 1 and "," in lines[1]:
            city_state, postal_code = lines[1].split(",", 1)
        return {
            "street": street,
            "city_state": city_state.strip(),
            "postal_code": postal_code.strip()
        }
    except:
        return {"street": "", "city_state": "", "postal_code": ""}

def process_employee_id(id):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL)

        page.fill("#txtEmployer", id)
        token = solve_recaptcha(sitekey, URL)

        if token:
            page.evaluate("""(token) => {
                document.getElementById("g-recaptcha-response").style.display = 'block';
                document.getElementById("g-recaptcha-response").value = token;
            }""", token)
            page.evaluate("document.getElementById('g-recaptcha-response').dispatchEvent(new Event('change'))")
            time.sleep(3)
            page.click("#lnkbtnSearch")
            try:
                page.wait_for_selector("td[class='employerName']", timeout=60000)
            except:
                browser.close()
                return None

            name = page.query_selector("td[class='employerName']")
            code = page.query_selector("td[class='employerCode']")
            addr = page.query_selector("td[class='employerAddress']")
            browser.close()

            address_parts = parse_employer_address(addr.inner_text() if addr else "")

            return {
                "employee_id": id,
                "employer_name": name.inner_text() if name else "",
                "employer_code": code.inner_text() if code else "",
                "street": address_parts["street"],
                "city_state": address_parts["city_state"],
                "postal_code": address_parts["postal_code"]
            }

        browser.close()
        return None

# Run in parallel
employee_ids = ["10108", "10006", "10020", "10026", "10101", "10105",
"10110",
"10119",
"10120",
"10123"]

with ThreadPoolExecutor(max_workers=3) as executor:
    future_to_id = {executor.submit(process_employee_id, emp_id): emp_id for emp_id in employee_ids}
    for future in as_completed(future_to_id):
        result = future.result()
        if result:
            results.append(result)

# Save to Excel
df = pd.DataFrame(results)
df.to_excel("employer_data_parallel.xlsx", index=False)
print("[✅] Data saved to employer_data_parallel.xlsx")
