import sqlite3

# データベースの作成（または接続）
conn = sqlite3.connect('calendar_app.db')
c = conn.cursor()

# 予定テーブルの作成
c.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        description TEXT
    )
''')

conn.commit()
conn.close()

print("Database and table created successfully.")
