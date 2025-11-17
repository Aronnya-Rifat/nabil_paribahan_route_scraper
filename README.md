
```markdown
# Nabil Paribahan Route & Trip Scraper

A Python-based automated scraper that extracts all bus routes and trip information from the official Nabil Paribahan website.  
The script uses Selenium and Requests to handle dynamic content, modals, dropdowns, and "Next Day" schedules that load only after interaction.

---

## Features

- Extracts all available routes from the homepage.
- Scrapes trip data including:
  - Operator  
  - Bus type  
  - Coach number  
  - Fare  
  - Starting & ending points  
  - Boarding points (from modal)  
  - Dropping points (from modal)
- Automatically clicks “Next Day” when no trips are available.
- Handles page load retries and network interruptions.
- Saves scraped data into JSON files.
- Creates a checkpoint file after each route to prevent data loss.

---

## Project Structure

```

.
├── main.py                # Main scraper
├── requirements.txt       # Dependencies
├── README.md              # Documentation
├── nabil_checkpoint.json  # Auto-saved data after each route (generated)
└── nabil_trips.json       # Final output (generated)

```

---

## Requirements

Install dependencies:

```

pip install -r requirements.txt

```

You must have:

- Python 3.8+
- Google Chrome installed
- ChromeDriver matching your Chrome version  
  Download: https://chromedriver.chromium.org/downloads

Ensure `chromedriver` is in PATH or in the same folder as `main.py`.

---

## How to Run

Simply run:

```

python main.py

```

When complete, the results are saved to:

```

nabil_trips.json

```

A checkpoint file is updated after each route:

```

nabil_checkpoint.json

````

---

## Output Format

Each trip entry looks like this:

```json
{
    "URL": "https://www.nabilparibahan.com/booking/bus/search?fromcity=dhaka&tocity=panchagarh",
    "Operator": "Nabil Paribahan",
    "Bus Type": "AC",
    "Route": "Dhaka → Panchagarh",
    "Coach": "37",
    "Starting Point": "Gabtoli",
    "Ending Point": "Panchagarh",
    "Fare": "1200",
    "Boarding Points": [
        "Gabtoli",
        "Kallyanpur",
        "Shyamoli"
    ],
    "Dropping Points": [
        "Rangpur",
        "Thakurgaon",
        "Panchagarh"
    ]
}
````

---

## Notes

* If the site fails to load, the script retries automatically.
* If no trips are found, the scraper attempts to load “Next Day” schedule.
* Boarding and dropping points are extracted from modal popups that require interaction.

---

## Disclaimer

This project is for educational and research purposes only.
Scraping websites may violate terms of service. Use responsibly.

```

