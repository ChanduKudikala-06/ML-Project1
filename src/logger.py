import logging
import os

from datetime import datetime

#creating dynamic log file
#datetime-> gets current date & time
#strftime->formats it into string
LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" 

#os.getcwd->gets current working directory ex:-D:\Projects\ML Project1
logs_path=os.path.join(os.getcwd(),"logs")

os.makedirs(logs_path,exist_ok=True)


LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s -%(levelname)s -%(message)s",
    level=logging.INFO,
)

if __name__=="__main__":
    logging.info("Logging has Started")