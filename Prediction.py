import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Load the dataset
df = pd.read_excel('Bucks Games.xlsx')

# Feature engineering and data preparation
# Filter data for Milwaukee (MIL) team
milwaukee_data = df[df['TEAM_ABBREVIATION'].str.strip() == 'MIL']

# Group by 'GAME_ID' and sum the points for Milwaukee
milwaukee_scores = milwaukee_data.groupby('GAME_ID')['PTS'].sum().reset_index()

# Merge the total Milwaukee scores back to the original dataframe
df = pd.merge(df, milwaukee_scores, how='left', on='GAME_ID', suffixes=('', '_MIL'))

# Assuming 'PTS' represents the total points scored for the opponent
df['OPP_Score'] = df['PTS'] - df['PTS_MIL']

# Add a label column based on the comparison of scores
df['Label'] = df.apply(lambda row: 1 if row['PTS_MIL'] > row['OPP_Score'] else 0, axis=1)

# Split the data into training and test sets
train_data, test_data = train_test_split(df, test_size=0.2, random_state=42)

train_data = train_data.dropna(subset=['PLUS_MINUS'])
test_data = test_data.dropna(subset=['PLUS_MINUS'])  

# One-hot encoding for categorical columns
df = pd.get_dummies(df, columns=['TEAM_ABBREVIATION'])

# Choose features (X) and labels (y) for training
X_train = train_data[['TEAM_ID','GAME_ID','PLAYER_ID', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PF', 'PTS', 'PLUS_MINUS']]
y_train = train_data['PLUS_MINUS']

# Choose features (X) and labels (y) for testing
X_test = test_data[['TEAM_ID','GAME_ID','PLAYER_ID', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PF', 'PTS', 'PLUS_MINUS']]
y_test = test_data['PLUS_MINUS']


# Initialize the regression model (e.g., Random Forest Regressor)
model = RandomForestRegressor()

# Train the model
model.fit(X_train, y_train)

# Predictions for the test set
predictions = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, predictions)
print(f'Mean Squared Error: {mse}')

# Now, assuming you have future game data stored in a DataFrame named future_games_data
# Ensure that future_games_data contains the necessary columns including TEAM_ID, GAME_ID, and PLAYER_ID
# For prediction, you may select relevant features from the future games data
selected_features = ['TEAM_ID','GAME_ID','PLAYER_ID', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PF', 'PTS', 'PLUS_MINUS']
future_games_data_selected = future_games_data[selected_features]

# Ensure that future_games_data_selected is a DataFrame with appropriate features
# Drop rows with NaN values in future_games_data_selected
future_games_data_selected = future_games_data_selected.dropna()

# Ensure valid data types in future_games_data_selected
future_games_data_selected = future_games_data_selected.astype(float)  

# Predictions for future games
future_predictions = model.predict(future_games_data_selected)
print(future_predictions)
