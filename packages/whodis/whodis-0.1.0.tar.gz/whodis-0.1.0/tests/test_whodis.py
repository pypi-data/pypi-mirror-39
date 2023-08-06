from unittest.mock import patch
import pytest
from whodis import WhoDis


@patch('os.walk')
def test_parse_with_valid_path(mockwalk):
    """
    Parse a valid path with files in only one language in it.
    """
    mockwalk.return_value = [
        ('/foo', ['bar', 'build'], ['README.md', 'requirements.txt']),
        ('/foo/bar', [], ['__init__.py', 'main.py', ]),
    ]
    blah = WhoDis()
    blah.parse("/fake_path_yo")

    # Tests for self.files.
    assert type(blah.files) is list
    assert len(blah.files) > 0

    # Tests for self.files_by_language.
    assert type(blah.files_by_language) is dict
    assert len(blah.files_by_language.keys()) == 1
    assert "py" in blah.files_by_language.keys()
    assert len(blah.files_by_language['py']) == 2

    # Tests for self.language.
    assert type(blah.language) is str
    assert blah.language != ""
    assert blah.language == 'py'

    # Tests for self.all_languages.
    assert type(blah.all_languages) is list
    assert blah.all_languages != []
    assert "py" in blah.all_languages


@patch('os.walk')
def test_parse_with_valid_path_multi_lang(mockwalk):
    """
    Parse a valid path with files in multiple languages in it.
    """
    mockwalk.return_value = [
        ('/app', ['controllers', 'models', 'assets'], [
            'README.md', 'Gemfile', 'Gemfile.lock']),
        ('/app/controllers', [], [
            'application_controller.rb', 'sessions_controller.rb']),
        ('/app/models', [], ['blah.rb', ]),
        ('/app/assets', ['javascripts', ], []),
        ('/app/assets', [], ['application.js', ])
    ]
    blah = WhoDis()
    blah.parse("/fake_path_yo")

    # Tests for self.files.
    assert type(blah.files) is list
    assert len(blah.files) > 0

    # Tests for self.files_by_language.
    assert type(blah.files_by_language) is dict
    assert len(blah.files_by_language.keys()) == 2
    assert "rb" in blah.files_by_language.keys()
    assert "js" in blah.files_by_language.keys()
    assert len(blah.files_by_language['rb']) == 3

    # Tests for self.language.
    assert type(blah.language) is str
    assert blah.language != ""
    assert blah.language == "rb"

    # Tests for self.all_languages.
    assert type(blah.all_languages) is list
    assert blah.all_languages != []
    assert "rb" in blah.all_languages
    assert "js" in blah.all_languages


def test_parse_with_invalid_path_raises_exception():
    """ An invalid path should raise an IOError """
    path = "/lol_i-DONT_exist"
    blah = WhoDis()
    with pytest.raises(IOError):
        blah.parse(path)


@patch('os.walk')
def test_parse_with_no_source_code_raises_exception(mockwalk):
    """ A path without recognizable source code should raise an IOError """
    mockwalk.return_value = [
        ('/foo', ('bar',), ('baz',)),
        ('/foo/bar', (), ('qux', 'quux',)),
    ]
    path = "/fake_path_yo"
    blah = WhoDis()
    with pytest.raises(IOError):
        blah.parse(path)
