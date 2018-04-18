"""
import logging
from logging.config import fileConfig
import os


LOG_CFG_FILE = os.path.join(os.getcwd(), "config", "logger.cfg")
fileConfig(LOG_CFG_FILE)

handler = logging.FileHandler('out.log', 'W', 'utf-8-sig')
logging.getLogger(__name__).addHandler(handler)
"""