import os
import sys
import MySQLdb as mdb
from database_access import util
from download_gsDir_to_local import GSManager
from protobuf_messages.zone_count_data_pb2 import Video

BUCKET_NAME = 'percolata-data'

REMOTE_DIR = 'data/combined/zone_count/'
LOCAL_WORK_DIR = './tmp/'

GET_PLACEMENT_ID_SQL = "SELECT id FROM placements WHERE name='%s'"
GET_MTURK_RESULT = "SELECT * FROM zone_person_labelings WHERE sample_time LIKE '{}%' AND placement_id={}"

class ErrorRateCounter:
    def __init__(self, placement, date_time):
        self.placement_name = placement
        self.date_time = date_time
        self.gs_worker = GSManager(BUCKET_NAME)

        # set remote dir of proto files
        self.remote_dir = REMOTE_DIR + placement + '/' + date_time + '/'
        print self.remote_dir
        if not os.path.exists(LOCAL_WORK_DIR):
            os.mkdir(LOCAL_WORK_DIR)

        # key time, value [proto count,mturk count]
        self.cnt_dict = {}

        # configurate db, get id for this placement
        self.db_con, self.db_cur = (None, None)
        mysql_conf = util.get_mysuhql_info()
        self.db_con = mdb.connect(
            host=mysql_conf['host'],
            user=mysql_conf['username'],
            passwd=mysql_conf['password'],
            db=mysql_conf['database'])
        self.db_cur = self.db_con.cursor()
        query = GET_PLACEMENT_ID_SQL % (self.placement_name)
        self.db_cur.execute(query)
        self.id = self.db_cur.fetchall()[0][0]

    def run(self):
        # download proto files
        self.down_proto_files()

        # process each file
        fl = os.listdir(LOCAL_WORK_DIR)
        for proto_file in fl:
            print proto_file
            self.analyse_one_proto(LOCAL_WORK_DIR + proto_file)

        # get mturk result
        self.get_mturk_result()

    def down_proto_files(self):
        self.gs_worker.download_dir_to_local(self.remote_dir, LOCAL_WORK_DIR)

    def analyse_one_proto(self, f):
        # f='data-combined-zone_count-8600125-2015-09-14-8600125_zone_count_2015-09-14-15-38-04_0.zoneCountproto'
        v = Video()
        fin = file(f)
        content = fin.read()
        v.ParseFromString(content)

        for frame in v.frame:
            tmp_key = str(frame.time)
            if tmp_key in self.cnt_dict:
                self.cnt_dict[tmp_key][0] += frame.count
            else:
                # -1 means no mturk result
                self.cnt_dict[tmp_key] = [frame.count, -1]

    def get_mturk_result(self):
        query = GET_MTURK_RESULT.format(self.date_time, self.id)
        self.db_cur.execute(query)
        result = self.db_cur.fetchall()
        # row[1] is time, row[4] is x, if there is no box on this frame, x would be null.
        for row in result:
            # unify the time format
            tmp_time = str(row[1]).strip().replace(' ', '-')
            tmp_time = tmp_time.replace(':', '-')
            count_flag = 1 if row[4] != None else 0
            if tmp_time in self.cnt_dict:
                if count_flag:
                    if self.cnt_dict[tmp_time][1] == -1:
                        self.cnt_dict[tmp_time][1] = 1
                    else:
                        self.cnt_dict[tmp_time][1] += 1
                else:
                    if self.cnt_dict[tmp_time][1] == -1:
                        self.cnt_dict[tmp_time][1] = 0

    def show_result(self):
        # calculate the error rate
        err_rate, tmp_cnt = 0.0, 0
        for key in self.cnt_dict:
            print key, self.cnt_dict[key]
            cnt_result, mturk_result = self.cnt_dict[key]

            if mturk_result == -1:  # no mturk result
                continue

            if mturk_result == 0 and cnt_result == 0:  # both 0, error is 0
                tmp_cnt += 1
                err_rate += 0
            elif mturk_result == 0 and cnt_result != 0:  # mturk result is 0, error rate = algo count
                tmp_cnt += 1
                err_rate += cnt_result
            elif mturk_result != 0 and cnt_result != 0:  # neither is 0, error rate = diff / mturk result
                tmp_cnt += 1
                err_rate += abs(mturk_result - cnt_result) * 1.0 / mturk_result
            else:  # mturk is valid, but no algo result, neglect temporarily
                pass

        final_err_rate = err_rate / tmp_cnt if tmp_cnt != 0 else 0
        print 'final error rate', final_err_rate

        # delete files
        fl = os.listdir(LOCAL_WORK_DIR)
        for f in fl:
            os.remove(LOCAL_WORK_DIR + f)


if __name__ == '__main__':
    placement_name = '8600125'
    date_time = '2015-10-23'
    if len(sys.argv) == 3:
        placement_name, date_time = sys.argv[1], sys.argv[2]
    t = ErrorRateCounter(placement_name, date_time)
    t.run()
    t.show_result()
