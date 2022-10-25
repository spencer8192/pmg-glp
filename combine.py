#!/usr/bin/env python3

import csv
import sys
import os

def combine(filenames, outfile=None):
    '''
    Combine several csv files with the same headers. Adds a column 
    indicating the filename from which each row originated.

    filenames -- a sequence of strings, each a path to a csv file
    outfile -- the file to print the resulting csv to (default: stdout)
    '''
    if len(filenames) < 1:
        raise Exception("Error: No filenames specified")
    if outfile is None:
        outfile = sys.stdout
    else:
        outfile = open(outfile, 'w')
    # Ensure that all the input files have the same header.
    # This is sufficient to ensure expected behavior.
    first_header = None
    for filename in filenames:
        with open(filename) as csvfile:
            header = csvfile.readline()
        if first_header is None:
            first_header = header
        if header != first_header:
            raise Exception('Error: Files have different headers: '\
                             f'{filenames[0]}, {filename}')
    # Print the updated header to the outfile.
    # Limitation: If the input files use a different convention for their
    # headers, the filename column header will not follow it.
    header = header.rstrip() + ',"filename"'
    print(header, file=outfile)
    # Print rows from each csv
    for filename in filenames:
        with open(filename) as csvfile:
            reader = csv.reader(csvfile)
            reader = iter(reader)
            next(reader) # Skip header row
            for row in reader:
                if len(row) > 0:
                    row[-1] = row[-1].rstrip()
                # Add a column for the base filename
                # Limitation: Two files can have the same basename
                row.append(os.path.basename(filename))
                print(','.join(row), file=outfile)
    outfile.close()
            

if __name__ == '__main__':
    filenames = sys.argv[1:]
    combine(filenames)