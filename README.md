🚌 Nabil Paribahan Full Route & Trip Scraper

A fully automated Python scraper that extracts all available bus routes and trip schedules from the official Nabil Paribahan website.

This script uses Selenium WebDriver + Requests + XPath/LXML parsing to collect:

✔ Route names

✔ Operator

✔ Bus type

✔ Coach / Bus number

✔ Starting & Ending points

✔ Fare

✔ Boarding points (inside modal)

✔ Dropping points (inside modal)

✔ “Next Day” trips when same-day schedule is empty

✔ Auto-retry for failed loads

✔ JSON output saved automatically

📌 Features
🚀 Route Crawling

Scrapes all routes listed on the homepage using lxml XPath parsing.

🔁 Trip Scraping

For each route:

Loads dynamic table rows

Scrolls automatically

Detects when no trips are available

Clicks Next Day automatically

Extracts structured trip info

🎫 Boarding & Dropping Points (Modal Handling)

Opens seat modal → selects dropdown → extracts all boarding points.
Handles dropping points modal → extracts all list items → closes modal automatically.

💾 Auto Save

After each route, data is saved to:

nabil_checkpoint.json
nabil_trips.json


You never lose progress even if a crash occurs.

🖥 Requirements

Install dependencies:

pip install -r requirements.txt


Make sure you have:

Python 3.8+

Google Chrome

ChromeDriver matching your Chrome version
Download: https://chromedriver.chromium.org/downloads

▶️ How to Run

Simply run:

python main.py


Output will be saved as:

nabil_trips.json


Each entry follows this structure:

{
    "URL": "...",
    "Operator": "Nabil Paribahan",
    "Bus Type": "AC",
    "Route": "Dhaka → Panchagarh",
    "Coach": "37",
    "Starting Point": "Gabtoli",
    "Ending Point": "Panchagarh",
    "Fare": "1200",
    "Boarding Points": ["Gabtoli", "Kallyanpur", "Shyamoli"],
    "Dropping Points": ["Birganj", "Rangpur", "Thakurgaon"]
}

📁 Project Structure
├── main.py                 # The full scraping logic
├── README.md               # Documentation
├── requirements.txt        # Dependencies
├── nabil_checkpoint.json   # Auto-saved interim data (after each route)
└── nabil_trips.json        # Final output

⚠️ Disclaimer

This tool is intended for educational and research purposes only.
Scraping websites without permission may violate terms of service.
Use responsibly.
