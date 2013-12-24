# ------------------------------------------------------------------------------
# File contains the methods for connecting to the database
#--------------------------------------------------------------------------------

import MySQLdb
import sys

class Dbconn():

    # opens up a connection to the mysql db
    def __init__(self, ho, usr, pswd, d):
        self.db = MySQLdb.connect(host=ho, user=usr, passwd=pswd, db=d)

    # Suppose to be used to get data from the database
    def read_query(self, q):
	r_arr = []
	cur = self.db.cursor()
	try:
            cur.execute(q)    # execute the query
	    for i in cur.fetchall():	    # puts the result of the query
		r_arr.append(i)		    #  into an array
	    cur.close()			    # no need for this
	    return r_arr		    # returns the result
	except:				    # so it does not goof
	    print 'Ohh no! An error occured\n'
	    print sys.exc_info()[0]	

    # Suppose to be used to commit data to the database
    def insert_query(self, q):
	cur = self.db.cursor()
	try:
	    cur.execute(q)	    # executes the query
	    self.db.commit()	    # commits the query
	    cur.close()		    # no need for this
# hopefully the database is good at keeping relationships and does not have commitment issues, lol...
	except:			    # so it does not goof
	    print 'Ohh no! An error occured\n'
	    print sys.exc_info()[0]

    # Closes up the connection to the database 
    def close_conn(self):
	self.db.close()


