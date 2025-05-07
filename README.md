# BetterSeatFinder

**BetterSeatFinder** is a web-based visualsation tool for displaying average seat availability across different UoB locations during exam season, helping users find study spaces with the most free seats.

**View the site:** [renn.ie/betterSeatFinder](https://renn.ie/betterSeatFinder)

---

## Features

- Visualises average seat availability per location for **each hour of the current day**
- The **current hour** is clearly highlighted
- Automatically updates based on your system clock

---

## Files
 - seat_scraper.py - Scrapes the seats from the websites and updates the CSV of all data
 - graph_plotter.py - Plots graphs as PNGs. Use flag `--last-two-weeks` to only plot from the last two weeks of data
 - json_producer.py - Generates a json file of averaged data by hour for each location
 - index.html - the live website (other website folders contain older version)
 - other folders contains the png plots of the data
 - workflows folder contains all the workflows that were used to scrape the original data used
