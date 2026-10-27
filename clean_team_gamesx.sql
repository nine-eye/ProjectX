 p.season,
            t.*,
            p.points

        FROM team_stats t
        JOIN points p
            USING (game_id, team)

        WHERE p.points IS NOT NULL
            AND t.third_down_rate IS NOT NULL