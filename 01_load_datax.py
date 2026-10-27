import nflreadpy as nfl
from pathlib import Path
Path("data/raw").mkdir(parents=True, exist_ok=True)   # create the folder if missing

SEASONS = [2021, 2022, 2023, 2024, 2025]

pbp = nfl.load_pbp(seasons=SEASONS) # one row per play
sched = nfl.load_schedules(seasons=SEASONS) # one row per game, with final scores

pbp.write_parquet("data/raw/pbp.parquet")
sched.write_parquet("data/raw/schedules.parquet")

print(pbp.shape, sched.shape)

