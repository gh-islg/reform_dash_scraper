
#%%
from bs4 import BeautifulSoup
import requests
import argparse
import git 
import re
# %%
def get_commit_history(data_path):
    '''
    Get the latest commit diff of a file.
    '''
    repo = git.Repo('..')
    commits = list(repo.iter_commits(paths=data_path))
    latest_commits = commits[-2:]
    diffs = repo.git.diff(latest_commits[0], latest_commits[1], data_path)
    return diffs

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
        soup = BeautifulSoup(diffs, 'html.parser')
        links = soup.find_all('a')
    return links

def get_specific_links(metric, init = True):
    '''
    Get the links depending on the metric.
    '''
    if init == True:
        links = get_links_from_html(html_doc, init = True)
    else:
        links = get_links_from_html(html_doc, init = False)

    if metric == 'vehicle_stops':
        urls, texts = [], []
        for link in links:
            try:
                url = link.get('href')
                if 'assets/nypd/downloads/excel/analysis_and_planning/vehcile-encounter-reports/' in url:
                    urls.append(url)
                    texts.append(link.get_text())
                    print(url)
            except:
                pass
    results = {
        'url': urls,
        'text': texts
    }
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path_to_html", 
                        help="The repo path to the html document."
                        type=str)
    parser.add_argument("--metric", 
                        help="The shortform name of the metric."
                        type=str)
    parser.add_argument("--init", 
                        help="T/F for whether it's the first time scraping the page."
                        type=bool)
    args = parser.parse_args()
    metric_links = get_specific_links(args.metric, init = args.init)
    print(metric_links)
