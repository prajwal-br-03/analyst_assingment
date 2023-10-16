import numpy as np
import requests
from bs4 import BeautifulSoup
import pandas as pd
url="https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
HEADERS=({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36','Accept-Language':'en-US,en;q=0.5'})
webpage = requests.get(url,headers=HEADERS)

soup = BeautifulSoup(webpage.content,"html.parser")
link = soup.find_all("span",attrs={'class':'a-size-medium a-color-base a-text-normal'})

num_pages_to_scrape = 20

d={"product_name":[],"price":[],"rating":[],"reviews":[]}

for page_num in range(1, num_pages_to_scrape + 1):
    page_url = f"{webpage}{page_num}"
    soup = BeautifulSoup(webpage.content, "html.parser")
    link = soup.find_all("span", attrs={'class': 'a-size-medium a-color-base a-text-normal'})
    price=soup.find_all("span",attrs={'class':'a-price-whole'})
    rating=soup.find_all("span",attrs={'class':'a-size-base s-underline-text'})
    review=soup.find_all("span",attrs={'class':'a-icon-alt'})
    for i in range(0,len(link)):
        d["product_name"].append(link[i].text.strip())
        d["price"].append(price[i].text.strip())
        #d["reviews"].append(rating[i].text.strip())
        d["rating"].append(review[i].text.strip())

amazon_df=pd.DataFrame.from_dict(d)
amazon_df['product_name'].replace('',np.nan,inplace=True)
amazon_df=amazon_df.dropna(subset=['product_name'])
amazon_df.to_csv("amazon_data.csv",header=True,index=False)
print(amazon_df)
