#!/usr/bin/env python
import argparse
from os import path
from subprocess import call

#--------------------------
# CONSTANTS AND VARIABLES |
#--------------------------
TIME_PAIRS = "00:03:58.855 36.093; "
TIME_DELIMITER = '; '


def get_args():
    """ Argument layout """
    p = argparse.ArgumentParser()
    p.add_argument('video_path')
    p.add_argument('-e', action='store_true', help='Re-encode split (no stream copy)')
    p.add_argument('-t', help='optional text file path')
    return p.parse_args()

def command(reencode, start, vid, dur, out_chunk):
    """ Shell command layout """
    # TODO should error out of this function on any split error
    if reencode:
        return ["ffmpeg", "-ss", start, "-i", vid, "-t", dur, out_chunk]
        # call(["ffmpeg","-ss",start,"-i",vid,"-t",dur,"-c","copy",out_chunk])
    else:
        # stream copy
        return ["ffmpeg", "-ss", start, "-i", vid, "-t", dur, "-c", "copy", out_chunk]

def split(args, time_pairs=None):
    if args.video_path and not path.isfile(args.video_path):
        error('video_path is an invalid format')
    if args.t and not path.isfile(args.t):
        error("text file path is invalid")

    # make output directory
    video_filename = path.basename(args.video_path)
    out_directory = '{}/{}'.format(path.dirname(args.video_path),
                                   video_filename + '_chunks')
    if path.isdir(out_directory):
        i = 1
        while True:
            i += 1
            if not path.isdir('{}_{}'.format(out_directory, i)):
                out_directory = '{}_{}'.format(out_directory, i)
                break
    call(['mkdir', out_directory])

    # prefix for each output video chunk
    out_chunk_prefix = "{}/{}_chunk_".format(out_directory, video_filename)

    # if text file provided for times, parse that
    if args.t:
        with open(args.t) as f:
            time_pairs = f.readline().replace('"', '').split(TIME_DELIMITER)
    else:
        if time_pairs is None:
            time_pairs = TIME_PAIRS
        time_pairs = time_pairs.split(TIME_DELIMITER)

    # regex = "^\d{1,2}:\d{1,2}:\d{1,2}$"
    _, ext = path.splitext(args.video_path)
    i = 1
    for time_pair in time_pairs:
        if len(time_pair) <= 1:
            continue

        try:
            start, dur = time_pair.split(' ')
        except ValueError:
            error("time_pair '{}' didn't parse correctly'".format(time_pair[:-1]))

        # trim
        if dur[-1] == '\n':
            dur = dur[:-1]

        # output video chunk path
        while path.isfile(out_chunk_prefix + numstring(i) + ext):
            i += 1
        out_chunk = out_chunk_prefix + numstring(i) + ext

        call(command(args.e, start, args.video_path, dur, out_chunk))

    args.directory = out_directory
    return True

def numstring(num):
    if num < 10: return '0' + str(num)
    else: return str(num)

def error(msg):
    print(msg)
    return False



if __name__ == '__main__':
    args = get_args()
    split(args)
