"""
connect MySQLdb and execute select 

"""
import MySQLdb

conn = MySQLdb.connect (host = "gc.baysensors.com", user = "fengping", passwd = "zip94303", db = "ud_production")
cursor = conn.cursor ()
cursor.execute ("select * from zone_person_labelings where placement_id=83 and sample_time>'2015-10-20' and updated_at<'2015-10-27'")
rows = cursor.fetchall()  

for row in rows:  
    print "%s %s" % (row[1],row[2])

print "Number of rows returned: %d" % cursor.rowcount 
cursor.close () 
conn.close () 