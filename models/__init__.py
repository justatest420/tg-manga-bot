from config import env_vars
from logger import logger

if env_vars['DB_URL']:
  from .mdb import *
  logger.info("Using MongoDB")
  
elif env_vars['DATABASE_URL_PRIMARY']:
  from .db import DB, ChapterFile, Subscription, LastChapter, MangaName
  logger.info("Using Tembo DB")

else:
  logger.error("Add Database Link at config.py")
