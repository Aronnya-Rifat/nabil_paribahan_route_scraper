## Nabil Paribahan Web Scraper

This project is a Python-based automated scraper that extracts all available bus routes and trip details from the Nabil Paribahan website. The scraper uses Selenium to handle dynamic content such as modals, dropdowns, and Next Day schedules, and uses the Requests + lxml libraries to collect route links from the homepage.

## Overview

The scraper performs the following tasks:

1. Collects all route URLs from the homepage.
2. Loads each route page and extracts all available trip data.
3. Detects when no trips are available and clicks the "Next Day" button to load the next day’s schedule.
4. Opens boarding point and dropping point modals and extracts all available points.
5. Saves all scraped data into JSON format.
6. Creates a checkpoint file after each route so data is never lost.

## Features

* Full route extraction
* Trip details collection (operator, bus type, coach, fare)
* Boarding point extraction from modal
* Dropping point extraction from modal
* Automatic retry for page load failures
* Works with dynamic JavaScript-loaded elements
* Creates two output files:

  * nabil_trips.json         Final dataset
  * nabil_checkpoint.json    Automatic backup after each route

## Installation

1. Install dependencies using:

   pip install -r requirements.txt

2. Install Google Chrome.

3. Download ChromeDriver matching your Chrome version from:
   [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)

4. Place ChromeDriver either:

   * In the same folder as main.py, or
   * Added to system PATH

## Usage

Run the scraper using:

python main.py

When the scraper finishes, your final data will be saved in:

nabil_trips.json

A checkpoint file is also saved after each route:

nabil_checkpoint.json

## Output Format

The output is a JSON list of objects. Each object contains:

* URL
* Operator
* Bus Type
* Route
* Coach Number
* Starting Point
* Ending Point
* Fare
* Boarding Points (list)
* Dropping Points (list)

Example:

{
"URL": "https://www.nabilparibahan.com/booking/bus/search?fromcity=dhaka&tocity=panchagarh
",
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

## Project Structure

main.py
README
requirements.txt
nabil_checkpoint.json   (generated)
nabil_trips.json        (generated)

## Notes

* The scraper includes retries if a page fails to load.
* Boarding and dropping points are extracted from modals that require interaction.
* Clicking “Next Day” ensures the scraper continues even when no same-day trips exist.

## Disclaimer

This project is for educational and research purposes. Scraping websites may violate terms of service. Use responsibly.



Just tell me — I can rewrite it in any style you want.
