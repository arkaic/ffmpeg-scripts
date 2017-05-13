#!/usr/bin/env python
import argparse
from os import listdir, remove
import os.path
from os.path import basename, isfile, splitext
from random import shuffle
from subprocess import call

#--------------------------
# CONSTANTS AND VARIABLES |
#--------------------------

def get_args():
    """ Argument layout """
    p = argparse.ArgumentParser()
    p.add_argument('directory', help='directory')
    p.add_argument('-r', action='store_true', help='randomize')
    return p.parse_args()

def command(textfile_path, outpath):
    """ shell command layout """
    # return ['ffmpeg', '-f', 'concat', '-i', textfile_path, '-c', 'copy', outpath]
    return ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', textfile_path, '-c', 'copy', outpath]

def join(args):
    videonames = []
    filenames = listdir(args.directory)
    if not filenames:
        return error_and_kill("No files found in given directory. Is directory name correct?")

    for filename in listdir(args.directory):
        _, ext = splitext(filename)
        if ext and ext != 'txt':  # todo robustify
            videonames.append(os.path.join(args.directory, filename))

    if not videonames:
        return error_and_kill('No videos found in given directory. Filename formatting issues maybe?')

    out_filename, ext = splitext(basename(videonames[0]))
    out_filename += '_joined'
    outpath = '{}/{}{}'.format(args.directory, out_filename, ext)
    if isfile(outpath):
        return error_and_kill('joined video exists')

    textfile_str = ''
    if args.r:  # randomize
        shuffle(videonames)
    for videoname in videonames:
        textfile_str += "file '{}'\n".format(videoname)

    textfile_path = os.path.join(args.directory, 'files_to_join.txt')
    with open(textfile_path, 'w+') as tf:
        tf.write(textfile_str)

    call(command(textfile_path, outpath))
    remove(textfile_path)
    call(['open', outpath])

def error_and_kill(msg):
    print(msg)
    return False

if __name__ == '__main__':
    join(get_args())
