from django.core.management.base import BaseCommand
from django.db import connection
import pandas as pd

class Command(BaseCommand):
  help = 'Prints all tables in the database'

  def handle(self, *args, **kwargs):
    with connection.cursor() as cursor:
      cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
      tables = cursor.fetchall()
      
      for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        print(f"Table: {table_name}")
        print(pd.DataFrame(rows[:]))
        print("\n")
