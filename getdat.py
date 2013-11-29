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
import sys

# These are the sites that I like
sites = ["http://www.io9.com", "http://www.wired.com", "http://www.economist.com", "http://www.hackaday.com", "dgdhgf"]

# Dictionary of sites that were reached split into good (successfully reached)
# and bad (not reached).  Will be used primarily to generate a report
reached = {"good":[], "bad":[]};

def main():
    dr = wd.Firefox()	# Light the fire under the fox

    for i in sites:	# Loops through the sites 
    
    # TODO: When tested, the try/except did not catch that "dgdhgf" is 
    #	    not a web page.  Fix this!
	try:
	    dr.get(i)			# Goes to the site
	    reached["good"].append(i)	# adds to successful list
	except:				# So it does not goof
	    er = "Ooops, an error occured " + sys.exc_info()[0]
	    print er
	    reached["bad"].append([i, er])	# add to the unsuccessful list

    dr.close()	    # Close the window because we no longer need it
    gen_report()    # Generates report
    print "All done-ski"
	
	
# Generates a report to the file interwebs.txt based on the data in the
# dictionary reached
def gen_report():
    out = open('interwebs.txt', 'w')	# Opens a file to write to

    # For the "good" part of the dictionary
    out.write("Successfully reached the following pages: \n")
    for i in reached["good"]:
	 out.write( i + '\n')

    # For the "bad" part of the dictionary
    out.write("\nDone goofed for the following pages: \n")
    for i in reached["bad"]:
	out.write(i[0] + " Exception: " + i[1] + '\n')
	

if __name__ == "__main__":
    main()
