from playwright.sync_api import sync_playwright
import requests
import time

API_KEY = "6d93b13a2ea92ffa70d1b683f9d83247"  # Your 2Captcha API Key

def solve_recaptcha(site_key, url):
    print("[INFO] Sending request to 2Captcha...")
    response = requests.post("http://2captcha.com/in.php", data={
        "key": API_KEY,
        "method": "userrecaptcha",
        "googlekey": site_key,
        "pageurl": url,
        "json": 1
    })

    request_id = response.json().get("request")
    if not request_id:
        print("[ERROR] 2Captcha request failed:", response.text)
        return None

    print(f"[INFO] Request ID: {request_id}, waiting for solution...")
    for _ in range(20):
        time.sleep(5)
        result = requests.get(
            f"http://2captcha.com/res.php?key={API_KEY}&action=get&id={request_id}&json=1"
        ).json()

        if result.get("status") == 1:
            print("[INFO] Captcha solved.")
            return result.get("request")
        elif result.get("request") != "CAPCHA_NOT_READY":
            print("[ERROR] Failed:", result)
            return None
    return None

def parse_employer_address(raw_address):
    try:
        lines = raw_address.strip().split("\n")
        street = lines[0].strip()

        if len(lines) > 1:
            city_state_zip = lines[1].strip()
            if "," in city_state_zip:
                city_state, postal_code = city_state_zip.split(",", 1)
                city_state = city_state.strip()
                postal_code = postal_code.strip()
                return {
                    "street": street,
                    "city_state": city_state,
                    "postal_code": postal_code
                }
        # fallback in case format is unexpected
        return {
            "street": street,
            "city_state": "",
            "postal_code": ""
        }
    except Exception as e:
        print(f"[ERROR] Failed to parse address: {e}")
        return {
            "street": "",
            "city_state": "",
            "postal_code": ""
        }


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    # page = browser.new_page()
    # url = "https://secure.theworknumber.talx.com/twneeer/PreAuthenticated/FindEmployer.aspx?ReturnUrl=%2ftwneeer%2f"
    # page.goto(url)

    sitekey = "6LfhGqoUAAAAABwg4jK9YFUL4BSXQxUJDs6c0FiU"  # Replace if it changes

    employee_ids = ["10108", "10006", "10020", "10026", "10101"]

    for id in employee_ids[0:3]:
        page = browser.new_page()
        url = "https://secure.theworknumber.talx.com/twneeer/PreAuthenticated/FindEmployer.aspx?ReturnUrl=%2ftwneeer%2f"
        page.goto(url)
        input_field = page.query_selector("#txtEmployer")
        if input_field:
            input_field.click()
            input_field.fill(id)
            time.sleep(2)

        # Solve CAPTCHA before each search
        token = solve_recaptcha(sitekey, url)

        if token:
            # Inject token into g-recaptcha-response
            page.evaluate("""(token) => {
                document.getElementById("g-recaptcha-response").style.display = 'block';
                document.getElementById("g-recaptcha-response").value = token;
            }""", token)
            page.evaluate("document.getElementById('g-recaptcha-response').dispatchEvent(new Event('change'))")
            time.sleep(3)

            search_button = page.query_selector("#lnkbtnSearch")
            if search_button:
                search_button.click()
                print(f"[INFO] Searched for employer ID: {id}")
            else:
                print(f"[WARN] Search button not found for ID: {id}")
        else:
            print(f"[ERROR] CAPTCHA solve failed for ID: {id}")

        
        page.wait_for_selector("td[class='employerName']", timeout=60000)
        employer_name_ele = page.query_selector("td[class='employerName']")
        if employer_name_ele:
            employer_name = employer_name_ele.inner_text()
        else:
            employer_name = ""
            
        employerCode_ele = page.query_selector("td[class='employerCode']")
        if employerCode_ele:
            employerCode = employerCode_ele.inner_text()
        else:
            employerCode = ""
            
        employer_address_ele = page.query_selector("td[class='employerAddress']")
        if employer_address_ele:
            employer_address = employer_address_ele.inner_text()
            address_parts = parse_employer_address(employer_address)
            print("Street:", address_parts["street"])
            print("City + State:", address_parts["city_state"])
            print("Postal Code:", address_parts["postal_code"])
        
        time.sleep(5)  # Optional delay between iterations

        page.close()
    browser.close()
