import duckdb

con = duckdb.connect()

# A. What's actually in the play-by-play file?
print("A. pbp rows by season and season_type")
con.sql("""
    SELECT season, season_type, COUNT(*) AS n
    FROM 'data/raw/pbp.parquet'
    GROUP BY season, season_type
    ORDER BY season, season_type
""").show()

print("A. most common play_type values")
con.sql("""
    SELECT play_type, COUNT(*) AS n
    FROM 'data/raw/pbp.parquet'
    GROUP BY play_type
    ORDER BY n DESC
    LIMIT 8
""").show()

# B. What's in the schedules file?
print("B. schedule rows by season and game_type")
con.sql("""
    SELECT season, game_type, COUNT(*) AS games, COUNT(home_score) AS with_score
    FROM 'data/raw/schedules.parquet'
    GROUP BY season, game_type
    ORDER BY season, game_type
""").show()

# C. Do the two files share any game_ids at all?
print("C. games found in both files")
con.sql("""
    SELECT COUNT(DISTINCT p.game_id) AS shared_games
    FROM 'data/raw/pbp.parquet' p
    JOIN 'data/raw/schedules.parquet' s USING (game_id)
""").show()