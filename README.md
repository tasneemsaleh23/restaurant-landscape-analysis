# 🍽️ Restaurant Landscape Analysis — 6th of October City, Egypt

A data cleaning and analysis project that turns a raw, messy Google Maps scrape into a structured, queryable dataset and an interactive dashboard covering food-serving businesses in 6th of October City, Egypt.

## Problem

Raw Google Maps scrapes are wide, messy, and inconsistent. This project's source file had 480 columns (mostly empty, from flattened nested JSON), city names spelled 5 different ways for the same place, and irrelevant business types (grocery stores, a poultry farm) mixed in because of a broad search term. None of it was usable for analysis without deliberate, justified cleaning first.

## Solution

A layered pipeline (raw → cleaned → analytics) that:
- Projects the raw 480 columns down to ~30 meaningful fields
- Filters to food-serving categories only, with documented exclusions
- Handles missing values with a **different, justified strategy per field type** — not one blanket rule (see below)
- Standardizes city names into a new `city_clean` column, without ever overwriting the raw source data
- Enforces deduplication at the database level via a `place_id` primary key
- Surfaces data-quality findings transparently, in the dashboard itself, instead of hiding them

## Input

Apify **Google Places Crawler** output — 150 businesses scraped from three overlapping search terms (`restaurant`, `مطعم`, `food`) centered on 6th of October City, Egypt. `scrapePlaceDetailPage` was `false`, so only search-result-level fields were collected (no price tier, hours, or menu data).

## Processing

| Step | What happens |
|---|---|
| Column selection | 480 → ~30 columns with actual data |
| Category filtering | 150 → 138 rows (excluded grocery stores, supermarkets, a poultry farm, etc.) |
| Missing values | 3 distinct strategies: zero-fill for review counts, explicit `'Not provided'`/`'Unknown'` labels for sparse text/status fields, and a boolean flag (`is_rated`) instead of a guessed rating |
| City standardization | 5 raw spelling variants mapped to one canonical value in a new `city_clean` column |
| Deduplication | `place_id` (Google's own unique ID) enforced as a database primary key |
| Storage | SQLite (`restaurants.db`), plus CSV/Parquet exports |

## Output

- A clean dataset: `data/cleaned/restaurants_clean.csv` / `.parquet`
- A queryable SQLite database: `data/analytics/restaurants.db`
- An interactive Streamlit dashboard (`app/app.py`) with filters, KPIs, a map, and a top-reviewed table

## Key findings

- 138 of 150 scraped listings were genuinely food-serving businesses
- 16 of 138 (11.6%) had no Google reviews at all — labeled `Unrated`, not dropped
- 65 of 138 (47%) had no neighborhood listed on Google Maps
- One business appeared twice under different `place_id`s — confirmed via address and coordinates to be two real branches, not a scrape duplicate, and both were kept

## Who benefits

Anyone scouting the area for a new restaurant location, a food-delivery ops analyst prioritizing which businesses to onboard, or anyone wanting a worked example of cleaning real, messy scraped data end-to-end.

## Tech stack

Python · Pandas · SQLite · SQL · Streamlit · Plotly

## Architecture

```
Apify raw export (480 cols, 150 rows)
   → Column projection (~30 useful cols)
   → Category filtering (food-serving only, 138 rows)
   → Missing-value handling (3 distinct strategies by field type)
   → Non-destructive text standardization (city_clean)
   → Deduplication (place_id PRIMARY KEY)
   → SQLite (data/analytics/restaurants.db)
   → SQL analysis (rating distribution, top-reviewed, category breakdown)
   → Streamlit dashboard
```

## Project structure

```
restaurant_project/
├── notebooks/
│   └── restaurant_cleaning.ipynb   # full cleaning + analysis walkthrough
├── app/
│   └── app.py                      # Streamlit dashboard
├── data/
│   ├── raw/restaurants_raw.xlsx
│   ├── cleaned/restaurants_clean.csv
│   ├── cleaned/restaurants_clean.parquet
│   └── analytics/restaurants.db
├── sql/
│   └── schema.sql
└── README.md
```

## How to run

```bash
pip install streamlit pandas
streamlit run app/app.py
```

Opens at `http://localhost:8501`. The dashboard reads directly from `data/analytics/restaurants.db`, so that file must exist at the path above relative to where you run the command.

## What I learned

- How to reason about *why* a value is missing before deciding how to handle it — not every `NaN` means the same thing
- That flattened scraper JSON needs deliberate column selection, not blind cleaning
- How a database `PRIMARY KEY` constraint formalizes a business rule that a pandas script alone can only assume is true
- The practical gap between exploratory notebook work and a reusable, runnable script

## Possible future improvements

- Re-scrape with `scrapePlaceDetailPage: true` to capture price tier and opening hours
- Expand to multiple cities to make `city_clean` genuinely load-bearing
- Add review-text sentiment analysis if a future scrape captures review content
