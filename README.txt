# JSON 2 Tree [![Downloads](https://pepy.tech/badge/json2tree)](https://pepy.tech/project/json2tree)
A python library to create HTML tree view from JSON files.
This can also be used as a command line tool for the same purpose.


<img src="J2T.jpg" height=400px />

[](mdtoc)
# Table of Contents

* [Getting Started](#getting-started)
	* [Installation](#installation)
	* [Usage (CLI)](#usage-cli)
		* [Sample command](#sample-command)
* [Using as a Library](#using-as-a-library)
* [Themes](#themes)
* [Development Notes](#development-notes)
* [Contributors](#contributors)
[](/mdtoc)

# Getting Started
## Installation
- Install usig pip `pip install json2tree`
	### or
- Clone this repo by running following command
    ``` git clone https://github.com/abhaykatheria/json2tree ```
- CD into the cloned repo
- Install using following command ``` pip install . ```

## Usage (CLI)
You can invoke the cli with typing json2tree command.
There are 2 necessary arguments -
- -j : this flag will take the input json file.
- -o : this flag will set up the output file.

There is a third theme flag
- -t : this can be used to set the theme of html output.

### Sample command
``` json2tree -j example.json -o output.html -t 1 ```

# Using as a Library

You can use `json2tree` as a Python library to convert JSON data into HTML. The primary function for this is `convert` from the `json2tree` package.

```python
from json2tree import convert
import json

# Example 1: Convert JSON file to HTML file, specifying theme 2
# Ensure 'input.json' exists or provide a valid path.
# convert('input.json', theme='2', output_file='output_theme2.html')

# Example 2: Convert a JSON string to an HTML string (theme 1 default)
json_string = '{"name": "Test User", "details": {"age": 30, "isStudent": false, "courses": ["Math", "Science"]}}'
html_output_string = convert(json_string)
# print(html_output_string) # Or save it to a file:
# with open('output_from_string.html', 'w', encoding='utf-8') as f:
#     f.write(html_output_string)

# Example 3: Convert a Python dictionary to HTML and save to a file
my_dict = {
    "project": "json2tree",
    "version": "0.2.0",
    "data": {
        "items": [
            {"id": 1, "value": "apple"},
            {"id": 2, "value": "banana"}
        ],
        "status": "ok",
        "nested_data": {
            "key1": "value1",
            "key2": [10, 20, 30]
        }
    }
}
convert(my_dict, theme='1', output_file='output_from_dict.html')

# Example 4: Convert a Python dictionary to an HTML string with theme 2
another_dict = {"message": "Hello, World!", "code": 200}
html_string_theme2 = convert(another_dict, theme='2')
# print(html_string_theme2)
```

**`convert` function parameters:**

*   `json_input`: The JSON data to convert. Can be:
    *   A file path (string) to a JSON file.
    *   A JSON formatted string.
    *   A Python dictionary.
*   `theme`: Theme identifier string ('1' or '2'). Defaults to '1'.
*   `output_file`: Optional. File path to save the HTML output. If `None` (default), the HTML string is returned.

# Themes
Currently there are only 2 themes.
- ### Theme 1
![image](https://user-images.githubusercontent.com/40055274/134461395-f738857d-a543-4a1b-8ab6-71d02e7c5e92.png)
- ### Theme 2
![image](https://user-images.githubusercontent.com/40055274/134461586-f5b071af-64d5-46e9-ba4d-946936ce34f7.png)

# Development Notes
Recent versions (v0.2.0) include significant refactoring for:
- Improved maintainability by centralizing HTML generation logic.
- Enhanced theme structure.
- Performance optimizations in HTML string building processes.
- Introduction of the `convert()` function for more flexible library usage.

# Contributors
@abhaykatheria
@m1-key
AI Contributor via Google-ChatTool
