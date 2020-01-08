#!/usr/bin/env python2
"""
Logpuzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700]
"GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows;
U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"

"""

import os
import re
import sys
import urllib
import argparse

author = "__Bryan__"


def read_urls(filename):
    # opening file and grabbing server_name
    with open(filename, 'r') as f:
        f_data = f.read()
        server_name = re.search(r'_(.+)', filename)
        server = server_name.group()
        # get pattern
        pattern = re.compile(r'GET\s(.+)\sHTTP')

        matches = pattern.finditer(f_data)

        url_dict = {}
        url_list = []

        for match in matches:
            phrase = match.group(1)
        # dictionary first to keep unique keys
            if "puzzle" in phrase:
                url_dict[phrase] = "YES"

        protocol = "http://"

        # turn dictionary into list in order to use .sort() later
        for path in url_dict:
            url_list.append(protocol + server[1:] + path)

        # Turn entire list to string to use REGEX
        check_string = " ".join(url_list)

        # Sorting the list function
        def myFunc(e):

            value = re.search(r'puzzle/p-\w+-(\w+)', e).group(1)

            return value

        # Check for which file was used. Animal or Place
        if re.search(r'puzzle/(\w+-\w+-\w+)', check_string):
            print("this file is PLACE_CODE.GOOGLE.COM")
            url_list.sort(key=myFunc)

        else:
            print("this file is ANIMAL_CODE.GOOGLE.COM")
            url_list.sort()

        return url_list


def download_images(urls_list, dest_dir):
    count = 0
    directory_path_list = []
    images_list = ""

    if dest_dir.startswith("/"):
        dest_dir = dest_dir[1:]

    dst_path = os.path.abspath(dest_dir)

    try:
        os.makedirs(dst_path)
    except OSError:
        print("Directory /{} may exist already\n".format(dest_dir))

    for img_url in urls_list:

        file_name = "img{}".format(count)
        print("Now retrieving {}...".format(file_name))

        directory_path = dst_path + "/" + file_name
        directory_path_list.append(directory_path)

        local_filename, _ = urllib.urlretrieve(img_url, directory_path)
        poo = re.search(r'assessment(.+)', local_filename)

        local_filename = poo.group()
        local_filename = local_filename[10:]
        print(local_filename)

        images_element = '<img src="' + local_filename + '"/>'
        images_list = images_list + images_element

        count += 1

    html_string = """
    <html>
        <body>
            <p>So it Begins...</p>
            <script>
                document.write('{}')
            </script>
        </body>
    </html>

    """.format(images_list)

    html_file = dst_path + "/index.html"

    with open(html_file, "w") as wf:
        wf.write(html_string)


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parse args, scan for urls, get images from urls"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)
    img_urls_list = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls_list, parsed_args.todir)

    else:
        print('\n'.join(img_urls_list))


if __name__ == '__main__':
    print("\n")
    main(sys.argv[1:])
    print("\n")
