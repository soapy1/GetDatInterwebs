from bs4 import BeautifulSoup as bs	# This ain't no BS though
import sys
import re

class Page():
    ''' Class that allows us to look through web pages more easily '''

    # list of the goofs
    errors = ["errors"]
    # list of cool things
    cool = ["urls"]

    def __init__(self, name, dr):
	self.name = name
	self.dr = dr

    # the important function that will allow us to process the html page
    def process_page(self, key):
	doc = bs(self.dr.page_source)	# the webpage is assigned to doc
	for i in doc.findAll():	    # Loops through the html doc line by line
	    try:
                self.cool.append(i.get('href')) # tries to add it to cool list
	    except:		    # So it does not goof
		self.errors.append(sys.exc_info()[0])	

    # function that analyzes the string
    def analyze(line, key):
	for i in key:				    # goes through the keys
	    match = re.search(i, str(line), re.I)   # executes regex
	    if match:				    # checks if match
		#try:
		self.cool.append(tmp) # add it to cool list
		#except:				    # so it does not goof
		#    self.errors.append(sys.exc_info()[0])
	    else:
		pass				    # don't care about this 
	    del tmp

    def print_cool(self):
	return self.cool
	#print self.cool 
	#print '\n' 
	#print self.errors 

