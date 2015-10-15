__author__ = 'fengpinghu'

import MySQLdb as mdb
from database_access import util

GET_PLACEMENT_ID_SQL = "SELECT id FROM placements WHERE name='%s'"
GET_MTURK_RESULT = "SELECT * FROM zone_person_labelings WHERE sample_time LIKE '{}%' AND placement_id={}"

def get_placement_name(placement_name):
# get id for this placement
    db_con, db_cur = (None, None)
    mysql_conf = util.get_mysql_info()
    db_con = mdb.connect(
        host=mysql_conf['host'],
        user=mysql_conf['username'],
        passwd=mysql_conf['password'],
        db=mysql_conf['database'])
    db_cur = db_con.cursor()
    query = GET_PLACEMENT_ID_SQL % (placement_name)
    db_cur.execute(query)
    id = db_cur.fetchall()[0][0]
    return id

#query = GET_MTURK_RESULT.format(self.date_time, self.id)
#self.db_cur.execute(query)
#result = self.db_cur.fetchall()

if __name__ == "__main__":
	get_placement_name("8600165")