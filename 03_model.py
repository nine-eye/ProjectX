# Goal: Predict how many points a team scores in a game from its
# offensive stats, then check how good those predictions are.

# Imports
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# Loading the clean data
df = pd.read_parquet("data/clean/team_games.parquet")

# Choosing the inputs (X) and the target (Y)
features = ["plays", "pass_yds", "rush_yds", "turnovers", "sacks", "third_down_rate"]

target = "points"

# Split into training and test sets
# Train on 2021-2024 data, test on 2025 data.
# df["season"] < 2025 gives T/F for every row;
# df[...] then keeps only the rows where it's True.
train = df[df["season"]<2025]
test = df[df["season"]==2025]

# x = the inputs (a table), y = the target (one column).
X_train, y_train = train[features], train[target]
X_test, y_test = test[features], test[target]

# make_pipeline chains two steps so they always run together, in order:
# StandardScaler rescales each feature to mean 0 and standard
# deviation 1, so yards (in the hundreds) and third-down rate (0-1)
# are comparable scales.

# LinearRegression finds the weight for each feature that best
# predicts points.
model = make_pipeline(StandardScaler(), LinearRegression())

# .fit() is where the learning happens, using only the training data.
# The scaler learns each feature's mean and SD; the regression learns the weights.
model.fit(X_train, y_train)

# Predict on data the model has never seen
# .predict() applies what was learned to the 2025 games. The scaler
# reuses the training means and SDs; nothing is learned from test data.
predictions = model.predict(X_test)

# Build a baseline to compare against
# The simplest reasonable guess: the training average, for every game
# A model is only worth anything if it beats this
baseline = [y_train.mean()] * len(y_test)

# Score the predictions
# MAE (mean absolute error - how far off we are)
# R² = share of the variation in points the model explains
print(f"Baseline MAE: {mean_absolute_error(y_test, baseline): .2f} points")
print(f"Model MAE: {mean_absolute_error(y_test, predictions): .2f} points")
print(f"Model R²: {r2_score(y_test, predictions): .3f}")

# Look inside the model
# Model [-1] is the last step of the pipeline (the LinearRegression).
# .coef_ holds one learned weight per feature, in the same order as
# features. Because the features were scaled, each weight means:
# "points gained or lost when this stat rises by one standard deviation".
coefs = pd.Series(model[-1].coef_, index = features).sort_values()
print("\nPoints per 1-SD change in each feature:\n", coefs)

from pathlib import Path
Path("results").mkdir(exist_ok=True) # create a results folder if missing

# One row per 2025 team-game: its stats,points, prediction and error.
results = test[["season", "game_id","team"]+ features + [target]].copy()
results["predicted"] = predictions
results["error"] = results["points"] - results["predicted"] # + means the model guessed too low
results.to_csv("results/predictions_2025.csv", index=False)

# One row per feature: its name and learned weight
coef_df = pd.DataFrame({"feature": features, "coef": model[-1].coef_})
coef_df.to_csv("results/coefficients.csv", index=False)