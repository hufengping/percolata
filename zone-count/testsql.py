"""
connect MySQLdb and execute select 
"""
import MySQLdb

conn = MySQLdb.connect (host = "gc.percolata.com", user = "fengping", passwd = "zip94303", db = "ud_production")
cursor = conn.cursor ()
cursor.execute ("select * from average_camera_zone_counts where placement_id=83 and start_time<'2015-12-18' and start_time>'2015-12-17'")
rows = cursor.fetchall()  

average_count = 0
for row in rows:  
    print "%s" % (row[5])
    average_count += row[5]
print "Number of average_count: %d" % average_count
cursor.close () 
conn.close () 
