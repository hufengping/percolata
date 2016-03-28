'''
Created on 30 Aug 2015

@author: fengpinghu

'''
import json
data1 = {'b':789,'c':456,'a':123}
data2 = {'a':123,'b':789,'c':456}
d1 = json.dumps(data1,sort_keys=True,indent=4)
print d1