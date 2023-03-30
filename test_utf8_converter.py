import os

import pytest
from charset_normalizer.api import from_path

from utf8_converter import UTF8Converter

TEST_FILES_TO_BE_REMOVED = ('arabic-converted.txt', 'french-converted.txt', 'korean-converted.txt')


class TestUTF8Converter:
    def test_source_file_not_exists(self):
        with pytest.raises(TypeError) as exc_info:
            UTF8Converter('not_exist.txt', 'utf8.txt')
        assert str(exc_info.value) == "Source file's path is incorrect. Given file does not exist"

    def test_invalid_source_file_extension(self):
        with pytest.raises(TypeError) as exc_info:
            UTF8Converter('data/invalid_extension.html', 'utf8.txt')
        assert str(exc_info.value) == "Source file's extension is not allowed. Try with .txt"

    def test_invalid_target_file_extension(self):
        with pytest.raises(TypeError) as exc_info:
            UTF8Converter('data/sample-arabic.txt', 'invalid_extension.html')
        assert str(exc_info.value) == "Target file's extension is not allowed. Try with .txt"

    def test_successful_conversion_arabic(self):
        # GIVEN text file with Arabic content not encoded with utf-8 codec
        arabic_base_data = from_path('data/sample-arabic.txt').best()
        assert arabic_base_data.encoding == 'cp1256'
        assert arabic_base_data.language == 'Arabic'

        # WHEN it's converted via UTF8Converter class
        converter = UTF8Converter('data/sample-arabic.txt', 'arabic-converted.txt')
        converter.convert()

        # THEN this converted Arabic text file has utf-8 encoding
        arabic_converted_data = from_path('arabic-converted.txt').best()
        assert arabic_converted_data.encoding == 'utf_8'
        assert arabic_converted_data.language == 'Arabic'

    def test_successful_conversion_korean(self):
        # GIVEN text file with Korean content not encoded with utf-8 codec
        arabic_base_data = from_path('data/sample-korean.txt').best()
        assert arabic_base_data.encoding == 'cp949'
        assert arabic_base_data.language == 'Korean'

        # WHEN it's converted via UTF8Converter class
        converter = UTF8Converter('data/sample-korean.txt', 'korean-converted.txt')
        converter.convert()

        # THEN this converted Korean text file has utf-8 encoding
        arabic_converted_data = from_path('korean-converted.txt').best()
        assert arabic_converted_data.encoding == 'utf_8'
        assert arabic_converted_data.language == 'Korean'

    def test_successful_conversion_french(self):
        # GIVEN text file with French content not encoded with utf-8 codec
        arabic_base_data = from_path('data/sample-french.txt').best()
        assert arabic_base_data.encoding == 'cp1252'
        assert arabic_base_data.language == 'French'

        # WHEN it's converted via UTF8Converter class
        converter = UTF8Converter('data/sample-french.txt', 'french-converted.txt')
        converter.convert()

        # THEN this converted French text file has utf-8 encoding
        arabic_converted_data = from_path('french-converted.txt').best()
        assert arabic_converted_data.encoding == 'utf_8'
        assert arabic_converted_data.language == 'French'

    def teardown_class(self):
        for filename in TEST_FILES_TO_BE_REMOVED:
            os.unlink(filename)
