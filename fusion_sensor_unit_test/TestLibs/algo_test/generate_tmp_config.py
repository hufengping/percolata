#!/usr/bin/env python

import os
import sys
from optparse import OptionParser
import json

CONFIG_TEMPLATE="./template.config"

def parse_option_args():
    parser = OptionParser()
    parser.add_option("-i","--input",help="the mturk result file.")
    parser.add_option("-o","--output",help="output tmp config file.")


    (options, args) = parser.parse_args()

    _in = options.input
    _out = options.output

    if not (_in==None or _out==None):
        return (_in, _out)
    else:
	print('''Usage: generate_tmp_config.py [options]

Options:
  -h, --help            show this help message and exit
  -i INPUT, --input=INPUT
                        the mturk result file.
  -o OUTPUT, --output=OUTPUT
                        output tmp config file..''')
	sys.exit(1)

def toString(obj):
    if type(obj) in [bool, int, float]:
	return str(obj)
    elif type(obj) is list:
	_l = list()
	for e in obj:
	    _l.append(toString(e))
        return _l
    elif type(obj) is dict:
	_d = dict()
	for (k,v) in dict.items():
	    _d[toString(k)]=toString(v)
	return _d
    else:
	raise TypeError("Unsupported type: %s" % str(type(obj)))

def get_tmp_config(inFile, outFile):
    with open(CONFIG_TEMPLATE,'r') as _tmpFile:
        with open(inFile,'r') as _inFile:
            with open(outFile,'w') as _outFile:
                _inConf = json.load(_inFile)["header"]
                _tmpConf = json.load(_tmpFile)
                _tmpConf["ESLOICount"]["0"]["expectedPersonArea"]\
                        = toString(_inConf["expected_person_area"])
                _tmpConf["ESLOICount"]["0"]["minPersonArea"]\
                        = toString(_inConf["min_person_area"])
                _tmpConf["ESLOICount"]["0"]["fTau"]\
                        = toString(_inConf["bg_shadow_ftau"])
                _tmpConf["ESLOICount"]["0"]["loiParam"]\
                        = toString(_inConf["tripline"])
                _tmpConf["ESLOICount"]["0"]["unwarp"]["distortF"]\
                        = toString(_inConf["unwarp"]["distortF"])
                _tmpConf["ESLOICount"]["0"]["unwarp"]["rectF"]\
                        = toString(_inConf["unwarp"]["rectF"])
                _tmpConf["ESLOICount"]["0"]["unwarp"]["resolutionFactor"]\
                        = toString(_inConf["unwarp"]["resolutionFactor"])
                _tmpConf["ESLOICount"]["0"]["unwarp"]["rotation"]\
                        = toString(_inConf["unwarp"]["rotation"])
                _tmpConf["ESLOICount"]["0"]["unwarp"]["useBilinear"]\
                        = toString(_inConf["unwarp"]["useBilinear"])
                _tmpConf["ESLOICount"]["0"]["unwarp"]["xcenteroffset"]\
                        = toString(_inConf["unwarp"]["xcenteroffset"])
                _tmpConf["ESLOICount"]["0"]["unwarp"]["ycenteroffset"]\
                        = toString(_inConf["unwarp"]["ycenteroffset"])
                _tmpConf["ESLOICount"]["0"]["unwarp"]["roiH"]\
                        = _inConf["unwarp"]["roiH"]
                _tmpConf["ESLOICount"]["0"]["unwarp"]["roiW"]\
                        = _inConf["unwarp"]["roiW"]
                _tmpConf["ESLOICount"]["0"]["unwarp"]["roiX"]\
                        = _inConf["unwarp"]["roiX"]
                _tmpConf["ESLOICount"]["0"]["unwarp"]["roiY"]\
                        = _inConf["unwarp"]["roiY"]

    		_outFile.seek(0)
		_outFile.truncate()
		json.dump(_tmpConf, _outFile, sort_keys=True)

if __name__ == '__main__':
    (_mturkResultFile, _tmpConfigFile) = parse_option_args()

    get_tmp_config(_mturkResultFile, _tmpConfigFile)
