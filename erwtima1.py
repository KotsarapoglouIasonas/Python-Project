from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import jsons
import pandas as pd

from MovieClass import MovieClass

WEBSITE_1 = 'https://www.subs4free.club/search_report.php?search='
WEBSITE_2 = '&searchType=1'
MOVIE_NAME = 'furious'

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
    websource = driver.page_source
    return websource

def getHTMLsources2(download_link):
    ouroptions = Options()
    ouroptions.add_argument('--headless')
    driver = webdriver.Chrome(options = ouroptions, service=Service((ChromeDriverManager().install())))
        
    driver.get('https://www.subs4free.club' + download_link)
    websource = driver.page_source
    return websource

def deutero_epipedo(download_link, movie):
    web_source = getHTMLsources2(download_link)
    rating_no_reviews_regex = r'Βαθμολογία:<\/span><\/b>\s*(\d\.?\d?\/10) \((\d+)\)<\/p>'
    genre_regex = r'Είδος ταινίας:<\/span><\/b>\s(.*?)<\/p>'

    rating_no_reviews = re.findall(rating_no_reviews_regex, web_source)
    if rating_no_reviews:
        rating = rating_no_reviews[0][0]
        movie.setRating(rating)
        no_reviews = rating_no_reviews[0][1]
        movie.setReviews(no_reviews)
    else:
        movie.setReviews("")
        movie.setRating("")
    
    genre = re.findall(genre_regex, web_source)
    if genre:
        movie.setGenre(genre[0])
    else:
        movie.setGenre("")

    return movie



def get_list_of_entries(websource):
    #regex gia tin apothikeusi twn pliroforiwn tis kathe tainias
    entries_list_regex = '<div class="movie-details(.*?)<div class="clearfix">'
    sub_name_regex = '<span>(.*?)</span>'
    sub_title_lang_regex = 'class="sprite (\w+)gif"><\/div><span>'
    sub_user_creator_regex = 'title="Subtitles uploaded by .*?">([\w_-]*?)<\/a>'
    times_dl_regex = '<\/a><p><b>(\d+)<\/b>DLs'
    created_at_regex = 'on (\d+\/\d+\/\d+ \d+:\d+[apm]{2})(<\/p><\/div>)?'
    download_link_regex = '<div class="movie-download"><a href="(\/.*?)" title="'
    entries_list  = re.findall(entries_list_regex, websource)


    global final_dictionary 
    df1 = pd.DataFrame(final_dictionary)
    i=0
    #for each entrance in the entries list (each sub)
    for entry in entries_list:
        sub_title_name = re.findall(sub_name_regex, entry)
        #elegxos ean vrethikan apotelesmata
        if len(sub_title_name) > 0:
            sub_title_name = sub_title_name[0]
        else:
            sub_title_name = ""

        sub_title_lang = re.findall(sub_title_lang_regex, entry)
        #elegxos ean vrethikan apotelesmata
        if len(sub_title_lang) > 0:
            sub_title_lang = sub_title_lang[0]
        else:
            sub_title_lang = ""

        sub_user_creator = re.findall(sub_user_creator_regex, entry)
        #elegxos ean vrethikan apotelesmata
        if len(sub_user_creator) > 0:
            sub_user_creator = sub_user_creator[0]
        else:
            sub_user_creator = ""
        
        times_dl = re.findall(times_dl_regex, entry)
        #elegxos ean vrethikan apotelesmata
        if len(times_dl) > 0:
            times_dl = times_dl[0]
        else:
            times_dl = ""

        created_at = re.findall(created_at_regex, entry)
        #elegxos ean vrethikan apotelesmata
        if len(created_at) > 0:
            created_at = created_at[0]
        else:
            created_at = ""
        
        download_link = re.findall(download_link_regex, entry)
        #elegxos ean vrethikan apotelesmata
        if len(created_at) > 0:
            created_at = created_at[0][0]
        else:
            created_at = ""

        #dimiourgia antikeimenou tainias
        movie = MovieClass(sub_title_name, sub_title_lang,sub_user_creator,times_dl, created_at,download_link)

        #meta tin apoktisi tou link prosthiki sto epomeno epipedo
        movie = deutero_epipedo(download_link[0], movie)

        #metatropi se dictionary
        movie = jsons.dump(movie)
       
        df2 = pd.DataFrame([movie], index = [0])
        #prosthiki tou neou DataFrame στο 
        df1 = df1.append(df2, ignore_index = True)
        
        print (df1)

    #eggrafi tou DataFrame sto excel
    df1.to_excel('pandasexcel.xlsx', sheet_name='newsheet')


def main():
    websource = getHTMLsources()
    get_list_of_entries(websource)


if __name__ == "__main__":
    main()