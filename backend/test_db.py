import pyodbc

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=serveragenticai.database.windows.net;"
    "DATABASE=free-sql-db-2677174;"
    "UID=adminsql@serveragenticai;"
    "PWD=P@ssword1234;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
)

print("✅ Connected successfully!")
