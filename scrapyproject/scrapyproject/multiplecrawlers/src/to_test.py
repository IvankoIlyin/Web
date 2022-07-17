import scrapy
from config import *
import logging

logging.getLogger("scrapy").propagate = False
logging.basicConfig(
    level="INFO",
    format="[%(levelname)-5s] %(asctime)s\t-\t%(message)s",
    datefmt="%d/%m/%Y %I:%M:%S %p",
)

proxy = "https://{}:{}@{}".format(proxy_user, proxy_password, proxy_base_url)

def handle_error(failure):
    pass

