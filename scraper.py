import requests
from bs4 import BeautifulSoup


days_in_month = [31,28,31,30,31,30,31,31,30,31,30,31]
months = [1,2,3,4,5,6,7,8,9,10,11,12]

def scrape(day,month,year):
    url = 'https://www.wunderground.com/history/daily/it/brescia/LIPO/date/{}/{}/{}'.format(year,month,day)
    print(url)
    response = requests.get(url)
    html_content = response.content

    # Create a BeautifulSoup object from the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # get this element: <app-root _nghost-sc138="" ng-version="11.2.14" _nghost-app-root-c105=""><router-outlet _ngcontent-app-root-c105=""></router-outlet><app-history _nghost-app-root-c232="" class="ng-star-inserted"><one-column-layout _ngcontent-app-root-c232="" _nghost-app-root-c130=""><ad-wx-hidden _ngcontent-app-root-c130="" class="ng-star-inserted"><div id="hidden-ad-browser"><div id="WX_Hidden" style="display: none; margin-top: -21px;"><div id="google_ads_iframe_/7646/web_wunderground_us/_9__container__" style="border: 0pt none;"></div></div></div></ad-wx-hidden><!----><wu-header _ngcontent-app-root-c130="" role="main" _nghost-app-root-c128=""><div _ngcontent-app-root-c128="" class="topbar"><div _ngcontent-app-root-c128="" id="global-header" class="global-header"><a _ngcontent-app-root-c128="" href="#main-page-content" class="hidden-navigation button radius">Skip to Main Content</a><a _ngcontent-app-root-c128="" href="/" id="header-logo" title="Weather Underground" aria-label="Weather Underground Logo" class="logo">_</a><lib-menu _ngcontent-app-root-c128="" _nghost-app-root-c124="" class="ng-star-inserted"><nav _ngcontent-app-root-c124="" class="feature-menu" aria-label="Article"><menu-item _ngcontent-app-root-c124="" class="ng-star-inserted"><button aria-haspopup="true" mat-button="" class="mat-focus-indicator mat-menu-trigger mat-button mat-button-base wunder-r" title="Sensor Network"><span class="mat-button-wrapper"> Sensor Network
    #get the body 
    table = soup.find('body')
    #get all the values in all the tags 
    table = soup.find_all('body')
    print(table)
    #print(table)
    
    #now we will parse out the data we want

    #make script regex pattern
    import re
    #get the digit from this patter r'"temperatureMin24Hour&q;:(\d+)'
    pattern = re.compile(r'.*temperatureMin24Hour&q;:(\d+).*')
    #find all the matches in the table
    minT = pattern.findall(str(table))
    
    #now for min 
    pattern = re.compile(r'.*class="ng-star-inserted>(\d+).*')
    #find all the matches in the table
    MaxT = pattern.findall(str(table))
    print('MaxT: ', MaxT)
    
    #now precipitation
    pattern = re.compile(r'.*precip24Hour&q;:(\d+).*')
    #find all the matches in the table
    precip = pattern.findall(str(table))
    #cast all to int 
    minT = int(minT[0])
    MaxT = int(MaxT[0])
    precip = int(precip[0])

    avg_tmp = (MaxT + minT)/2
    print('avg_tmp: ', avg_tmp)
    return [avg_tmp, precip]
    
print(scrape(1,1,2017))


#let's loop through all the days in 2017 and 2018 to get the data and store it in a csv file with the following format date, avg_tmp, precip
import csv
with open('weather.csv', 'w', newline='') as csvfile:
    fieldnames = ['date', 'avg_tmp', 'precip']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for year in [2017,2018]:
        for month in months:
            for day in range(1,days_in_month[month-1]+1):
                date = '{}/{}/{}'.format(day,month,year)
                avg_tmp, precip = scrape(day,month,year)
                writer.writerow({'date': date, 'avg_tmp': avg_tmp, 'precip': precip})