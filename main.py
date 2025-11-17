import time
import random
import json
import requests
from lxml import html
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def safe_get(driver, url, timeout=40, retries=3):
    for attempt in range(retries):
        try:
            driver.set_page_load_timeout(timeout)
            driver.get(url)
            return True
        except Exception as e:
            print(f"⚠ Connection error: {e} (attempt {attempt+1}/{retries})")
            time.sleep(3)

    print("❌ Failed to load after several retries.")
    return False
# ------------------------------------------------------------
# 1️⃣ FUNCTION: Scrape all route links from homepage
# ------------------------------------------------------------
def get_route_links(home_url="https://www.nabilparibahan.com/"):
    response = requests.get(home_url, timeout=10)
    response.raise_for_status()

    tree = html.fromstring(response.content)
    elements = tree.xpath('//*[@id="routes_sec"]/div/ul/li')

    routes = []
    for el in elements:
        text = el.text_content().strip()
        link = el.xpath('.//a/@href')
        full_link = urljoin(home_url, link[0]) if link else None
        if full_link:
            routes.append({"route_name": text, "url": full_link})

    return routes


# ------------------------------------------------------------
# 2️⃣ FUNCTION: Scrape a SINGLE route page (with Next Day & Boarding Points)
# ------------------------------------------------------------
def scrape_route_page(url):
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

    driver = webdriver.Chrome(options=chrome_options)
    if not safe_get(driver, url):
        driver.quit()
        return []

    wait = WebDriverWait(driver, 20)

    def load_trip_rows():
        """Try to load trips; if none, return empty list."""
        try:
            return driver.find_elements(By.CSS_SELECTOR, "tr[data-trip]")
        except:
            return []

    time.sleep(random.uniform(3, 5))
    rows = load_trip_rows()

    # -------------------------------
    # 🔁 If no trips → click " Next Day "
    # -------------------------------
    if len(rows) == 0:
        print("⚠ No trips found → Clicking ' Next Day '")

        try:
            next_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Next Day'] | //a[normalize-space()='Next Day'] | //button[contains(text(), 'Next Day')]"))
            )
        except:
            print("❌ ' Next Day ' button not found — giving up for this route.")
            driver.quit()
            return []

        next_btn.click()
        time.sleep(random.uniform(3, 5))

        rows = load_trip_rows()

    # When trips appear, scroll
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.uniform(2, 4))

    results = []

    for row in rows:

        # -------------------------------
        # Basic trip fields
        # -------------------------------
        try:
            operator = row.find_element(By.CLASS_NAME, "op_name").text.strip()
        except:
            operator = None

        try:
            bus_type = row.find_element(By.CLASS_NAME, "bus_type").text.strip()
            bus_type = bus_type.split("Coach")[0].strip().rstrip(":")
        except:
            bus_type = None

        try:
            coach = row.find_element(By.CLASS_NAME, "trip_num").text.strip()
            coach = coach.split(":")[1].strip()
        except:
            coach = None

        try:
            fare = row.find_element(By.CLASS_NAME, "fare-list").text.strip()
        except:
            fare = None

        # Route, Starting, Ending
        text_block = row.text.split("\n")
        route = start_point = end_point = None

        for t in text_block:
            if "Route" in t:
                route = t.split(":", 1)[-1].strip()
            if "Starting Point" in t:
                start_point = t.split(":", 1)[-1].strip()
            if "Ending Point" in t:
                end_point = t.split(":", 1)[-1].strip()

        # -------------------------------
        # BOARDING POINTS (with 1s sleep + select click)
        # -------------------------------
        boarding_points = []

        try:
            # Button containing the exact text " View Seats "
            seats_btn = row.find_element(
                By.XPATH,
                ".//button[contains(normalize-space(.), 'View Seats')]"
            )

            # Scroll into view to avoid click interception
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", seats_btn)
            time.sleep(0.5)

            # Try clicking → fallback to JS click
            try:
                seats_btn.click()
            except:
                driver.execute_script("arguments[0].click();", seats_btn)

            # ⏳ Wait for modal animation
            time.sleep(1)

            # Wait until select exists
            select_el = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "boardingpoint"))
            )

            # 👇 Click the select tag (as you requested)
            try:
                select_el.click()
            except:
                driver.execute_script("arguments[0].click();", select_el)

            # Wait until option list fully loads
            options = WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//select[@id='boardingpoint']/option[@value!='0']")
                )
            )
            time.sleep(1)
            # Extract option text
            for op in options:
                txt = op.text.strip()
                if txt:
                    boarding_points.append(txt)

        except Exception as e:
            print("⚠ Boarding points not found:", e)
            boarding_points = []
        # -------------------------------
        # DROPPING POINTS (Corrected)
        # -------------------------------

        dropping_points = []

        try:
            # Find anchor with onclick containing 'droppingPoints'
            drop_link = row.find_element(
                By.XPATH,
                '//*[@id="tbl_offer"]/span/span[2]/span[2]/a'
            )
            time.sleep(0.5)

            # Scroll into view
            driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", drop_link
            )
            time.sleep(0.5)

            # Click → fallback to JS click
            try:
                drop_link.click()
            except:
                driver.execute_script("arguments[0].click();", drop_link)

            # Allow modal/panel to load
            time.sleep(1)

            # Wait for dropping point section
            drop_div = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "dropping_point"))
            )

            # Extract li items
            li_items = drop_div.find_elements(By.XPATH, ".//ul/li")

            for li in li_items:
                txt = li.text.strip()
                if txt:
                    dropping_points.append(txt)
            exit_link = row.find_element(By.XPATH, '//*[@id="myModal"]/div/div/div[1]/button')
            time.sleep(0.5)
            try:
                exit_link.click()
            except:
                driver.execute_script("arguments[0].click();", exit_link)
            time.sleep(0.5)
        except Exception as e:
            print("⚠ Dropping points not found:", e)
            dropping_points = []

        results.append({
            "URL": url,
            "Operator": operator,
            "Bus Type": bus_type,
            "Route": route,
            "Coach": coach,
            "Starting Point": start_point,
            "Ending Point": end_point,
            "Fare": fare,
            "Boarding Points": boarding_points,
            "Dropping Points": dropping_points
        })
        print({
            "URL": url,
            "Operator": operator,
            "Bus Type": bus_type,
            "Route": route,
            "Coach": coach,
            "Starting Point": start_point,
            "Ending Point": end_point,
            "Fare": fare,
            "Boarding Points": boarding_points,
            "Dropping Points": dropping_points
        })

    driver.quit()
    return results


# ------------------------------------------------------------
# 3️⃣ FUNCTION: Scrape ALL routes (loop)
# ------------------------------------------------------------
def scrape_all_routes():
    all_data = []
    routes = get_route_links()

    print(f"🚀 Found {len(routes)} routes.\n")

    for r in routes:
        try:
            print(f"🔍 Scraping route: {r['route_name']} → {r['url']}")
            trips = scrape_route_page(r["url"])
            all_data.extend(trips)

            # Save after each route
            with open("nabil_checkpoint.json", "w", encoding="utf-8") as f:
                json.dump(all_data, f, indent=4, ensure_ascii=False)

            print("💾 Route saved.\n")
            time.sleep(random.uniform(2, 4))

        except Exception as e:
            print(f"❌ Route failed: {r['url']} — {e}")
            continue

    return all_data


# ------------------------------------------------------------
# 4️⃣ MAIN RUN
# ------------------------------------------------------------
if __name__ == "__main__":
    final_data = scrape_all_routes()

    print("\n✅ Done! Total trips scraped:", len(final_data))

    print(json.dumps(final_data, indent=4, ensure_ascii=False))
    output_file = "nabil_trips.json"

    # Save the data
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=4, ensure_ascii=False)

    print(f"\n✅ Scraping complete! Data saved to {output_file}")