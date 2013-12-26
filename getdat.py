# /usr/bin/python2
#http://www.sitepoint.com/understanding-sql-joins-mysql-database/
#-----------------------------------------------------------------------------
# A script that finds the cool internet things
#
# Done  step 1: Create thing that parses web pages
#TODO:	step 2: implement search algorithm with python regex
#	step 3: search more than just what is in your list
#	step 4: android
#
# Jokes search algorithm:
# 	basically just has a list of key words.  finds all the href's on a 
#	web page (hope they are at least kind of descriptive) and compares 
#	them to the list of key words.  
#	Still OUTSTANDING, removing the useless urls by another set of keys
# Proposed revised algorithm
#	search the whole document for key words.  When one is found take the 
# 	href before and after it, along with that matching part of the document

# Next steps (ie what I will do tomorrow)
# 	set it up with a sql database 
#	db structure (table main):
#id int(10), website varchar(255), matching_tag varchar(255), link varchar(255), rid int(10)
#create table main (id int(10) auto_increment, website varchar(255), matching_tag varchar(255), link varchar(255), rid int(10), primary key (id) );
#
#	db structure (table times):
#id int(10), time_run int(10), number_of_results int(10), rid int(10)
#create table times (id int(10) auto_increment, time_run datetime, number_of_results int(10), rid int(10), primary key (id) );
#
#	generate reports from database 
#	reason for two tables is to practice table joins	
#------------------------------------------------------------------------------

from selenium import webdriver as wd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys 
from bs4 import BeautifulSoup
import sys
import page
import datetime
import dbconn

# These are the sites that I like
sites = ["http://www.io9.com", "http://www.wired.com", "http://www.economist.com", "http://www.hackaday.com"]
#sites = ["http://www.hackaday.com"]


# These are the cool keywords that I am looking for
key = ["robots", "waterloo", "toronto", "ottawa", "cool", "computer", "arduino", "python", "html", "css", "php", "ruby", "rails", "android", "java", "funny", "mit", "linux", "ubuntu", "arch"]
# The regex version of the cool keywords that I am looking for
# Really regex does not need to be user here but yolo
key_regex = ["^robot", "waterloo$", "toronto$", "ottawa$", "^cool$", "computer", "arduino", "python", "^html", "^css", "^php", "ruby", "rails", "android", "java", "^mit$", "linux", "ubuntu", "arch$", "^ai$", "artificial intelligence", "satellite", "^dr.who$", "^doctor who$"]
# The anti regex key with the purpose to filter out anything that may be annoying
# based on what the key_regex has.  Probably not the most efficient thing but
# my regex skills are not that good so we get around that be doing this

# Dictionary of sites that were reached split into good (successfully reached)
# and bad (not reached).  Will be used primarily to generate a report
reached = {"good":[], "bad":[]};
# dictionary where the url to all the cool articles will be stored
#cool_pages = [];

db = dbconn.Dbconn('localhost','user','password','getdatinterwebs')
num_matches = 0
rid = 0

def main():
    global cool_pages
    dr = wd.Firefox()	# Light the fire under the fox
    get_rid()

    for i in sites:	# Loops through the sites
	global num_matches 
	try:
	    dr.get(i)			# Goes to the site
	    reached["good"].append(i)	# adds to successful list
	    pg = page.Page(i, dr)	# creates page object
	    num_matches += pg.process_page(key_regex, rid)  # processes the page
	    pg.finish()
	    #pg.process_page(["feed"])
	    #cool_pages += pg.get_cool() 
	except:				# So it does not goof
	    er = "Ooops, an error occured " , sys.exc_info()[0]
	    print er
	    reached["bad"].append([i, er])	# add to the unsuccessful list
	
   
    update_times_table()
    dr.close()	    # Close the window because we no longer need it
    gen_report()    # Generates report
    print "All done\n"
    dr.quit()
    db.close_conn() 

def get_rid():
    global rid
    try:
	q = "select max(rid) from times"
        rid = db.read_query(q)[0][0] + 1
    except:
	print "Ooops, an error occured", sys.exc_info()[0]
        rid = 0

def update_times_table():
	cur_date = datetime.datetime.now()
	cur_date = str(cur_date)
	q_time = "insert into times values(null, '" + cur_date + "', '"+ str(num_matches) +"', '" + str(rid) + "')"
	db.insert_query(q_time)


# Generates a report to the file interwebs.txt based on the data in the
# dictionary reached
def gen_report():

    # TODO: make more "full" reports

#select times.time_run, main.website, main.link, times.rid, main.rid from times inner join main on main.rid = 0 and times.rid = 0 GROUP BY main.website;

    out = open('interwebs.txt', 'w')	# Opens a file to write to

    # for to db
    inf_q = "select times.time_run, main.link from times inner join main on main.rid = " + str(rid) + " and times.rid = " + str(rid);
    inf = db.read_query(inf_q)
    
    out.write(str(inf[0][0]))
    # For the "good" part of the dictionary
    out.write("\nSuccessfully reached the following pages: \n")
    for i in reached["good"]:
	 out.write( i + '\n')

    # For the "bad" part of the dictionary
    out.write("\nDone goofed for the following pages: \n")
    for i in reached["bad"]:
	a = i[0] , " Exception: " , i[1] , '\n'
	out.write(str(a))

    # For the bamf cool pages
    out.write("\nThe very nice pages are the follwing:  \n")
    for i in inf:
	out.write(i[1])
	out.write('\n\n')
	 
    
'''
    out.write(time.strftime("%d/%m/%Y, %H:%M:%S"))
    # For the "good" part of the dictionary
    out.write("\nSuccessfully reached the following pages: \n")
    for i in reached["good"]:
	 out.write( i + '\n')

    # For the "bad" part of the dictionary
    out.write("\nDone goofed for the following pages: \n")
    for i in reached["bad"]:
	a = i[0] , " Exception: " , i[1] , '\n'
	out.write(str(a))

    # For the bamf cool pages
    out.write("\nThe very nice pages are the follwing:  \n")
    for i in cool_pages:
	out.write('\n')
	out.write(i + '\n')
'''


if __name__ == "__main__":
    main()
