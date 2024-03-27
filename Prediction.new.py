import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# Step 1: Load the historical game data
historical_data = pd.read_excel('Bucks Games.xlsx')

# Step 2: Feature engineering and data preparation

# We need to select relevant features and preprocess the data.
# For simplicity, let's assume we are interested in predicting the point difference (PLUS_MINUS) of the Milwaukee Bucks team.

# Filter data for Milwaukee Bucks (MIL) team
milwaukee_data = historical_data[historical_data['TEAM_ABBREVIATION'].str.strip() == 'MIL']

# Group by 'GAME_ID' and sum the points for Milwaukee Bucks
milwaukee_scores = milwaukee_data.groupby('GAME_ID')['PTS'].sum().reset_index()

# Merge the total Milwaukee scores back to the original dataframe
historical_data = pd.merge(historical_data, milwaukee_scores, how='left', on='GAME_ID', suffixes=('', '_MIL'))

# Assuming 'PTS' represents the total points scored for the opponent
historical_data['OPP_Score'] = historical_data['PTS'] - historical_data['PTS_MIL']

# Step 3: Split the data into training and testing sets
train_data, test_data = train_test_split(historical_data, test_size=0.2, random_state=42)

# Step 4: Choose features (X) and labels (y) for training and testing
X_train = train_data[['FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 
                      'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PF', 'PTS', 'PLUS_MINUS']]
y_train = train_data['PLUS_MINUS']

X_test = test_data[['FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 
                    'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PF', 'PTS', 'PLUS_MINUS']]
y_test = test_data['PLUS_MINUS']

# Step 5: Initialize and train the RandomForestRegressor model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Step 6: Evaluate the model
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
print(f'Mean Squared Error: {mse}')
