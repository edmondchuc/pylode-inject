# pyLODE Inject

*Inject logo images, links, paragraphs, and figures to a pyLODE document.*

Easily do the above by defining the instructions in a YAML file and passing it to the command line application.

# Usage
Clone this repository and change directory into it.

Install dependencies in the `requirements.txt` document in a virtual environment.
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
Example usage:
```
python3 pylode_inject inject.yml index.html
```
where `inject.html` is the YAML configuration file to tell `pylode_inject` what to do and `index.html` is the pyLODE HTML document to be injected with additional HTML. 

## Files

* [pylode_inject.yml](pylode_inject.yml) - A working configuration file for the Plot Ontology
* [index.html](index.html) - The Plot Ontology's HTML output by pyLODE
* [output.html](index.html) - Output of pyLODE Inject.

# Improvements

* Make this project into a pip-installable package and can be executed with `pylode_inject` as a global command.