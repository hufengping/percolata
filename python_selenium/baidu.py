#coding: gbk

from selenium import webdriver

browser = webdriver.Firefox()
browser.get("http://www.baidu.com")

print "browser maxsize"
browser.maximize_window()
browser.find_element_by_id("kw").send_keys("selenium")
browser.find_element_by_id("su").click()

browser.quit()
