__author__ = 'fengpinghu'
#!/usr/bin/env python

from optparse import OptionParser
import sys
def main():
    p = OptionParser()
    p.add_option('-n','--name',dest='person_name',help='person\'s name',default='person1')
    p.add_option('-a','--age',default=30, help='person\'s age')
    p.add_option('-j','--job',default='software engineer', help='person\'s job')
    options, args = p.parse_args()
    print 'Hello %s' %options.person_name, ', age is %d' %int(options.age), ',job is %s' %options.job

if __name__ == '__main__':
    main()
