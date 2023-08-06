# -*- coding:utf-8 -*-
# writer: Mia at 16. 9. 9, 
# last revision: 오후 11:22

from time import strftime,localtime

def print_time():
    print (strftime("[%H:%M:%S]", localtime()),)

def print_time_msg(msg):
    print (strftime("[%H:%M:%S]", localtime()), msg)