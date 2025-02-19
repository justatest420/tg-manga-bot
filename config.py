env_vars = {
  # Get From my.telegram.org
  "API_HASH": "c0da9c346d2c45dbc7ec49a05da9b2b6",
  
  # Get From my.telegram.org
  "API_ID": int("13675555"),
  
  #Get For @BotFather
  "BOT_TOKEN": "5123263018:AAFhrk204_c3NTupbt5aJ87tOOUVfCcrzA4",
  
  # Get For tembo.io
  "DATABASE_URL_PRIMARY": "",
  
  # Mongodb Url
  "DB_URL": "mongodb+srv://justatestsubject01:HzP5SK8ZiiLHcF3o@cluster0.wizfkbo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
  
  # Logs Channel Username Without @
  "CACHE_CHANNEL": "",
  
  # Force Subs Channel username without @
  "CHANNEL": "",
  
  # {chap_num}: Chapter Number
  # {chap_name} : Manga Name
  # Ex : Chapter {chap_num} {chap_name} @Manhwa_Arena
  "FNAME": "",
  
  # Upload at repo and put path
  "THUMB": ""
}

dbname = env_vars.get('DATABASE_URL_PRIMARY') or env_vars.get('DATABASE_URL') or 'sqlite:///test.db'

if dbname.startswith('postgres://'):
    dbname = dbname.replace('postgres://', 'postgresql://', 1)
    
