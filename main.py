#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import actions

if __name__ == '__main__':
    args_len = len(sys.argv)
    if args_len < 4:
        print("Missing enough arguments, at least 3: Uid, Pwd, qmsgkey")
        exit(1)
    
    if args_len > 4:
        print("Too many arguments")
        exit(1)

    Uid = sys.argv[1]
    Pwd = sys.argv[2]
    actions.qmsgkey = sys.argv[3]
    actions.run(Uid,Pwd)