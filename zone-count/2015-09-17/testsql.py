"""
connect MySQLdb and execute select 

"""
import MySQLdb

conn = MySQLdb.connect (host = "162.222.178.71", user = "fengping", passwd = "zip94303", db = "ud_production")
cursor = conn.cursor ()
cursor.execute ("select * from zone_person_labelings where placement_id=83 and sample_time>'2015-09-18' and updated_at<'2015-09-19' and x IS NOT NULL")
rows = cursor.fetchall()  

for row in rows:  
    print "%s" % (row[1])

print "Number of rows returned: %d" % cursor.rowcount 
cursor.close () 
conn.close () 