from bs4 import BeautifulSoup as bs4
import selenium
import requests
import re
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class webscraper:
    '''
        Given a link to a page with reviews, perform scraping to gather data on the movie
        The information yieled through all of these is below but it gets the 
        name of the movie, text review, numerical review, usefulness rating, and name of user
        The only field of the scraper is a soup object and you'd call the getters buy invoking soup.find() with relevant parameters 

        lister_item_content is the overarching div that has all the information we want
    '''

    def __init__(self, link):
        ''' 
            Constructor
            link - link to the review page with the html we are parsing
            soup attribute is the soup object 
        '''
        self.soup = self.__scrape_reviews(link)

    def __scrape_reviews(self, link):
        '''
            Private helper that uses selenium to scroll for multiple pages, so that multiple reviews are collected by the soup object
        '''
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.get(link)
        if len(driver.find_elements(By.CLASS_NAME, "ipl-load-more__button")) != 0:
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
                (By.CLASS_NAME, "ipl-load-more__button")))
            for i in range(20):  # 20 here is arbitrary, if we wanted to scrape until time out, we could do a while loop that continues when a timeout is caught
                try:
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
                        (By.CLASS_NAME, "ipl-load-more__button"))).click()
                    #print("MORE button clicked")
                except TimeoutException:
                    break

        soup = bs4(driver.page_source)
        driver.close()
        return soup

    def get_review(self, lister_item_content):
        '''
            for an individual listed item's content, scrape the review
        '''
        rev = lister_item_content.find(
            'div', attrs={'class': 'text show-more__control'})
        if rev is not None:
            review = ''
            for it in rev.contents:
                if not re.match('^<', str(it)):
                    review += (str(it))
                    review += (' ')
            review = review.split('\n')
            clean_review = ' '.join(review)
            clean_review = clean_review.split("\'")
            clean_review = "'".join(clean_review)
            return str(clean_review)
        return 'No review'

    def get_rating(self, lister_item_content):
        '''
            find the numerical rating out of 10 for a listed item's content
        '''
        r = lister_item_content.find(
            'span', attrs={'class': 'rating-other-user-rating'})
        if r is not None:
            for it in r.contents:
                if re.match("<span>[0-9|10]</span>", str(it)):
                    return it.contents[0]
        return -1

    def get_username(self, lister_item_content):
        '''
            Get the user name of the user who created the review
        '''
        cont = lister_item_content.find(
            'span', attrs={'class': 'display-name-link'})
        if cont is not None:
            tag = cont.contents
            user_name = tag[0].contents
            return str(user_name[0])
        return "No Username"

    def get_usefulness_rating(self, lister_item_content):
        '''
            Gets the usefulness rating of a review
        '''
        cont = lister_item_content.find(
            'div', attrs={'class': 'actions text-muted'})
        if cont is not None:
            nums = re.findall('[0-9]+', cont.contents[0])
            if float(nums[1]) != 0:
                return float(nums[0])/float(nums[1])
        return -1

    def get_dirty_reviews(self):
        return self.soup.findAll('div', attrs={'class': 'lister-item-content'})

    def get_name(self):
        name = re.split("<|>", str(self.soup.find('a', itemprop="url")))[2]
        return name
