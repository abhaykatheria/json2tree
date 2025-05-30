import json
import os

# Attempt to import from __main__ first for the generate_from_file functionality
# and create_output_file. If __main__ is not available (e.g. during package import by setup.py),
# these will be handled by direct calls later if possible.
try:
    from .__main__ import generate as generate_from_file_path
    from .__main__ import create_output_file
except ImportError:
    # This might happen if setup.py imports __init__.py before __main__.py is in sys.path in a structured way
    # Or if used in a context where __main__ is not directly runnable as a module entry.
    # We will define fallbacks or ensure direct calls for core logic.
    generate_from_file_path = None # Placeholder, direct file handling will be in convert
    create_output_file = None      # Placeholder, direct file writing will be in convert


from .theme_1 import html as html_1
from .theme_2 import html as html_2

__version__ = "0.2.0" # Updated version
__author__ = 'Abhay Katheria, Mithilesh Tiwari, and AI Contributor'
__all__ = ['convert']


def convert(json_input, theme='1', output_file=None):
    """
    Converts JSON input to an HTML tree representation.

    :param json_input: JSON data to convert. Can be:
                       - A file path (string) to a JSON file.
                       - A JSON formatted string.
                       - A Python dictionary.
    :param theme: Theme identifier string ('1' or '2'). Defaults to '1'.
    :param output_file: Optional. File path to save the HTML output.
                        If None, the HTML string is returned.
    :return: HTML string if output_file is None, otherwise None.
    :raises TypeError: If json_input is not a str, dict.
    :raises ValueError: If json_input string is not a valid JSON or file path.
    """
    html_string = ''
    json_data = None

    if isinstance(json_input, str):
        if os.path.exists(json_input): # Check if it's a file path
            # Use the generate function from __main__ if available and it handles file paths
            # For direct file handling:
            try:
                with open(json_input, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
            except FileNotFoundError:
                raise ValueError(f"Input file not found: {json_input}")
            except json.JSONDecodeError:
                raise ValueError(f"Invalid JSON in file: {json_input}")
        else: # Assume it's a JSON string
            try:
                json_data = json.loads(json_input)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON string provided: {e}")
    elif isinstance(json_input, dict):
        json_data = json_input
    else:
        raise TypeError("json_input must be a file path (str), a JSON string (str), or a dictionary.")

    if json_data is None: # Should have been caught by now, but as a safeguard
        raise ValueError("Failed to parse or load JSON input.")

    if theme == '1':
        html_string = html_1.create_html_report(json_data)
    elif theme == '2':
        html_string = html_2.create_html_report(json_data)
    else: # Default to theme 1 if an invalid theme is chosen
        html_string = html_1.create_html_report(json_data)

    if output_file:
        # Use create_output_file from __main__ if available and it handles writing
        # For direct file writing:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_string)
            return None # Function signature implies None when writing to file
        except IOError:
            # Consider how to handle IOErrors, e.g., re-raise or log
            raise IOError(f"Could not write to output file: {output_file}")
    else:
        return html_string
