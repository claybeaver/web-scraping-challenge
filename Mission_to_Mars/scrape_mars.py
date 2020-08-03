import pandas as pd
import pymongo
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
from selenium import webdriver
from flask import Flask, render_template

def init_browser():
    executable_path = {'executable_path': 'C:/Users/Clay/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    scraped_dict = {}
    browser = init_browser()
    
    # NASA MARS NEWS
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    scraped_dict['title'] = browser.find_by_css("div.content_title a").text
    scraped_dict['news'] = browser.find_by_css("div.article_teaser_body").text
    browser.quit()

    # JPL MARS SPACE IMAGES - Featured Image
    executable_path = {'executable_path': 'C:/Users/Clay/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_jpl)
    html_jpl = browser.html
    soup_jpl = bs(html_jpl, 'html.parser')
    button = browser.find_by_id('full_image')
    button.click()
    html_mars_img = browser.html
    soup_mars_img = bs(html_mars_img, 'html.parser')
    more_info = browser.links.find_by_partial_text('more info')
    more_info.click()
    html_more_info = browser.html
    soup_full_mars_img = bs(html_more_info, 'html.parser')
    mars_img_link = soup_full_mars_img.select_one('figure.lede a img').get('src')
    featured_image_url = f'https://www.jpl.nasa.gov{mars_img_link}'
    scraped_dict['imgurl'] = featured_image_url
    browser.quit()

    # MARS WEATHER TWITTER
    executable_path = {'executable_path': 'C:/Users/Clay/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url_twitter = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_twitter)
    html = browser.html
    soup = bs(html, 'html.parser')
    mars_text = soup.find("div", { "data-testid" : "tweet" })
    mars_weather = mars_text.text.strip()
    scraped_dict['weather'] = mars_weather
    browser.quit()

    # MARS FACTS
    executable_path = {'executable_path': 'C:/Users/Clay/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url_marsfacts = 'https://space-facts.com/mars/'
    browser.visit(url_marsfacts)
    mars_table = pd.read_html(url_marsfacts)
    mars_info.set_index([0])
    mars_info_html = mars_info.to_html()
    scraped_dict['table'] = mars_info_html
    browser.quit()

    # MARS HEMISPHERES
    executable_path = {'executable_path': 'C:/Users/Clay/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hem_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    link = browser.find_by_css("a.product-item h3")
    hemisphere_image_urls = []
    hemisphere_dict = {}
    browser.find_by_text('Cerberus Hemisphere Enhanced').click()
    hemisphere_dict['title'] = browser.find_by_css("h2.title").text
    hemisphere_dict['img_url'] = browser.links.find_by_text('Original').first['href']
    hemisphere_image_urls.append(hemisphere_dict)
    browser.visit(hem_url)
    browser.find_by_text('Schiaparelli Hemisphere Enhanced').click()
    hemisphere_dict['title'] = browser.find_by_css("h2.title").text
    hemisphere_dict['img_url'] = browser.links.find_by_text('Original').first['href']
    hemisphere_image_urls.append(hemisphere_dict)
    browser.visit(hem_url)
    browser.find_by_text('Syrtis Major Hemisphere Enhanced').click()
    hemisphere_dict['title'] = browser.find_by_css("h2.title").text
    hemisphere_dict['img_url'] = browser.links.find_by_text('Original').first['href']
    hemisphere_image_urls.append(hemisphere_dict)
    browser.visit(hem_url)
    browser.find_by_text('Valles Marineris Hemisphere Enhanced').click()
    hemisphere_dict['title'] = browser.find_by_css("h2.title").text
    hemisphere_dict['img_url'] = browser.links.find_by_text('Original').first['href']
    hemisphere_image_urls.append(hemisphere_dict)
    scraped_dict['hemispheres'] = hemisphere_image_urls
    browser.quit()
    
    return scraped_dict





