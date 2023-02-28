# reform_dash_scraper

This repo collects data from various webpages through cron jobs (via GitHub Actions). The frequency of the trigger depends on the data source, but will not make commits unless a change is detected.


### Data Sources

- [ ] [Vehicle reports (traffic stops)](https://nyc.gov/site/nypd/stats/reports-analysis/vehicle-stop-reports.page)
 + Triggered: first of every month at 11am UTC
 + Output: /results/vehicle_stops.csv 
 + Parser params:
   - metric = 'vehicle_stops'
   - html_doc = 'https://raw.githubusercontent.com/gh-islg/reform_dash_scraper/main/vehicle_stops.html'
 
 - [ ] [Domestic violence reports](https://www.nyc.gov/site/nypd/stats/reports-analysis/domestic-violence.page)
 + Triggered: first of every month at 11am UTC
 + Output: /results/domestic_violence.csv
 + Parser params:
   - metric = 'domestic_violence'
   - html_doc = 'https://raw.githubusercontent.com/gh-islg/reform_dash_scraper/main/domestic_violence.html'
  
 - [ ] [SQF reports](https://www.nyc.gov/site/nypd/stats/reports-analysis/stopfrisk.page)
 + Triggered: first of every month at 11am UTC
 + Output: /results/sqf.csv
 + Parser params:
   - metric = 'sqf'
   - html_doc = 'https://raw.githubusercontent.com/gh-islg/reform_dash_scraper/main/sqf.html'

