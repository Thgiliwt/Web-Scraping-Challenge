from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

#set up def as 'scrape()'
def scrape():
    executable_path = {'executable_path':ChromeDriverManager().install()}
    browser = Browser('chrome',**executable_path,headless=False)

    #NASA Mars News ############################################################################
    url_news = 'https://redplanetscience.com/'
    browser.visit(url_news)
    time.sleep(1)

    html = browser.html
    soup = bs(html,'html.parser')
    
    news_list = soup.find_all('div',class_='list_text')
    latest_news = news_list[0]
    
    
    news_title = latest_news.find('div',class_='content_title').text
    news_p = latest_news.find('div',class_='article_teaser_body').text

    #JPL Mars Space Images - Featured Image ####################################################
    url_img = 'https://spaceimages-mars.com/'
    browser.visit(url_img)
    time.sleep(1)

    html = browser.html
    soup = bs(html,'html.parser')
    browser.links.find_by_partial_text('FULL IMAGE').click()

    #As 'soup' only work for a single page, hence need to redefine the page and the bs4 method
    html = browser.html
    soup = bs(html,'html.parser')
    img_path = soup.find('img',class_='fancybox-image')['src']
    featured_image_url = url_img + img_path

    #Mars Facts ################################################################################
    url_tables = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url_tables,flavor='html5lib')

    mars_profile = tables[0]

    mars_profile = mars_profile.rename(columns = {0:'Description',1:'Mars',2:'Earth'})
    mars_profile.set_index('Description',inplace=True)
    mars_table = mars_profile.to_html()

    #Mars Hemispheres ##########################################################################
    url_hemis = 'https://marshemispheres.com/'
    browser.visit(url_hemis)
    time.sleep(1)

    html = browser.html
    soup = bs(html,'html.parser')

    all_four_links = soup.find_all('div',class_='description')


    hemisphere_image_urls = []

    for link in all_four_links:
        sub_dict = {}
        link_title = link.find('h3').text
        sub_dict['title'] = link_title
        browser.links.find_by_partial_text(link_title).click()
        
        html_sub = browser.html
        soup_sub = bs(html_sub,'html.parser')
        
        img_path = soup_sub.find_all('li')[0].a['href']
        img_url = url_hemis + img_path
        sub_dict['img_url'] = img_url
        
        hemisphere_image_urls.append(sub_dict)

        browser.back()
        
    #insert values into a dict with 2 key-value pairs and then put all dicts into a list
    # hemisphere_image_urls = []
    # sub_dict = {}
    # for x in range(4):
    #     sub_dict['title'] = all_four_titles[x]
    #     sub_dict['img_url'] = img_urls[x]
    #     hemisphere_image_urls.append(sub_dict)
    #     sub_dict = {}

    #store all scraped info into a list ########################################################
    mars_dict = {'latest_news_title':news_title,
                 'news_content':news_p,
                 'JPL':featured_image_url,
                 'table_info':mars_table,
                 'four_urls':hemisphere_image_urls}
    

    browser.quit()

    return mars_dict
