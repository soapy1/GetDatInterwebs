#--------------------------------------------------------------------------------
# File contains the Page class
# The Page class contains the methods that allow for the analysis of
# the webpages
#--------------------------------------------------------------------------------

from bs4 import BeautifulSoup as bs	# This ain't no BS though
import sys
import re
import dbconn
import datetime

class Page():
    ''' Class that allows us to look through web pages more easily '''

    # list of the goofs
    errors = ["errors"]

    def __init__(self, name, dr):
	self.name = name	# the name of the website
	self.dr = dr		# the webdriver object
	self.cool = [name]	# array of cool links
	self.db = dbconn.Dbconn('localhost','user','password','getdatinterwebs')

    # the important function that will allow us to process the html page
    # note that key must be an array
    def process_page(self, key, rid):
	num_matches = 0
	doc = bs(self.dr.page_source)	# the webpage is assigned to doc
	for i in doc.findAll():	    # Loops through the html doc line by line
	    line = i.get('href')
	    if (line != None): 
		print '\nanalyzing: ' , line , '\n'
		for j in key:
		    match = re.search(j, str(line), re.I)
		    if match:
			num_matches += 1
			print str(line), '\n'
			q_main = "insert into main values (null, '"+ self.name+"', '" + j + "', '" + line + "', '" + str(rid) + "')"
			self.db.insert_query(q_main)	# inserts into db
	return num_matches
#	cur_date = datetime.datetime.now()
#	cur_date = str(cur_date)
#	q_time = "insert into times values(null, '" + cur_date + "', '"+ str(num_matches) +"')"
#	self.db.insert_query(q_time)

    def finish(self):
	self.db.close_conn()
	
