#!/usr/bin/python

import os
import sys
import re

def find_fail_rul(log_buf):
    for log in log_buf:
        if re.search('report_failure.*neverallow',log) != None:
            filename = re.findall('neverallow on line \d+ of \S+',log)[0].split()[5]
            log = re.findall('violated by.*$',log)[0]
            rule = re.findall('\sallow.*$',log)[0]
            print rule.strip()
    return (filename,rule.strip())

def remove_rule(r,filename):
    print filename
    if os.path.exists(filename) == False:
        print "not file " + filename
        return
    f = open(filename,'r')
    lines = f.readlines()
    f.close()
    f = open(filename,'w')
    for l in lines:
        if r not in l:
            print l
            f.write(l)

def write_fail_rule(r,fname):
    f = open(fname,'a+')
    f.seek(2)
    f.write(r)
    f.write('\n')
    f.close()

def main():
    if os.path.exists(sys.argv[1]):
        logf = open(sys.argv[1])
        log_buf = logf.readlines()
        f,r = find_fail_rul(log_buf)
        write_fail_rule(r,"fail_rules.te")
        remove_rule(r,"device/qcom/sepolicy/common/untrusted_app.te")
    else:
        print "usag: fix_build_error.py  make.error.log"

if __name__ == "__main__":
    main()
