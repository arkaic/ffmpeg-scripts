#!/usr/bin/env python3
import argparse
import os
from random import randrange, shuffle
import subprocess

# --------- #
# CONSTANTS #
# --------- #
# Settable
SHUFFLE_STYLE      = 2

SHUFFLE_AT_EACH    = 1  # Fixed
SHUFFLE_AT_END     = 2  # Fixed
DEFAULT_DURATION   = 5  # per clip
DEFAULT_ITERATIONS = 10
PLAYLIST_EXT       = '.m3u'
ERROR_MARGIN       = 2

# argument layout
def _get_args():
    p = argparse.ArgumentParser()
    p.add_argument('videos_directory')
    p.add_argument('-d', '--duration', help='integer duration of each')
    p.add_argument('-i', '--iterations')
    return p.parse_args()

# -------------------------------------------------------------------------- #
#                                                                            #
# -------------------------------------------------------------------------- #

def _get_media_length(filepath):
    """ @return an integer value for length of video """
    cmd = []
    cmd.append('ffprobe')
    cmd.append('-v')
    cmd.append('error')
    cmd.append('-show_entries')
    cmd.append('format=duration')
    cmd.append('-of')
    cmd.append('default=noprint_wrappers=1:nokey=1')
    cmd.append(filepath)
    out, err = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()
    length = out.decode('utf-8')
    return int(float(length))

def build_montage_playlist(args):
    """ Create playlist given a directory & optional iterations and duration """

    if not os.path.isdir(args.videos_directory):
        print('Not a directory')
        return False

    duration = int(args.duration) if args.duration else DEFAULT_DURATION
    iterations = int(args.iterations) if args.iterations else DEFAULT_ITERATIONS
    
    # create playlist file path
    if args.videos_directory[-1] == '/':
        directory_basename = os.path.basename(args.videos_directory[:-1])
    else:
        directory_basename = os.path.basename(args.videos_directory)
    i = 1
    while True:
        playlist_path = os.path.join(args.videos_directory, '{}_{}s_X_{}_{}{}'.format(
            directory_basename, duration, iterations, i, PLAYLIST_EXT))
        if not os.path.isfile(playlist_path):
            break
        i += 1
    
    # store (filepath,length) tuples in memory before writing to playlist file
    filepaths_lengths = []
    for filename in os.listdir(args.videos_directory):
        _, ext = os.path.splitext(filename)
        if ext and ext != PLAYLIST_EXT:
            path = os.path.join(args.videos_directory, filename)
            filepaths_lengths.append((path, _get_media_length(path)))

    filepaths_lengths_to_write = []
    for _ in range(iterations):
        if SHUFFLE_STYLE == SHUFFLE_AT_EACH:
            shuffle(filepaths_lengths)
        for filepath_vidlength in filepaths_lengths:
            _, ext = os.path.splitext(filepath_vidlength[0])
            if ext and ext != PLAYLIST_EXT:
                filepaths_lengths_to_write.append(filepath_vidlength)
                
    if SHUFFLE_STYLE == SHUFFLE_AT_END:
        shuffle(filepaths_lengths_to_write)

    # create playlist file
    playlist_duration_sec = 0
    with open(playlist_path, 'w') as f:
        f.write('#EXTM3U\n')
        for filepath, vidlength in filepaths_lengths_to_write:
            if vidlength < duration:
                playlist_duration_sec += vidlength
            else:
                # write couple lines to playlist specifying random start point
                # running for 'duration'
                playlist_duration_sec += duration
                start = randrange(vidlength - 1 - duration)
                stop = start + duration
                assert stop < vidlength
                f.write('#EXTVLCOPT:start-time={}\n'.format(start))
                f.write('#EXTVLCOPT:stop-time={}\n'.format(stop))
            f.write(filepath + '\n')
    
    playlist_duration_min = int(playlist_duration_sec / 60)
    remaining_secs = playlist_duration_sec % 60
    print(playlist_path)
    print('Playlist size: ' + str(len(filepaths_lengths_to_write)))
    print('Playlist length: {}m {}s'.format(playlist_duration_min, remaining_secs))
    subprocess.run(['open', '-n', playlist_path])
    return True


if __name__ == '__main__':
    build_montage_playlist(_get_args())
