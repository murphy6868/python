import urllib, lxml.html
from selenium import webdriver
import time

u='http://www.ptt.cc/bbs/Boy-Girl/'
r=urllib.request.Request(u,headers={'User-Agent':''})
data=urllib.request.urlopen(r).read()
t=lxml.html.fromstring(data.decode('utf-8'))
target = "‹ 上頁"
for link in t.xpath('//a'):
    #print(link.text,link.attrib.get('href')) 
    if link.text == target:
        url = link.attrib.get('href')
        print(url[url.index("index") + 5:url.index(".html")])
    
    
target1 = "爆"
for link in t.xpath('//span'):
    #print(link.text,link.attrib.get('href')) 
    if link.text == target1:
        bao = link.getparent().getparent().getchildren()[2].getchildren()[0]
        print(bao.text, bao.attrib.get('href'))



URI='http://www.ptt.cc/bbs/Boy-Girl/'
driver=webdriver.Chrome() # Chrome, PhantomJS, etc.
driver.get(URI)
driver.save_screenshot('0.png')
string = '.png'
for j in range(3):
    url = driver.current_url
    driver.get(url)
    btn=driver.find_element_by_link_text('‹ 上頁')
    btn.click()
    time.sleep(1)
    name = str(j + 1) + string
    driver.save_screenshot(name)
