##############################################
#	Author : Chris O'Brien   
#	Created On : Mon Aug 13 2018
#	File : logger_test.py
#	Description: Test of the logger class
##############################################

from logger import Logger

def main():
    log = Logger("./logs/test.log")

    log.info("This is a test...")
    log.warning("I know what you did last summer...")

if __name__ == "__main__":
    main()
    