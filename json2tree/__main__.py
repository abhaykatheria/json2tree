import argparse
import logging
import os
import sys
from json2tree.theme_1 import html as html_1 # Kept for generate, if generate is kept
from json2tree.theme_2 import html as html_2 # Kept for generate, if generate is kept
import json # Kept for generate, if generate is kept
from . import convert # Import the new convert function

# The original generate and create_output_file functions can be kept if there's a desire
# for them to be callable directly for some reason, or removed if convert fully supersedes.
# For this refactoring, run() will use convert(), making generate() and create_output_file()
# not directly used by the CLI flow anymore.

def generate(file_path, theme):
    # this functions takes input json file and theme
    # then returns the html string to be written in files
    # f = open(file_path)
    # json_data = json.load(f)
    with open(file_path, 'r', encoding='utf-8') as f:
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
    with open(output_file_path, 'w', encoding='utf-8') as f: # Added encoding='utf-8' for consistency
        f.write(html_string)
        # f.close() # Not strictly necessary with 'with open()'

def run(args):
    if not args.json:
        sys.stderr.write("Input JSON file not specified. Use -j or --json.\n")
        return
    if not args.output_file:
        sys.stderr.write("Output file not specified. Use -o or --output-file.\n")
        return

    # Use the new convert function
    # It handles file existence checks and JSON parsing internally for file paths
    try:
        # If args.theme is None (not provided), convert will use its default '1'
        # convert handles writing to output_file directly.
        convert(json_input=args.json, theme=args.theme if args.theme else '1', output_file=args.output_file)
        # print(f"HTML tree generated successfully at {args.output_file}") # Optional success message
    except FileNotFoundError as e:
        sys.stderr.write(f"Error: Input file not found - {args.json}\n")
    except ValueError as e: # Catches JSON parsing errors or other value errors from convert
        sys.stderr.write(f"Error: {e}\n")
    except TypeError as e: # Catches type errors from convert if input is not str/dict
        sys.stderr.write(f"Error: {e}\n")
    except IOError as e:
        sys.stderr.write(f"Error writing to output file: {e}\n")
    # except Exception as e: # Generic catch for other unexpected errors
    #     sys.stderr.write(f"An unexpected error occurred: {e}\n")

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
                            ver_str="0.2.0", py_v=py_ver)) # Updated version string here

    args, unknown = parser.parse_known_args()

    if sys.version_info < (3, 0):
        sys.stderr.write("Errrrrrrr.....Please run on Python 3.7+")
    else:
        run(args)