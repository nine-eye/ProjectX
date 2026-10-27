If I know how a team’s offence played in a game, can I work out how many points it scored?

Here's a pipeline that uses SQL and linear regression to explain how much of an NFL team's scoring comes from its offensive box-score stats.

Using 5 seasons of past NFL data, I cleaned the data using SQL/DuckDB and trained a model on 4 seasons, testing on a 5th unseen season.

Results:

The model explains about 59% of the story.

The model's usually around 5 points off, compared to an average guess of around 8 points off.

Yards are the biggest driver; passing yards matter slightly more than rushing yards.

Efficiency matters - if 2 teams gain the same yards, the one that needed more plays tends to score less. Checks out.

Turnovers, as you may imagine, hurt. A lot.

Limits:

The model, unfortunately, cannot predict a game before it happens. This is literally a starter project, so slow your roll, bucko.

The results infer patterns, not a causal relationship.

The model was tested on a single season only; testing on further seasons would show if a MAE of 4.91 is luck or not.

The model uses linear regression, which is likely too simple for a sport as unpredictable and complex as football.
