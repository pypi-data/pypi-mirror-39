"""
whodis
"""
import os
from .common_filters import COMMON_FILTERS
from .go_filters import GO_FILTERS
from .java_filters import JAVA_FILTERS
from .javascript_filters import JAVASCRIPT_FILTERS
from .python_filters import PYTHON_FILTERS
from .ruby_filters import RUBY_FILTERS


FILTERED_DIRS = COMMON_FILTERS + GO_FILTERS + JAVA_FILTERS + \
                JAVASCRIPT_FILTERS + PYTHON_FILTERS + RUBY_FILTERS

FILE_EXTENSIONS = [
    "py",  # Python
    "js",  # JavaScript
    "go",  # Go
    "java",  # Java
    "rb",  # Ruby
]


class WhoDis():
    def __init__(self):
        self.files = []
        self.language = ""
        self.files_by_language = {}
        self.all_languages = []

    def parse(self, path):
        """
        Recursively parse a path looking for source code files. This function
        sets multiple attributes in the process:
            1) self.files - A list of all files present in the directory and
                any subdirectories. Filtered files are not in the list.
            2) self.files_by_language - For each language present, a list of
                all files for each language.
            3) self.language - The dominant language across all files.
            4) self.all_languages - A list of all languages across all files.

        Parameters
        ----------
        path : str
            The path to walk through. For example, "/home/user/source_code".

        Returns
        -------
        """
        self.files = self._recursively_get_files_in_path(path)
        self.files_by_language = self._breakdown_by_language()
        self.language = self._determine_dominant_language()
        self.all_languages = self._determine_all_languages()

    def _recursively_get_files_in_path(self, path: str):
        """
        Use os.walk to recurse through a path and return a list of files.
        Filters out files from any directory in FILTERED_DIRS. If no files
        are returned, an IOError exception is raised.

        Parameters
        ----------
        path : str
            The filepath to walk through.

        Returns
        -------
        list : str
            A list of filenames from the filtered path.
        """
        files = []
        for _dirpath, dirnames, filenames in os.walk(path):
            # First, remove any filtered directories.
            for dir_to_filter in FILTERED_DIRS:
                if dir_to_filter in dirnames:
                    dirnames.remove(dir_to_filter)

            files.extend(filenames)

        if files == []:
            raise IOError("No files in {}. Is it a valid directory?"
                          .format(path))

        return files

    def _breakdown_by_language(self):
        """
        Breaks self.files down by language.

        Parameters
        ----------

        Returns
        -------
        dict
            A dict that maps language to a list of files for that language.
            e.g.
            {
                "python": ['file1.py', 'file2.py', 'file3.py'],
                "javascript": ['blah.js', 'blorp.js'],
                "typscript": ['something.ts']
            }
        """
        breakdown = {}

        for file in self.files:
            if "." in file:
                extension = file.partition('.')[2]
                if extension in FILE_EXTENSIONS:
                    if extension in breakdown:
                        breakdown[extension].append(file)
                    else:
                        breakdown[extension] = [file]

        if breakdown == {}:
            raise IOError("Could not determine the language associated with "
                          "any of the source files. Either the files do "
                          "not contain any source code or our parser does "
                          "not support the language being used.")

        return breakdown

    def _determine_dominant_language(self):
        """
        Looks at self.files_by_language and determines the dominant language.

        Parameters
        ----------

        Returns
        -------
        str
            The dominant language among all source code files.
        """
        dominant_language = ""
        dominant_language_length = 0

        for language in self.files_by_language:
            num_files_in_language = len(self.files_by_language[language])
            if num_files_in_language > dominant_language_length:
                dominant_language = language
                dominant_language_length = num_files_in_language
            # TODO elif: num_files_in_language == dominant_language_length:

        return dominant_language

    def _determine_all_languages(self):
        """
        Looks at self.files_by_language and determines all languages.

        Parameters
        ----------

        Returns
        -------
        list
            A list of all languages present among all source code files.
        """
        languages = []

        for language in self.files_by_language:
            languages.append(language)

        return languages
