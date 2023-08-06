# WhoDis
Parses the contents of a source code directory and determines the programming languages in use.

# Languages Supported:
* Go
* Java
* JavaScript
* Python
* Ruby

# Usage
```python
from whodis import WhoDis
blah = WhoDis()
blah.parse("/some/valid/path/with/source/code")
blah.language # The dominant programming language in the source path.
blah.all_languages # All languages present in the source path.
blah.files # All non-filtered files in the source path.
blah.files_by_language # All non-filtered files in the source path broken down by language.
```
