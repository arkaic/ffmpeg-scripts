#!/usr/bin/env python3
import argparse
import datetime
import os

import splitter
import joiner

#--------------------------
# CONSTANTS AND VARIABLES |
#--------------------------
TIME_PAIRS = "00:44:21.540 2.1730000000002; 00:16:34.319 7.0110000000001; 00:19:48.753 10.74; 00:20:08.302 11.403"  # deprecated
TIME_DELIMITER = '; '


def parser():
    """ Argument layout """
    p = argparse.ArgumentParser()
    p.add_argument('video_path')
    p.add_argument('-e', action='store_true', help='Re-encode split (no stream copy)')
    p.add_argument('-t', help='optional text file path')    
    p.add_argument('-r', action='store_true', help='randomize chunks in joined output')
    return p

def get_args():
    return parser().parse_args()

def compilate(args):
    status = splitter.split(args, TIME_PAIRS)
    if status:
        joiner.join(args)
    else:
        print('error on split')

if __name__ == '__main__':
    args = get_args()
    compilate(args)
