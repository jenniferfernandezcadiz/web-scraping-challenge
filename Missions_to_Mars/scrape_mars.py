# import dependencies
from bs4 import BeautifulSoup
import requests as r 
import pandas as pd
from splinter import Browser
import os
from flask import Flask, render_template
from selenium import webdriver
import time 
import json
import pymongo


def init_browser():
    executable_path= {'executable_path': 'C://Users/jenni/OneDrive/Documents/chromedrv/chromedriver.exe'}
    return Browser ('chrome', **executable_path, headless=False)

def scrape():
    
    browser=init_browser()
    mission_to_mars={}

    # Mars News
    url="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(5)

    html=browser.html
    soup_nasa=BeautifulSoup(html,'html.parser')

    mission_to_mars['mars_title'] = soup_nasa.find('div', class_='content_title')
    mission_to_mars['mars_paragraph']=soup_nasa.find('div', class_='rollover_description_inner')

    # Mars Space Images
    url_images='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_images)

    html2=browser.html
    image_soup=BeautifulSoup(html2, 'html.parser')
    images=image_soup.find_all('a',class_='fancybox')

    nasa_pic=[]
    for i in images: 
        picture=i['data-fancybox-href']
        nasa_pic.append(picture)

    mission_to_mars['featured_image_url']='https://www.jpl.nasa.gov' + str(nasa_pic[1])

    # Mars Weather


    # Mars Facts
    facts_url='https://space-facts.com/mars/'
    facts_table=pd.read_html(facts_url)[0]
    html_facts=facts_table.to_html()
    
    mission_to_mars['mars_facts']=html_facts

    # Mars Hemispheres
    hemisphere_image_urls=[]

    # Cerberus Hemisphere
    url_cerberus='https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    browser.visit(url_cerberus)
    cerberus_result=browser.html
    soup_cerberus=BeautifulSoup(cerberus_result, "html.parser")
    cerberus_image=soup_cerberus.find_all('div', class_='wide-image-wrapper')

    for c in cerberus_image:
        c_image=c.find('li')
        full_image=c_image.find('a')['href']

    c_title=soup_cerberus.find('h2', class_='title').text

    cerberus_hemp={"Title": c_title, "url": full_image}

    hemisphere_image_urls.append(cerberus_hemp)

    # Schiaparelli Hemisphere
    url_schi='https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    browser.visit(url_schi)
    schi_result1=browser.html
    soup_schi=BeautifulSoup(schi_result1, 'html.parser')
    schi_image=soup_schi.find_all('div', class_='wide-image-wrapper')

    for s in schi_image:
        s_image=s.find('li')
        full_image=s_image.find('a')['href']

    s_title=soup_schi.find('h2', class_='title').text

    schi_hemp={"Title": s_title, "url": full_image}

    hemisphere_image_urls.append(schi_hemp)


    # Syrtis Major Hempisphere

    url_syrtis='https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    browser.visit(url_syrtis)
    syrtis_result1=browser.html
    soup_syrtis=BeautifulSoup(syrtis_result1, 'html.parser')
    syrtis_image=soup_syrtis.find_all('div', class_='wide-image-wrapper')

    for sy in syrtis_image:
        sy_image=sy.find('li')
        full_image=sy_image.find('a')['href']

    sy_title=soup_syrtis.find('h2', class_='title').text

    syrtis_hemp={"Title": sy_title, "url": full_image}

    hemisphere_image_urls.append(syrtis_hemp)

    # Valles Hemisphere

    url_valles='https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    browser.visit(url_valles)
    valles_result1=browser.html
    soup_valles=BeautifulSoup(valles_result1,'html.parser')
    valles_image=soup_valles.find_all('div', class_='wide-image-wrapper')

    for v in valles_image:
        v_image=v.find('li')
        full_image=v_image.find('a')['href']

    v_title=soup_valles.find('h2', class_='title').text

    valles_hemp={"Title": v_title, "url": full_image}

    hemisphere_image_urls.append(valles_hemp)


    mission_to_mars["hemisphere_image"]=hemisphere_image_urls

    return mission_to_mars







