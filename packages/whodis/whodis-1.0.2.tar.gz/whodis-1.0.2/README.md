# WhoDis
Parses the contents of a source code directory and determines the programming languages in use.

# Languages Supported:
* Go
* Java
* JavaScript
* Python
* Ruby

# Usage
Install from PyPI:
```python
pip install whodis
```

Import the module and create a new instance of WhoDis:
```python
from whodis import WhoDis
blah = WhoDis()
```

WhoDis objects have a single method, parse(), which takes a single filepath (string) parameter:
```
blah.parse("/some/valid/path/with/source/code")
```

After parsing a valid path with at least one file in a supported language, the object will have four attributes:
```python
# language - The dominant programming language in the source path.
# String.
# Possible string values are "go", "java", "js", "py", "rb".
blah.language
>>> "py"

 # all_languages - All languages present in the source path.
 # List of strings.
 # Possible list values are "go", "java", "js", "py", "rb".
blah.all_languages
>>> ["rb", "js"]

# files - All non-filtered files in the source path.
# List of strings.
blah.files
>>> ["__init__.py", "main.py", "README.md", "LICENSE.md", "requirements.txt"]

# files_by_language - All non-filtered files in the source path broken down by language.
# Dictionary with strings for keys and lists of strings for values.
# Possible key names are "go", "java", "js", "py", "rb".
blah.files_by_language
>>> {"rb": ["application_controller.rb", "model.rb"], "js": ["app.js"]}
```

# FAQs
### 1. How does WhoDis work?
WhoDis is very naive. It will recursively find all files in a path, filter out certain directories (e.g. .git, build/packaging, virtual environments, etc.), look at the file extensions of the files returned, and group them by extension (e.g. .py). WhoDis then looks at which language has the most files and considers it the dominant language for the source code in the path.

### 2. What gets filtered out? Why filter?
Please look at the *_filters.py files, which should be quite easy to understand. The files getting filtered are in directories that are commonly associated with things like version control, building/packaging, and virtual environments. The reason for filtering is 1) to speed up WhoDis (e.g. a big .git can slow us down a lot), and 2) these directories usually contain files that are irrelevant/redundant to determining the programming languages being used. In short, filtered files shouldn't influence WhoDis' parsing.

### 3. Why only support Go, Java, JavaScript, Python, and Ruby?
I wrote WhoDis for use with another project that interacts with AWS Lambda. These languages are all natively supported by Lambda. Feel free to open a PR if you'd like additional language support!
