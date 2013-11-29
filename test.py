# script for testing the script

import page
from selenium import webdriver as wd

dr = wd.Firefox()
web = "http://xkcd.com"
dr.get(web)
pg = page.Page(web, dr)
pg.process_page("about")
pg.print_output()
dr.quit()

