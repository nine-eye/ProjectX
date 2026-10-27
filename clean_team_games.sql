-- Offensive stats per team game (regular season)
WITH team_stats AS (
    SELECT
        game_id,
        posteam AS team,
        COUNT(*) AS plays,
        SUM(CASE WHEN play_type = 'pass' THEN yards_gained ELSE 0 END) AS pass_yds,
        SUM(CASE WHEN play_type = 'run' THEN yards_gained ELSE 0 END) AS rush_yds,

        SUM(COALESCE(interception,0)+ COALESCE(fumble_lost, 0)) AS turnovers,
        SUM(COALESCE(sack,0)) AS sacks,

        SUM (third_down_converted) * 1.0
            / NULLIF(SUM(third_down_converted)+ SUM(third_down_failed), 0) AS third_down_rate

    FROM 'data/raw/pbp.parquet'

    WHERE 1 = 1
        AND season_type = 'REG'
        AND posteam IS NOT NULL
        AND play_type IN ('pass','run')

    GROUP BY game_id, posteam
    ),

    points AS (
        SELECT game_id, season, home_team AS team, home_score AS points
        FROM 'data/raw/schedules.parquet'
        WHERE game_type = 'REG'

        UNION ALL

        SELECT game_id, season, away_team AS team, away_score AS points
        FROM 'data/raw/schedules.parquet'
        WHERE game_type = 'REG'
        )

        SELECT
         p.season,
            t.*,
            p.points

        FROM team_stats t
        JOIN points p
            USING (game_id, team)

        WHERE p.points IS NOT NULL
            AND t.third_down_rate IS NOT NULL
