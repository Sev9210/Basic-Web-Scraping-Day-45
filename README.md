# Hacker News (Y Combinator) Web Scraper
Note!: this is just a basic webscraping this will only work for static website such as "Hacker News"

A robust Python web scraper that extracts top stories from the Hacker News homepage. This project was developed as part of **Day 45 of the "100 Days of Code: The Complete Python Pro Bootcamp"**, but features a heavily modified architecture designed to handle complex HTML layouts and prevent data shifting.

## 🚀 Project Overview

The original curriculum goal for Day 45 focuses on global list extractions. However, due to the old-school HTML `<table>` architecture used by Hacker News, a standard list extraction leads to misaligned data because not every article has upvote scores or comments. 

This implementation shifts the workflow to a production-grade **Row-by-Row Extraction Strategy**, introducing structural validation and advanced CSS selectors to ensure 100% data integrity.

## 🛠️ Key Technical Features

* **Row-by-Row Strategy**: Finds the main story container (`.athing`) and uses relative sibling navigation (`.find_next_sibling('tr')`) to map the metadata row directly to its title.
* **Data Alignment Defenses**: Implements fallback default values (`0 points`, `0 comments`) if an article is brand new, keeping data perfectly aligned across columns.
* **Direct Child Selectors**: Uses `span.titleline > a` to strictly target the article link while ignoring sub-domain links.
* **Text Keyword Filtering**: Scans unstructured metadata lists for the words `'comment'` or `'discuss'` to cleanly isolate comment strings.
* **Data Normalization**: Cleans unicode artifacts like non-breaking spaces (`\xa0`) and parses strings into pure numeric integers.
* **Top 5 Filtering**: Leverages a Python `lambda` expression inside the `sorted()` function to instantly isolate the top 5 highest-voted stories.

## 📋 Scraped Data Structure

The scraper outputs a clean, structured dictionary formatted as follows:

```json
{
    "Shipping a laptop to a refugee camp in Uganda": {
        "link": "https://notesbylex.com",
        "score": 436,
        "author": "lexandstuff",
        "age": "11 hours ago",
        "comments": 157
    }
}
```

## ⚙️ Installation & Usage

1. Clone this repository to your local machine.
2. Ensure you have your virtual environment activated:
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install the required external libraries:
   ```bash
   pip install beautifulsoup4 requests
   ```
4. Run the scraper script:
   ```bash
   python main.py
   ```

## 💡 Lessons Learned

* **The Inspect vs. Raw Text Trap**: Learned that browser developer tools display modified live HTML trees, whereas the `requests` library retrieves raw static markup.
* **Method Workflows**: Established a clear operational boundary—using `.select()` for multi-tier nested navigation paths and `.find()` for explicit, localized tag selections.
