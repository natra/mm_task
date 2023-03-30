import os
from typing import Union

from charset_normalizer import detect

from exceptions import ConversionException

ALLOWED_FILE_EXTENSIONS = (".txt",)
CONFIDENCE_THRESHOLD = 0.75


class UTF8Converter:
    """
    Class that converts text files encoded in non-UTF to UTF-8 encoded files
    """

    def __init__(self, source_file_path: str, target_file_path: str):
        if not os.path.isfile(source_file_path):
            raise TypeError(
                "Source file's path is incorrect. Given file does not exist"
            )

        if (
            os.path.splitext(source_file_path)[-1].lower()
            not in ALLOWED_FILE_EXTENSIONS
        ):
            raise TypeError("Source file's extension is not allowed. Try with .txt")

        if (
            os.path.splitext(target_file_path)[-1].lower()
            not in ALLOWED_FILE_EXTENSIONS
        ):
            raise TypeError("Target file's extension is not allowed. Try with .txt")

        self.source_file_path = source_file_path
        self.target_file_path = target_file_path

    def detect_encoding_type(self, file_bytes: bytes) -> Union[None, str]:
        detected_encoding_type_data = detect(file_bytes)

        if detected_encoding_type_data["confidence"] < CONFIDENCE_THRESHOLD:
            # as there is no 100% guarantee that charset_normalizer guess the correct codec,
            # we need to use some threshold
            return None

        return detected_encoding_type_data["encoding"]

    def convert(self) -> None:
        with open(self.source_file_path, "rb") as f:
            source_file_bytes = f.read()

        source_file_detected_encoding_type = self.detect_encoding_type(
            source_file_bytes
        )
        if source_file_detected_encoding_type is None:
            raise ConversionException(
                f"Unable to detect an encoding type for {self.source_file_path}"
            )

        try:
            source_file_text = source_file_bytes.decode(
                source_file_detected_encoding_type
            )
        except UnicodeDecodeError:
            raise ConversionException(
                f"Unable to decode file: {self.source_file_path} using codec {source_file_detected_encoding_type}"
            )

        with open(self.target_file_path, "w", encoding="utf-8") as f:
            f.write(source_file_text)
