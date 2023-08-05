##############################################
#	Author : Chris O'Brien   
#	Created On : Mon Aug 13 2018
#	File : rm_logger.py
#	Description: Generic Logging Class
##############################################

import inspect
import logging.handlers
import os

class Logger(object):
    
    def __init__(self, 
                 log_file_location, 
                 logger_name="", 
                 max_log_file_size=1, 
                 log_file_backup_count=3, 
                 logging_level="INFO", 
                 log_format="%(levelname)s: [%(name)s]: %(asctime)s - %(message)s", 
                 date_format="%m/%d/%Y %H:%M:%S"):
        if logger_name != "":
            self.logger_name = logger_name
        else:
            self.logger_name = self.__get_calling_file_name()
        self.log_file_location = log_file_location
        self.max_log_file_size = max_log_file_size
        self.log_file_backup_count = log_file_backup_count
        self.logging_level = logging_level
        self.log_format = log_format
        self.date_format = date_format

        self.__create_log_file()
        self.__setup_logger()

    def __create_log_file(self):
        # Get the directory portion
        directory = os.path.dirname(self.log_file_location)
        # Check if it exists and create it if not
        if not os.path.exists(directory):
            os.makedirs(directory)
        # Create the file
        if not os.path.isfile(self.log_file_location):
            with open(self.log_file_location, 'a') as logfile:
                logfile.close()

    def __calculate_max_log_file_size(self):
        return self.max_log_file_size * 1048576

    def __get_calling_file_name(self):
        frame=inspect.currentframe()
        frame=frame.f_back.f_back
        code=frame.f_code
        return code.co_filename

    def __setup_logger(self):
        # Set up a specific logger with our desired output level
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(self.logging_level)
        
        # Add the log message handler to the logger
        handler = logging.handlers.RotatingFileHandler(self.log_file_location, maxBytes=self.__calculate_max_log_file_size(), backupCount=self.log_file_backup_count)

        formatter = logging.Formatter(self.log_format, datefmt=self.date_format)

        handler.setFormatter(formatter)

        self.logger.addHandler(handler)

        return self.logger

    # Overloaded logger methods
    def debug(self, log_msg):
        self.logger.debug(log_msg)

    def info(self, log_msg):
        self.logger.info(log_msg)

    def warning(self, log_msg):
        self.logger.warning(log_msg)

    def error(self, log_msg):
        self.logger.error(log_msg)
    
    def critical(self, log_msg):
        self.logger.critical(log_msg)

# class LoggerTest(object):
#     from logger import Logger

#     def main():
#         log = Logger("./logs/test.log")

#         log.info("Hey, this is a test!")

#         log.critical("Uh oh, danger!!!")

#     if __name__ == "__main__":
#         main()
