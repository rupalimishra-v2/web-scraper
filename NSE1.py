# -*- coding: utf-8 -*-
"""
Created on Wed Sept 07 15:30:53 2022
The script pulls the data from the NSE India website and gets all the images links involved in the creation of
the website.
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import csv


def scrape():
    head = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/87.0.4280.88 Safari/537.36 "
    }
    req = requests.session().get(url="https://www.nseindia.com/", headers=head)
    soup = bs(req.text, 'html.parser')

    return soup


def etl():
    try:
        page = scrape()

    except Exception as e:
        print(e)

    titles = []
    links = []
    title_to_img_src = {}
    images_list = page.find_all('img')
    for image in images_list:
        titles.append(image.get('title'))
        links.append(image.get('src'))
        title_to_img_src[image.get('title')] = image.get('src')
    print(title_to_img_src)

    df = pd.DataFrame()
    df['title'] = titles
    df['links'] = links
    return df


''' Further we can use the csv file data to process and derive meaningful information out of it. '''


def get_images():
    data = pd.read_csv('nse.csv')
    images = [data.links]
    for image in images[0]:
        img = requests.get(image)
        print(img)


def main():
    df1 = etl()
    dd = pd.concat([df1])
    dd.to_csv('nse.csv', encoding='utf_8_sig')
    # get_images()


if __name__ == "__main__":
    main()
