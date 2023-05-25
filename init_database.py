import sqlite3
from dhe import *

conn = sqlite3.connect('chat_database')
c = conn.cursor()


private_key_list = [generate_private_key(), generate_private_key(), generate_private_key(), 
                    generate_private_key(), generate_private_key(), generate_private_key()]

public_key_list = [generate_public_key(private_key_list[0]), generate_public_key(private_key_list[1]), 
                   generate_public_key(private_key_list[2]), generate_public_key(private_key_list[3]),
                   generate_public_key(private_key_list[4]), generate_public_key(private_key_list[5])]

try:
  c.execute('''
    CREATE TABLE `user_table` (
      `username` varchar(300) NOT NULL,
      `password` varchar(300) NOT NULL,
      `private_key` INT DEFAULT NULL,
      `public_key` INT DEFAULT NULL,
      PRIMARY KEY (`username`)
    )
            ''')
  c.execute(f'''
  INSERT INTO `user_table` VALUES 
  ('Alice','alice', {private_key_list[0]}, {public_key_list[0]}),
  ('Boby','boby', {private_key_list[1]}, {public_key_list[1]}),
  ('Ryan','ryan', {private_key_list[2]}, {public_key_list[2]}),
  ('Samy','Samy', {private_key_list[3]}, {public_key_list[3]}),
  ('Ted','ted', {private_key_list[4]}, {public_key_list[4]}),
  ('Admin','admin', {private_key_list[5]}, {public_key_list[5]})
          ''')
  print("Database Initialized!")
except Exception:
  print("user_table already exists!")

try:
  c.execute('''
    CREATE TABLE `session_table` (
      `user1` varchar(300) NOT NULL,
      `user2` varchar(300) NOT NULL,
      `session_key` INT NOT NULL,
      PRIMARY KEY (`session_key`)
    )
            ''')
except Exception:
  print("session_table already exists!")




conn.commit()
