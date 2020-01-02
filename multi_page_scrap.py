# libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# get the data
def get(url):
    """
    its a funtion to get the data from webpage
    """    
    page = requests.get(url) 
    if page.status_code == 200:
        htmldata = page.text
        soup = BeautifulSoup(htmldata, 'lxml')
        print('success')
        return soup
    else:
        print('error',page.status_code)

def extract(soup):
    page_tags = [] # will hold the tags from a page
    tag_name = soup.find_all('div',attrs={'class':'i-tag'})
    tag_posts= soup.find_all('div',attrs={'class':'i-total'})
    
 
    for t,p in zip(tag_name,tag_posts):
        data = (t.text,p.text)
        page_tags.append(data)
    print('total tags collected',len(page_tags))
    return page_tags

def save(dataset,filename="out.csv"):
    if len(dataset) > 0:
        print('saving dataset...')
        df = pd.DataFrame(dataset)
        df.to_csv(filename)
        print('saved file to', filename)
    else:
        print('could not save empty dataset')