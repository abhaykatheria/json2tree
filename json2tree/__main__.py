import argparse
import logging
import os
import sys
from json2tree.theme_1 import html as html_1
from json2tree.theme_2 import html as html_2
import json

def generate(file_path, theme):
    # this functions takes input json file and theme
    # then returns the html string to be written in files
    f = open(file_path)
    json_data = json.load(f)
    html_string = ''
    if(theme=='1'):
        html_string = html_1.create_html_report(json_data)
    elif(theme=='2'):
        html_string = html_2.create_html_report(json_data)
    else:
        html_string = html_1.create_html_report(json_data)
    return html_string

def create_output_file(output_file_path, html_string):
    # takes input html string generated then outputs into
    # file path given by user
    with open(output_file_path, 'w') as f:
        f.write(html_string)
        f.close()

def run(args):
    if args.json:
        if os.path.exists(args.json):
            if args.output_file is None:
                sys.stderr.write("Output file not specified")
            html_string = generate(args.json, args.theme)
            create_output_file(args.output_file, html_string)        
        else:
            sys.stderr.write("Input file not specified")

def main():
    # main entery point
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
    parser.add_argument('-t', '--theme',
                        help="Select the theme to use. To know about theme visit"
                        "official repository")
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