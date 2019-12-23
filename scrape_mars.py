#Dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
from selenium import webdriver
import time



def scrape():
    # @NOTE: Replace the path with your actual path to the chromedriver
    browser = Browser("chrome", executable_path="/Users/yorch/Documents/GitHub/chromedriver.exe", headless=True)
    news_title, news_p = news(browser)

    data = {
        "title": news_title(),
        "paragraph": news_p(),
        "image": image(browser),
        "weather": twitter_weather(browser),
        "facts": facts(),
        "hemispheres": hemispheres(browser),   
    }

    browser.quit()
    return data

def news(browser):
    nasa_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(nasa_url)

    html = browser.html
    soup = bs(html, "html.parser")
    news_title = soup.find(name="div", attrs={"class":"content_title"}).find("a").text
    news_p = soup.find(name="div", attrs={"class":"article_teaser_body"}).text

    return news_title, news_p


def image(browser):
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

    #click on full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()

    #scrape image
    html = browser.html
    soup = bs(html, "html.parser")

    results = soup.find(name="figure", attrs={"class":"lede"}).a.img["src"]
    featured_image_url = "https://www.jpl.nasa.gov"+results
    
    return featured_image_url

def twitter_weather(browser):

    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)

    html = browser.html
    soup = bs(html, "html.parser")

    mars_weather = soup.find("div", class_="js-tweet-text-container")
    mars_weather = mars_weather.p.text

    return mars_weather

def facts():
    facts_df = pd.read_html('https://space-facts.com/mars/')[0]
    facts_df.columns=['Profile_item', 'Value']
    facts_df.set_index('Profile_item', inplace=True)
    facts_html = facts_df.to_html()

    return facts_html

def hemispheres(browser):
    hemis_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemis_url)

    html = browser.html
    soup = bs(html, "html.parser")

    items = soup.find_all(name="div",attrs={"class":"item"})

    hemisphere_image_urls =[]
    hemis_main_url = "https://astrogeology.usgs.gov"

    for i in items: 
        title = i.find("h3").text
        partial_img_url = i.find("a", class_="itemLink product-item")["href"]
        browser.visit(hemis_main_url + partial_img_url)
        partial_img_html = browser.html
        soup = bs( partial_img_html, "html.parser")
        img_url = hemis_main_url + soup.find("img", class_="wide-image")["src"]
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

    return hemisphere_image_urls
    
if __name__ == "__main__":
    print(scrape())