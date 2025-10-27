import sqlite3, os, pandas as pd
db_path = os.path.join('data', 'data.db')
output_dir = "data"
with sqlite3.connect(db_path) as db:
    cur = db.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cur.fetchall()]
    for table in tables:
        df = pd.read_sql_query(f"SELECT * FROM {table};", db)
        df.to_csv(os.path.join(output_dir, f"{table}.csv"), index=False, encoding="utf-8-sig")
        print(f"Exported {table} ({len(df)} rows)")
