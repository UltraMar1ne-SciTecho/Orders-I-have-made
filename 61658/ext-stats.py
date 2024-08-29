#!/usr/bin/env python3

import os
import sys
import argparse

from collections import defaultdict


# Function to scan files and collect statistics
def file_stats(directory):
    # If no directory is given, use the current working directory
    if not directory:
        directory = '.'

    # Dictionary to hold file stats
    stats = defaultdict(lambda: {'count': 0, 'max_size': 0, 'total_size': 0})

    # Walking through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Extract the file extension
            _, ext = os.path.splitext(file)
            if ext:  # Ignore files without extension
                # Update the count
                stats[ext]['count'] += 1
                # Get the file size
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                # Update the max size if this file is larger
                stats[ext]['max_size'] = max(stats[ext]['max_size'], file_size)
                # Update the total size
                stats[ext]['total_size'] += file_size

    return stats


# Function to format the stats into a string
def format_stats(stats):
    output_lines = []
    for ext, data in sorted(stats.items()):
        output_lines.append(f"{ext}	{data['count']}	{data['max_size']}	{data['total_size']}")
    return "\n".join(output_lines)


# The script should be called with a command-line argument specifying the directory
if __name__ == "__main__":
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Scan directory for file statistics.")
    parser.add_argument('directory', nargs='?', default='.', help="Directory to scan for file statistics.")
    args = parser.parse_args()

    # check directory whether inputted, if not, use current working directory
    directory = args.directory if len(args.directory) > 1 else os.getcwd()
    stats = file_stats(directory)

    formatted_stats = format_stats(stats)
    print(formatted_stats)
