#!/usr/bin/env reform
#%%
from bs4 import BeautifulSoup
import requests
import argparse
import git 
import pandas as pd
import re
#%%
def get_commit_history(data_path):
    '''
    Get the latest commit diff of a file.
    '''
    repo = git.Repo()
    commits = list(repo.iter_commits(paths=data_path))
    latest_commits = commits[-2:]
    diffs = repo.git.diff(latest_commits[0], latest_commits[1], data_path)
    return diffs

def return_metric_params(metric):
    '''
    Storing paths to the html documents and url links for each metric.
    '''
    gh_url = 'https://raw.githubusercontent.com/gh-islg/reform_dash_scraper/main/'
    if metric == 'homicides':
        html_doc = f'{gh_url}homicides.html'
        link_url = 'assets/nypd/downloads/excel/analysis_and_planning/supplementary-homicide/'
    elif metric == 'vehicle_stops':
        html_doc =  f'{gh_url}vehicle_stops.html'
        link_url = 'assets/nypd/downloads/excel/analysis_and_planning/vehcile-encounter-reports/' 
    elif metric == 'domestic_violence':
        html_doc =  f'{gh_url}domestic_violence.html'
    elif metric == 'sqf':
        html_doc =  f'{gh_url}sqf.html'
        # 2015-2021 (pre 2015 are zip files)
        link_url =  "/assets/nypd/downloads/excel/analysis_and_planning/stop-question-frisk/"
    return [html_doc, link_url]

def get_links_from_html(html_doc, init = True):
    '''
    If we're initializing for the first times, get all links from a html document.
    Otherwise, get the links from the diff of the latest commit.
    '''
    if init == True:
        html = requests.get(html_doc).text
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a')
    else:
        data_path = re.findall('main/(.*)$', html_doc)[0]
        diffs = get_commit_history(data_path)
        # print diffs just in case
        print(diffs)
        soup = BeautifulSoup(diffs, 'html.parser')
        links = soup.find_all('a')
    return links

def search_links(metric, link_url, html_links):
    '''
    Search across all links on page for the relevant link depending on metric.
    '''
    urls, texts = [], []
    for link in html_links:
        try:
            url = link.get('href')
            if link_url in url:
                urls.append(url)
                texts.append(link.get_text())
                print(url)
        except:
            pass
    results = {
        'metric': metric,
        'url': [f"https://nyc.gov{i}" for i in urls],
        'text': texts
    }
    return results

def get_specific_links(metric, init = True):
    '''
    Get the links depending on the metric.
    '''
    metric_params = return_metric_params(metric = metric)
    html_doc = metric_params[0]
    link_url = metric_params[1]

    if init == True:
        links = get_links_from_html(html_doc, init = True)
    else:
        links = get_links_from_html(html_doc, init = False)

    results = search_links(metric = metric,
                           link_url = link_url, 
                           html_links = links)
    return results

def clean_dataframe(data):
    '''
    Create dataframe, some clean up, and add data_type column.
    '''
    pd_results = pd.DataFrame(data)
    if data.text.str.contains(':').any():
        data['text'] = data['text'].str.replace(':', ' -')

    # SQF has a different naming convention
    if data.metric.str.contains('sqf').any():
        data['text'] = "SQF " + data['text']

     # SQF has a different naming convention
    file = data['url'].str.split('/').str[-1]
    data['data_type'] = file.str.split('.').str[-1]
    clean_df = data

    # output to csv
    return clean_df

#%%
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--metric", 
                        help="The shortform name of the metric.",
                        type=str)
    parser.add_argument( "--init",  
                        help="T/F for whether it's the first time scraping the page.",
                        type=bool)
    args = parser.parse_args()
    metric_links = get_specific_links(args.metric, init = args.init)
    clean_results = clean_dataframe(data = metric_links)

    clean_results.to_csv(f'results/{args.metric}_links.csv', index = False) 
#%%
