#--------------------------------------------------------------------------------
# File contains the Page class
# The Page class contains the methods that allow for the analysis of
# the webpages
#--------------------------------------------------------------------------------

from bs4 import BeautifulSoup as bs	# This ain't no BS though
import sys
import re

class Page():
    ''' Class that allows us to look through web pages more easily '''

    # list of the goofs
    errors = ["errors"]

    def __init__(self, name, dr):
	self.name = name
	self.dr = dr
	self.cool = [name]

    # the important function that will allow us to process the html page
    # note that key must be an array
    def process_page(self, key):
	doc = bs(self.dr.page_source)	# the webpage is assigned to doc
	for i in doc.findAll():	    # Loops through the html doc line by line
	    line = i.get('href')
	    if (line != None): 
		print '\nanalyzing: ' , line , '\n'
		for j in key:
		    match = re.search(j, str(line), re.I)
		    if match:
			print str(line), '\n'
			self.cool.append(line)

    def get_cool(self):
        return self.cool

