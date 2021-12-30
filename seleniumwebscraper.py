#import neccesary packages
import requests
import numpy
import bs4
import re
import csv
import time
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options  

#Return the page html using selenium chromedriver
def defineHTML(yearIndex, url):
    chrome_options = Options()  
    chrome_options.add_argument("--headless")  
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get(url) #navigate to the page
    #select year element
    dropdownItem = browser.find_element_by_xpath('//*[@id="pastResultsYearSelector"]/option[{}]'.format(yearIndex))
    dropdownItem.click()
    time.sleep(1)
    innerHTML = browser.page_source
    browser.close()
    return innerHTML

#Find course information within the html using bs4
def webscrapeCourse(yearIndex, url):
    innerHTML = defineHTML(yearIndex, url)
    soup = bs4.BeautifulSoup(innerHTML, 'lxml')

    #Find the course name
    course = soup.find(string = re.compile("Course:"))
    course = course.lstrip('Course:')
    course = course.strip(' ')

    # Find the purse amount
    purse = soup.find(string = re.compile("Purse:"))
    if purse != None:
        purse = purse[8:len(purse)]
    else:
        purse = "NULL"

    #Find the course par
    par = soup.find(string = re.compile("PAR:"))
    par = par.lstrip('PAR: ')
    
    #Find the ending date of the tournment
    ending = soup.find(string = re.compile("Ending:"))
    ending = ending.lstrip('Ending: ')

    #Find year based on end date
    year = ending[-4:len(ending)]

    #Find the tournament title
    titleString = soup.title.string
    titleString = titleString[0:-14]

    #Combine attributes in a list
    coursedata = [titleString, year, ending, par, course, purse]
    return coursedata

#Function to return entire scoreboard data for the url and year selected
def playerscore(yearIndex, url):
    innerHTML = defineHTML(yearIndex, url)
    soup = bs4.BeautifulSoup(innerHTML, 'lxml')
    
    
    #Find the scoreboard table in the html
    table = soup.find('table', attrs={'class':'table-styled'})
    table_body = table.find_all('tbody')
    
    #Find the title
    titleString = soup.title.string
    titleString = titleString[0:-14]

    #Find the end date
    ending = soup.find(string = re.compile("Ending:"))
    ending = ending.lstrip('Ending: ')

    #Find the year
    year = ending[-4:len(ending)]

    #Loop through the html line by line to find the table values
    data = []
    for i in range(1,len(table_body)):
        #Find all table rows
        table = table_body[i].find_all('tr')
        for row in table:
            #Find each value in the table row and create a list of values
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            #Add list of values to the data masterlist
            data.append(cols)

    #Add association variable to each list in the masterlist, Plus some additional cleanup
    for i in data:
        i[1] = i[1].lstrip('T')
        i[7] = i[7].lstrip('$')
        i.append(titleString)
        i.append(ending)
        i.append(year)
    
    return data
