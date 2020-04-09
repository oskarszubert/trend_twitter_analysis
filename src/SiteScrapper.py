from bs4 import BeautifulSoup
import pandas as pd
import os
import requests
import time

class SiteScrapper():

    def scrape_yelp_url(self,web_url,filename='yelp_data'):
        collected_data = self.get_review_from_yelp(web_url)
        self.save_date_to_file(filename, collected_data)


    def scrape_ceneo_url(self,web_url,filename='ceneo_data'):
        collected_data = self.get_review_from_ceneo(web_url)
        self.save_date_to_file(filename, collected_data)


    def scrape_multiple_yelp_urls(self,save_as='yelp_data',urls_file='model_train_data/urls/yelp_urls.txt'):
        try:
            file = open(urls_file,'r')
        except Exception as e:
            print("Error! Cannot open file")
            print(e)
            exit(0)

        for line in file:
            print('Scraping site:' , line.strip('\n'),' ', end='')
            self.scrape_yelp_url(line.strip('\n'))


    def scrape_multiple_ceneo_urls(self,save_as='ceneo_data',urls_file='model_train_data/urls/ceneo_urls.txt'):
        try:
            file = open(urls_file,'r')
        except Exception as e:
            print("Error! Cannot open file")
            print(e)
            exit(0)

        for line in file:
            print('Scraping site:' , line.strip('\n'),' ', end='')
            self.scrape_ceneo_url(line.strip('\n'))

    def get_review_from_yelp(self, web_url):
        try:
            source = requests.get(web_url).text
            html_source = BeautifulSoup(source, 'lxml')
        except Exception as e:
            print("Error! while getting html site.")
            print(e)
            exit(0)

        div_review = html_source.find_all('div',itemprop='review')

        collected_data = []
        for review in div_review:
            tmp_list = []

            comment = review.p.text
            tmp_list.append( self.evaluate_review( float(review.find('meta',itemprop='ratingValue').get("content")) ) )
            tmp_list.append( comment )
            tmp_list.append('')
            collected_data.append( tmp_list )

        return collected_data


    def get_review_from_ceneo(self, web_url):
        try:
            source = requests.get(web_url).text
            html_source = BeautifulSoup(source, 'lxml')
        except Exception as e:
            print("Error! while getting html site.")
            print(e)
            exit(0)

        div_review = html_source.find_all("div", class_="show-review-content content-wide")

        collected_data = []
        for review in div_review:
            tmp_list = []
            comment = review.find('p', class_='product-review-body').text
            value = review.find('span', class_='review-score-count').text 
            tmp_list.append( self.evaluate_review( float(value.split('/')[0].replace(',','.'))) )
            tmp_list.append('')
            tmp_list.append( comment )
        
            collected_data.append(tmp_list)
        return collected_data


    def save_date_to_file(self, filename, collected_data):
        if not collected_data:
            print('Failed !')
            return None
        path_to_file = 'model_train_data/tagged/'
        if not os.path.exists( path_to_file ):
            os.makedirs(path_to_file)

        filename = path_to_file + filename.lower()+'.xlsx'
        if not os.path.exists(filename):
            self.xlsx_df = pd.DataFrame(columns=['sentient','text','vector'])
            self.xlsx_df.to_excel(filename,index=False)
            
        self.xlsx_df = pd.read_excel(filename)
        tmp_df = self.prepare_df(collected_data)

        self.xlsx_df = self.xlsx_df.append(tmp_df, ignore_index=True)
        self.xlsx_df.to_excel(filename,index=False)
        print('File: \'' + filename + '\' saved!')


    @staticmethod
    def prepare_df(collected_data):
        df = pd.DataFrame(data=collected_data, columns=['sentient','text','vector'])
        return df


    @staticmethod
    def evaluate_review(value):
        if value > 3:
            return 1
        elif value < 3:
            return -1
        else:
            return 0
