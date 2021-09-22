import argparse
import logging
import os
import sys
from . import html_1,css,js

import json

def readJSON(file_path, **kwargs):
    f = open(file_path)
    json_data = json.load(f)
    report = html_1.create_html_report(json_data)
    print(report)

def run(args):
    if args.json:
        if os.path.exists(args.json):
            if args.output_file is not None:
                # print("creating output file %s"%args.output_file)
                pass
            else : 
                print("no output file argument given")
            readJSON(args.json)
        else:
            print("bad boi ...")
                  


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        prog='json2tree',
        description='''
    json2tree helps you to create an html tree view for your json file.
    For comprehensive an intiutive analysis.
    Learn more at https://github.com/abhaykatheria/json2tree''')
    parser.add_argument('-j', '--json',
                        help="Input JSON file"
                        "give the path to the JSON file")
    parser.add_argument('-o', '--output-file',
                        help="give the path of the ouput file")
    py_ver = sys.version.replace('\n', '').split('[')[0]
    parser.add_argument('-v', '--version', action='version',
                        version="{ver_str}\n   python version = {py_v}".format(
                            ver_str="0.1.0", py_v=py_ver))

    args, unknown = parser.parse_known_args()

    if sys.version_info < (3, 0):
        sys.stderr.write("Errrrrrrr.....Please run on Python 3.7+")
    else:
        run(args)