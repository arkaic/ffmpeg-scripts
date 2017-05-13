#!/usr/bin/env python
import argparse

import splitter
import joiner

#--------------------------
# CONSTANTS AND VARIABLES |
#--------------------------
TIME_PAIRS = "00:50:02.665 4.597; 00:46:31.043 7.567; 00:44:34.376 7.264; 00:44:51.994 8.2459"


def get_args():    
    """ Argument layout """
    p = argparse.ArgumentParser()
    p.add_argument('video_path')
    p.add_argument('-e', action='store_true', help='Re-encode split (no stream copy)')
    p.add_argument('-t', help='optional text file path')    
    p.add_argument('-r', action='store_true', help='randomize chunks in joined output')
    return p.parse_args()

if __name__ == '__main__':
    args = get_args()
    status = splitter.split(args, TIME_PAIRS)
    if status:
        joiner.join(args)
    else:
        print('error on split')
