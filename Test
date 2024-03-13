import pandas as pd
import joblib  # for loading the trained model

# Load the trained model
model = joblib.load('basketball_model.pkl')

# Load the future games data into a DataFrame
future_games_data = pd.read_excel('Test.data.xlsx')  # Example: Load from an Excel file

# Select only the desired features for prediction
selected_features = ['TEAM_ID','GAME_ID','PLAYER_ID','FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PF', 'PTS', 'PLUS_MINUS']  # Example: Selecting certain features
future_games_data_selected = future_games_data[selected_features]

# Make predictions on the selected features
future_predictions = model.predict(future_games_data_selected)

# Print or use the predictions as needed
print(future_predictions)
