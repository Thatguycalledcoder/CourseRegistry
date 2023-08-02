
import logging.config
import json


class FileReader:
    logging.config.fileConfig("resources/configs/logging.conf")
    logger = logging.getLogger("Ingest")

    def __init__(self, filetype: str):
        self.logger.debug("FileReader constructor initialized")
        self.filetype = filetype

    def read_file(self):
        self.logger.debug(f"Reading {self.filetype} file")
        with open('course.json') as f:
            new_course = json.load(f)
        return new_course
