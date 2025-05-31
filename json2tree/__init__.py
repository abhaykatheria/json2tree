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
        # Heuristic: if it starts with { or [, it's likely a JSON string. Otherwise, could be a path.
        # This isn't foolproof but covers many common cases.
        is_likely_json_payload = json_input.strip().startswith(("{", "["))

        if os.path.exists(json_input):
            try:
                with open(json_input, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
            except json.JSONDecodeError: # File exists but is not valid JSON
                raise ValueError(f"Invalid JSON in file: {json_input}")
            # FileNotFoundError here would be a race condition if os.path.exists was true moments before.
            # Python's default FileNotFoundError would propagate.
        elif is_likely_json_payload: # Not a file path, but looks like a JSON string
            try:
                json_data = json.loads(json_input)
            except json.JSONDecodeError as e: # Does look like JSON but is malformed
                raise ValueError(f"Malformed JSON string provided: {e}")
        else: # Not an existing file path, and not starting like a JSON payload.
              # Treat as a non-existent file path or invalid input.
            raise ValueError(f"Input string '{json_input}' is not an existing file path and not a recognizable JSON string.")
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
        # Debug prints
        print(f"DEBUG: Attempting to write to output_file: {output_file}")
        print(f"DEBUG: Length of html_string: {len(html_string)}")
        if len(html_string) < 200: # Print a snippet if short
            print(f"DEBUG: HTML_STRING (snippet): {html_string[:100]}...{html_string[-50:]}")
        else:
            print(f"DEBUG: HTML_STRING (snippet): {html_string[:100]}...{html_string[-100:]}")

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_string)
            print(f"DEBUG: Successfully wrote to {output_file}") # Confirm write
            return None # Function signature implies None when writing to file
        except IOError as e:
            print(f"DEBUG: IOError during write: {e}") # Debug IOError
            # Consider how to handle IOErrors, e.g., re-raise or log
            raise IOError(f"Could not write to output file: {output_file}")
    else:
        return html_string
