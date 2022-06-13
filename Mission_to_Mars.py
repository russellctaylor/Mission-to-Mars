#!/usr/bin/env python
# coding: utf-8

#10.3.3
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd



executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)



# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

#set up the HTML parser:

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# #the code for this will eventually be used in an application that will scrape live data with the click of a button—this site is dynamic and the articles will change frequently


slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title
#.get_text(). When this new method is chained onto .find(), only the text of the element is returned


# There are two methods used to find tags and attributes with BeautifulSoup:
# 
# .find() is used when we want only the first class and attribute we've specified.
# .find_all() is used when we want to retrieve all of the tags and attributes.

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


#  ### Featured Image
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

#Next, we want to click the "Full Image" button. 
# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel
#What we've done here is tell BeautifulSoup to look inside the <img /> tag for an image with a class of fancybox-image. Basically we're saying, 
#"This is where the image we want lives—use the link that's inside these tags."

#add the base URL to our code.
# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### 10.3.5 Scrape Mars Data: Mars Facts

#Instead of scraping each row, or the data in each <td />, 
#we're going to scrape the entire table with Pandas' .read_html() function.
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

#Pandas also has a way to easily convert our DataFrame back into HTML-ready code using the .to_html() function.
df.to_html()



#to end the session.
browser.quit()

#10.3.6 Export to Python
#To fully automate it, it will need to be converted into a .py file.

