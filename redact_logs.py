#!/usr/bin/env python

import argparse
import datetime
import gzip
import logging
import os

"""
Redacts lines from files (likely log) containing the specified fields.

"""


def process_files(args):
    """processes files from the argument removing lines and log the results 
    """

    for f in args.files:

        # log start
        logging.info('Processing file: ' +f)
        start_time = datetime.datetime.now() #.replace(microsecond=0)
           
        new_name = 'redacted_' + f
        
        try:
            # open the original file and set up a gzipped output file
            with gzip.open(f, 'r') as f_in, gzip.open(new_name, 'wb') as f_out:
                out_exists = True # track if the file exists for exception handling
                total_lines = 0
                redacted_lines = 0
                # start iterating line by line
                for line in f_in: 
                    total_lines += 1
                    # look for everything after the delimiter for data
                    fields = line.split(args.field)
                    # if present we need to examine further
                    if len(fields) == 2:
                        # split the field elements and look for keys we ant to redact
                        field_elements = dict(x.split('=') for x in fields[1].split(args.delimiter))
                        if any(k in field_elements for k in args.keys): 
                            redacted_lines += 1
                            f_out.write('Log entry Redacted\n')
                        else:
                            f_out.write(line)
                    # line doesn't have a delimiter for data
                    else:
                        f_out.write(line)

        except Exception:
            logging.error('Error processing file ' +f +' to file ' +new_name)
            # try to remove the new file if there's an error
            try:
                f_out.close()
                os.unlink(f_out)
                out_exists = False
            finally:
                try:
                  f_in.close()
                  if out_exists:
                      f_out.close()
                except Exception:
                    logging.error("Error closing files")

        update_file_attr(f, new_name)
        # log before going to the next file  
        end_time = datetime.datetime.now() #.replace(microsecond=0)
        logging.info('Finished processing: ' +f  +' in ' + str(end_time - start_time) +'.  Redacted ' +str(redacted_lines) +' out of ' +str(total_lines) +' lines.')
                        

def update_file_attr(source, dest ):
    """attempts to copy ownership and timestamps from one file to another
    """
    try:
        stat = os.stat(source)
        uid = stat.st_uid
        gid = stat.st_gid
        atime = stat.st_atime
        mtime = stat.st_mtime
        ctime = stat.st_ctime
        size = stat.st_size
        os.utime(dest, (atime, mtime))
    except Exception:
        logging.error('Error setting metadata for file: ' +dest)

def parse_args():
    """parse the arguments from the command line
    """
    parser = argparse.ArgumentParser(description='Redact lines from input gzip file containing fields passed as parameter')
    parser.add_argument('-f', '--files', nargs='+', required=True, help='<Required> list of files delimited with spaces')
    parser.add_argument('-k', '--keys', nargs='+', required=True, help='<Required> list of fields that will cause a line to be redacted')
    parser.add_argument('-l', '--log', default='redacted.log', help='<Optional> location of log file. default is redacted.log')
    parser.add_argument('--field', default='Fields:', help='<Optional>String that begins fields to examine')
    parser.add_argument('-d', '--delimiter', default=', ', help='<Optional> Field delimiter inside of fields to examine')
    return parser.parse_args()

def main(args):
    logging.basicConfig(filename=args.log, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    process_files(args) 

if __name__ == '__main__':
    arguments = parse_args()
    main(arguments)
