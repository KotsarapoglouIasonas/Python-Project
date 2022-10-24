from turtle import down
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
from selenium.webdriver.common.by import By
import jsons
import pandas as pd

from MovieClass import MovieClass

WEBSITE_1 = 'https://www.subs4free.club/search_report.php?search='
WEBSITE_2 = '&searchType=1'
MOVIE_NAME = 'the batman'

final_dictionary = {'created_at':[],'download_link':[], 'genre':[], 'no_reviews':[], 'rating':[], 'sub_creator':[], 'sub_lang':[],'sub_name':[], 'times_dl':[]}

#sunartisi pou kanei merge 2 dictionary wste na enwsoume tis plirofories 1ou kai 2ou epipedou
def mergeDictionary(dict_1, dict_2):
   dict_3 = {**dict_1, **dict_2}
   for key, value in dict_3.items():
       if key in dict_1 and key in dict_2:
               dict_3[key] = [value , dict_1[key]]
   return dict_3

def getHTMLsources():
    ouroptions = Options()
    ouroptions.add_argument('--headless')
    driver = webdriver.Chrome(options = ouroptions, service=Service((ChromeDriverManager().install())))
    
    
    #replace movie name blanks with plus
    movie_name = MOVIE_NAME.replace(' ', '+')
    
    #apoktisi kwdika gia tin tainia
    driver.get(WEBSITE_1 + movie_name +WEBSITE_2)
    return driver

def getHTMLsources2(download_link):
    ouroptions = Options()
    ouroptions.add_argument('--headless')
    driver = webdriver.Chrome(options = ouroptions, service=Service((ChromeDriverManager().install())))
    
    driver.get('https://www.subs4free.club' + download_link)
    
    return driver



def get_list_of_entries(driver):
    entries_list = driver.find_elements(By.CLASS_NAME, "movie-details")
    
    global final_dictionary 
    
    df1 = pd.DataFrame(final_dictionary)
    i=0
    #for each entrance in the entries list (each sub)
    for entry in entries_list:
        sub_title_name = entry.find_element(By.CSS_SELECTOR, ".movie-heading > span")
        print (sub_title_name.text)
        
        sub_title_lang = entry.find_element(By.CSS_SELECTOR, '.movie-heading > div')
        lang = sub_title_lang.get_attribute('class')[:-3]
        print (lang[-2:])
        lang = lang[-2:]

        sub_user_creator = entry.find_element(By.CSS_SELECTOR, '.movie-info > p > a')
        print (sub_user_creator.text)
        
        times_dl = entry.find_element(By.CSS_SELECTOR, '.movie-download > p > b')
        print (times_dl.text)
        
        created_at = entry.find_element(By.CSS_SELECTOR, '.movie-info > p')
        print (created_at.text)
        
        download_link = entry.find_element(By.CSS_SELECTOR, '.movie-heading')
        download_link = download_link.get_attribute('href')
        print (download_link)
        
        #dimiourgia antikeimenou me tis parapanw plirofories
        movie = MovieClass(sub_title_name.text,lang, sub_user_creator.text, times_dl.text, created_at.text,download_link)

        
        movie = jsons.dump(movie)
       
        df2 = pd.DataFrame([movie], index = [0])
        
        df1 = df1.append(df2, ignore_index = True)
        
        print (df1)


#arxiki sunartisi gia ekkinisi tou driver
def main():
    driver = getHTMLsources()
    get_list_of_entries(driver)


if __name__ == "__main__":
    main()