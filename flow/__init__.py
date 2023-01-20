from configparser import ConfigParser
import logging
import os
from datetime import datetime

cfg = ConfigParser()
cfg.read("config.ini")

os.makedirs("log", exist_ok=True)

today_date = datetime.now()

log_date = today_date.strftime("%d_%m_%Y")

os.environ['WDM_LOG'] = str(logging.NOTSET)
log_format = '%(asctime)s - %(levelname)s: %(message)s'
logging.basicConfig(format=log_format, level=logging.INFO, filename=rf".\log\Log_{log_date}.log", datefmt='%H:%M:%S')