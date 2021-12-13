# Set up Dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
import pymongo
import requests
from splinter import Browser
import time
from webdriver_manager.chrome import ChromeDriverManager

def scrape_info():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # Set scraper to retreive image from Mars url 
    mars_url = 'https://redplanetscience.com/'
    browser.visit(mars_url)

    time.sleep(1)

    #Assign HTML content to variable    
    html = browser.html
    mars_soup = bs(html, 'html.parser')

    # Pull news title and paragraph teaser info
    title = mars_soup.find('div', class_='content_title').text
    teaser = mars_soup.find('div', class_='article_teaser_body').text

    # Set scraper to retreive image from JPL url
    jpl_url = 'https://spaceimages-mars.com/'
    browser.visit(jpl_url)

    time.sleep(1)

    #Assign HTML content to variable
    html = browser.html
    jpl_soup = bs(html, 'lxml')

    # Pull image
    image = jpl_soup.find_all('img', class_= "headerimage fade-in")[0]["src"]
    featured_image_url = jpl_url + image

    # Use the read_html function in Pandas to automatically scrape tabular data from the Mars Facts url
    url = 'https://galaxyfacts-mars.com/'

    # Read table
    mars_table = pd.read_html(url)

    # Slice off any Mars dataframe using normal indexing
    facts_df = mars_table[0]
    facts_df.columns = ['Description', 'Mars', 'Earth']

    # Create html table from Dataframe
    mars_html_table = facts_df.to_html(border="1", justify="left")

    # Remove newlines
    mars_html_table.replace('\n', '')

    # Set scraper to retreive images from Mars Hemisheres url
    hems_url = 'https://marshemispheres.com/'
    browser.visit(hems_url)

    time.sleep(1)

    #Assign HTML content to variable    
    html = browser.html
    hems_soup = bs(html, 'lxml')

    # Locate and pull hemisphere data
    all_hemispheres = hems_soup.find('div', class_= "collapsible results")
    # Locate and pull individual hemisphere data
    each_hemisphere = all_hemispheres.find_all('div', class_='item')

    hems_link = []

    # Iterate through to locate each hemisphere title and image

    for one in each_hemisphere:
        # Find the title of the image
        hems_title = one.find("h3").text
        hems_title = hems_title.replace("Enhanced", "")
        
        #Find the image url
        image = one.find('img', class_= "thumb")["src"]

        # Create featured image url
        img_url = hems_url + image
        
        # Create dictionary for title and image info
        hems_dict = {}
        hems_dict['title'] = hems_title
        hems_dict['img_url'] = img_url
        
        hems_link.append(hems_dict)

    # Store all scraped data in a mars dictionary
    mars_data_dict = {
        "news_title": title,
        "news_info": teaser,
        "featured_image_url": featured_image_url,
        "fun_facts_table": str(mars_html_table),
        "hemisphere_info": hems_link
    }

    # Quit the browser
    browser.quit()

    return mars_data_dict
