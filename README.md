
# JSON 2 Tree [![Downloads](https://pepy.tech/badge/json2tree)](https://pepy.tech/project/json2tree)
A python library to create HTML tree view from JSON files.
This can also be used as a command line tool for the same purpose.


<img src="J2T.jpg" height=400px />

[](mdtoc)
# Table of Contents

* [Getting Started](#getting-started)
	* [Installation](#installation)
	* [Usage](#usage)
		* [Sample command](#sample-command)
* [Themes](#themes)
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

## Usage
You can invoke the cli with typing json2tree command.
There are 2 necessary arguments - 
- -j : this flag will take the input json file.
- -o : this flag will set up the output file.

There is a third theme flag 
- -t : this can be used to set the theme of html output.

### Sample command
``` json2tree -j example.json -o output.html -t 1 ```

# Themes
Currently there are only 2 themes.
- ### Theme 1
![image](https://user-images.githubusercontent.com/40055274/134461395-f738857d-a543-4a1b-8ab6-71d02e7c5e92.png)
- ### Theme 2
![image](https://user-images.githubusercontent.com/40055274/134461586-f5b071af-64d5-46e9-ba4d-946936ce34f7.png)

# Contributors
@abhaykatheria
@m1-key
