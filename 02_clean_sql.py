import duckdb
from pathlib import Path
Path("data/raw").mkdir(parents=True, exist_ok=True)   # create the folder if missing

con = duckdb.connect()
query = open("data/sql/clean_team_games.sql").read()

df = con.sql(query).df()

print(df.shape)
print(df.isna().sum())
print(df.describe())

df.to_parquet("data/clean/team_games.parquet", index = False)

print(df)