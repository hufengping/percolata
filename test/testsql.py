import MySQLdb

conn = MySQLdb.connect (host = "162.222.178.71", user = "fengping", passwd = "zip94303", db = "ud_production")
cursor = conn.cursor ()
cursor.execute ("select * from zone_person_labelings where placement_id=83 and sample_time='2015-09-14 23:42:43'")
row = cursor.fetchone () 
print "line1:", row[0] 
cursor.close () 
conn.close () 