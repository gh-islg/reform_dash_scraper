# reform_dash_scraper

This repo collects data from various webpages through cron jobs (via GitHub Actions). The frequency of the trigger depends on the data source, but will not make commits unless a change is detected.


### Data Sources

- [ ] [Vehicle reports (traffic stops)](https://nyc.gov/site/nypd/stats/reports-analysis/vehicle-stop-reports.page)
 + Triggered: first of every month at 11am UTC
 + Output: vehicle_stops.html
