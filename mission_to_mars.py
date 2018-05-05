
# coding: utf-8

# In[3]:


### NASA Mars News

# Dependencies
import os
import time
from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
from splinter import Browser
import tweepy
import requests as req
import re


# In[8]:


# Create a dictionary for all of the scraped data 
mars_data = {}


# In[6]:


def marsNews():
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_ ="article_teaser_body").text
    output = [news_title, news_p]
    return output


# In[7]:


def marsImage():
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    return featured_image_url


# In[14]:


# URL of page to be scraped
url1 = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204=Latest"


# In[15]:


# Retrieve page with the requests module
response = requests.get(url1)
# Create BeautifulSoup object; parse with 'html.parser'
soup = BeautifulSoup(response.text, 'html.parser')


# In[16]:


news_title = soup.title.text
print(title)


# In[ ]:


paras = soup.find_all('p')
for para in paras:
    print(para.text)


# In[ ]:


news_title = soup.find(class_='BodyText')
print(title)
news_p = soup.find(class_='Paras')
print(para.text)


# In[ ]:


mars_data['news_title'] = news_title
mars_data['news_p'] = news_p


# In[ ]:


#Visit the URL for JPL's Space images
#splinter to navigate the site and find the image url for the current featured
#image and assign it to featured_image_url (use .jpg)
executable_path = {'executable_path' : 'chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)
url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(url2)


# In[ ]:


html = browser.html
soup = BeautifulSoup(html, "html.parser")


# In[6]:


# JPL Mars Space Images - Featured Image
def marsImage():
   image_url1 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
   browser.visit(image_url1)
   html = browser.html
   soup = BeautifulSoup(html, "html.parser")
   image = soup.find("img", class_="thumb")["src"]
   featured_image_url = "https://www.jpl.nasa.gov" + image
   mars_data ["featured_image_url"] = featured_image_url
   return featured_image_url
  
 


# In[7]:


#save a complete url string
featured_image_url = "https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA18851_hires.jpg"


# In[8]:


twitter_response = req.get("https://twitter.com/marswxreport?lang=en")
twitter_soup = BeautifulSoup(twitter_response.text, 'html.parser')


# In[9]:


tweet_containers = twitter_soup.find_all('div', class_="js-tweet-text-container")


# In[10]:


print(tweet_containers[0].text)
p = tweet_containers[0].text
type(p)


# In[40]:


mars_weather = "Sol 2036 (April 29, 2018), Sunny, high -5C/23F, low -72C/-97F, pressure at 7.28 hPa, daylight 05:24-17:20"
mars_data ["mars_weather"] = mars_weather


# In[41]:


#scrape the table containing facts about Mars
request_mars_space_facts = req.get("https://space-facts.com/mars/")
mars_space_table_read = pd.read_html(request_mars_space_facts.text)
df = mars_space_table_read[0]
df


# In[42]:



df= df.set_index(0).rename(columns={1: 'value'})
del df.index.name
mars_facts_df = df
mars_facts_df


# In[43]:


mars_facts_html = mars_facts_df.to_html()
mars_facts_html


# In[44]:


mars_facts_df.to_html('mars_table.html')
mars_data ["mars_facts_df"] = mars_facts_df


# In[45]:


hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(hemispheres_url)
html = browser.html
soup = BeautifulSoup(html, "html.parser")
mars_hemisphere = []

products = soup.find("div", class_ = "result-list" )
hemispheres = products.find_all("div", class_="item")

for hemisphere in hemispheres:
    title = hemisphere.find("h3").text
    title = title.replace("Enhanced", "")
    end_link = hemisphere.find("a")["href"]
    image_link = "https://astrogeology.usgs.gov/" + end_link    
    browser.visit(image_link)
    html = browser.html
    soup=BeautifulSoup(html, "html.parser")
    downloads = soup.find("div", class_="downloads")
    image_url = downloads.find("a")["href"]
    mars_hemisphere.append({"title": title, "img_url": image_url})
    mars_data ["mars_hemisphere"] = mars_hemisphere



# In[11]:


return mars_data

