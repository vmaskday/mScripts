#!/usr/bin/python
import os
import sys
import subprocess
import re

def get_selinux_rul(filename):
    f = open(filename)
    lines = f.readlines()
    f.close()
    ruls = []
    reg = re.compile('.*avc.*denied')
    for l in lines:
        if reg.match(l) != None:
            #            denied = re.findall('denied {.*}',l)[0].split()[2]
            denied = re.findall('denied\s*{.*}',l)[0].split()[2]
            scont  = re.findall('scontext=\S*s0',l)[0].split(':')[2]
            tcont  = re.findall('tcontext=\S*s0',l)[0].split(':')[2]
            tclass = re.findall('tclass=\S*',l)[0].split('=')[1]
            onerul = (scont,tcont,tclass,denied)
            ruls.append(onerul)
    return list(set(ruls))

def rul_exists(one,filename):
    s,t,c,d = one
#    se_file = "device/qcom/sepolicy/common/"+s+".te"
#    if os.path.exists(se_file) == False:
#        se_file = "external/sepolicy/" +s+".te"
#        if os.path.exists(se_file) == False:
#            print "not fond:" + s
#            return False
    if os.path.exists(filename) == False:
        return False
    se = open(filename)
    lines = se.readlines()
    se.close()
    for l in lines:
        if l.find(t) > 0:
            if l.find(c) > 0:
                if l.find(d) > 0:
                    return True
    return False

def write_one_ruls(one_rule,filename):
    if os.path.exists(filename):
        f = open(filename,'a+')
        f.seek(2)
        f.writelines(one_rule)
        f.close()

def check_rules(ruls,filename):
    for r in ruls:
        s,t,c,d = r
        if rul_exists(r,filename):
            print "!!! some thing wrong !!!"
            print r
     #       sys.exit(-1)

def write_ruls( ruls,filename=None):
    for r in ruls:
        s,t,c,d = r
        if filename == None:
            se_file = "device/qcom/sepolicy/common/"+s+".te"
        else:
            se_file = filename
        if rul_exists(r,se_file):
            continue
        if rul_exists(r,"fail_rules.te"):
            continue
        if os.path.exists(se_file):
#            if s == "untrusted_app":
#                act = "dontaudit "
#            else:
#                act = "allow "
            act = "allow "
            onerule = act + s + " " + t + ":" + c +" { "+ d +" };\n"
            write_one_ruls(onerule,se_file)
            print onerule
        else:
            print "not fond file:"+se_file

def main():
    #subprocess.call(["adb","shell","dmesg"])
    if len(sys.argv) != 2:
        print "argc len " + len(sys.argv) 
        sys.exit()
    if os.path.exists(sys.argv[1]) == False:
        print "not fond file " + sys.argv[1]
        sys.exit()
    ruls = get_selinux_rul(sys.argv[1])
    #se_file = "device/qcom/sepolicy/common/"+s+".te"
    write_ruls(ruls)
    check_rules(ruls,"all_ruls.te")
    write_ruls(ruls,"all_ruls.te")

if __name__ == "__main__":
    main()
