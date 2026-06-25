import pytest
import pyodbc

pytest.skip("Skipping DB connection test in CI", allow_module_level=True)

conn = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=serveragenticai.database.windows.net,1433;"
    "DATABASE=free-sql-db-2677174;"
    "UID=adminsql;"
    "PWD=P@ssword1234;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
)

print("✅ Connected successfully!")
