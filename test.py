# script for testing the script

import page
from selenium import webdriver as wd

a = []

dr = wd.Firefox()
web = "http://xkcd.com"
dr.get(web)
pg = page.Page(web, dr)
pg.process_page("about")
a = pg.print_cool()
print a
dr.quit()

