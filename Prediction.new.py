import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

def train_model(data):
    # Feature engineering and data preparation
    # Filter data for Milwaukee (MIL) team
    milwaukee_data = data[data['TEAM_ABBREVIATION'].str.strip() == 'MIL']

    # Group by 'GAME_ID' and sum the points for Milwaukee
    milwaukee_scores = milwaukee_data.groupby('GAME_ID')['PTS'].sum().reset_index()

    # Merge the total Milwaukee scores back to the original dataframe
    data = pd.merge(data, milwaukee_scores, how='left', on='GAME_ID', suffixes=('', '_MIL'))

    # Assuming 'PTS' represents the total points scored for the opponent
    data['OPP_Score'] = data['PTS'] - data['PTS_MIL']

    # Add a label column based on the comparison of scores
    data['Label'] = data.apply(lambda row: 1 if row['PTS_MIL'] > row['OPP_Score'] else 0, axis=1)

    # Split the data into training and test sets
    train_data, _ = train_test_split(data, test_size=0.2, random_state=42)

    train_data = train_data.dropna(subset=['PLUS_MINUS'])  

    # One-hot encoding for categorical columns
    data = pd.get_dummies(data, columns=['TEAM_ABBREVIATION'])

    # Choose features (X) and labels (y) for training
    X_train = train_data[['TEAM_ID','GAME_ID','PLAYER_ID', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PF', 'PTS', 'PLUS_MINUS']]
    y_train = train_data['PLUS_MINUS']

    # Initialize the regression model (e.g., Random Forest Regressor)
    model = RandomForestRegressor()

    # Train the model
    model.fit(X_train, y_train)

    return model

def predict_future_games(model, future_games_data):
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
    return future_predictions

# Load the training data
df = pd.read_excel('Bucks Games.xlsx')
# Train the model
model = train_model(df)

# Load future games data
future_games_data = pd.read_excel('future_games_data.xlsx')

# Predictions for future games
future_predictions = predict_future_games(model, future_games_data)
print(future_predictions)
