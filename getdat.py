#! /usr/bin/python2

#-----------------------------------------------------------------------------
# A script that finds the cool internet things
#
#TODO:  step 1: Create thing that parses web pages
#	step 2: implement search algorithm with python regex
#	step 3: search more than just what is in your list
#	step 4: android
#------------------------------------------------------------------------------

from selenium import webdriver as wd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys 
from bs4 import BeautifulSoup
import sys
import page
import time

# These are the sites that I like
#sites = ["http://www.io9.com", "http://www.wired.com", "http://www.economist.com", "http://www.hackaday.com"]
sites = ["http://www.io9.com"]


# These are the cool keywords that I am looking for
key = ["robots", "waterloo", "toronto", "ottawa", "cool", "computer", "arduino", "python", "html", "css", "php", "ruby", "rails", "android", "java", "funny", "mit", "linux", "ubuntu", "arch"]
# The regex version of the cool keywords that I am looking for
# TODO: make proper regex
key_regex = ["robots", "waterloo", "toronto", "ottawa", "cool", "computer", "arduino", "python", "html", "css", "php", "ruby", "rails", "android", "java", "funny", "mit", "linux", "ubuntu", "arch"]

# Dictionary of sites that were reached split into good (successfully reached)
# and bad (not reached).  Will be used primarily to generate a report
reached = {"good":[], "bad":[]};
# dictionary where the url to all the cool articles will be stored
cool_pages = {};

def main():
    dr = wd.Firefox()	# Light the fire under the fox

    for i in sites:	# Loops through the sites 
	try:
	    dr.get(i)			# Goes to the site
	    reached["good"].append(i)	# adds to successful list
	    pg = page.Page(i, dr)	# creates page object
	    pg.process_page(key_regex)	# processes the page for stuff
	    tmp_list = pg.print_cool()	# gets the results of the processing
	    tmp_dict = {i:tmp_list}	# make a temporary oxford
	    del tmp_list		# Life Tip 1: nobody needs lists
	    cool_pages.update(tmp_dict)	# update the dictionay
	    del tmp_dict		# Life Tip 2: nobody kneeds dictionarys
					# lol, spelling mistakes because of no
					# dictionaries
	except:				# So it does not goof
	    er = "Ooops, an error occured " + sys.exc_info()[0]
	    print er
	    reached["bad"].append([i, er])	# add to the unsuccessful list

    dr.close()	    # Close the window because we no longer need it
    gen_report()    # Generates report
    print "All done-ski\n"
    print cool_pages
    dr.quit()	
	
# Generates a report to the file interwebs.txt based on the data in the
# dictionary reached
def gen_report():
    out = open('interwebs.txt', 'w')	# Opens a file to write to

    out.write(time.strftime("%d/%m/%Y/%H:%M:%S"))
    # For the "good" part of the dictionary
    out.write("\nSuccessfully reached the following pages: \n")
    for i in reached["good"]:
	 out.write( i + '\n')

    # For the "bad" part of the dictionary
    out.write("\nDone goofed for the following pages: \n")
    for i in reached["bad"]:
	out.write(i[0] + " Exception: " + i[1] + '\n')

    # For the bamf cool pages
    out.write("\nThe very nice pages are the follwing:  \n")
    #TODO: don't pass an array
    for i in cool_pages:
	for j in cool_pages[i]:
	    if j != None:	    # cuts the crap
		out.write('\n')
		out.write(j)
#    	out.write(cool_pages[i])

if __name__ == "__main__":
    main()
