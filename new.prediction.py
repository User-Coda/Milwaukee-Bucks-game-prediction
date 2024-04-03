import pandas as pd

# Load historical game data
historical_data = pd.read_excel('Bucks Games.xlsx')

# Function to calculate player-level statistics
def calculate_player_stats(data):
    player_stats = data.groupby('PLAYER_ID').agg({
        'PTS': 'mean',  # Average points scored
        # Add more statistics as needed
    }).reset_index()
    return player_stats

# Calculate player-level statistics
player_statistics = calculate_player_stats(historical_data)

# Function to predict score for future games
def predict_future_scores(future_games_data, player_stats):
    predicted_scores = []
    for index, row in future_games_data.iterrows():
        # Get player IDs for players in the future game
        home_players = row['HOME_PLAYERS'].split(',')  # Assuming this column contains player IDs separated by comma
        away_players = row['AWAY_PLAYERS'].split(',')  # Assuming this column contains player IDs separated by comma
        
        # Get player statistics for players in the future game
        home_player_stats = player_stats[player_stats['PLAYER_ID'].isin(home_players)]
        away_player_stats = player_stats[player_stats['PLAYER_ID'].isin(away_players)]
        
        # Calculate predicted score based on player statistics
        # You can use any method to predict the score here, like averaging the historical points of players
        predicted_score = (home_player_stats['PTS'].mean() + away_player_stats['PTS'].mean()) / 2
        predicted_scores.append(predicted_score)
    return predicted_scores

# Load future game data
future_games_data = pd.read_excel('test.data.xlsx')

# Predict scores for future games
future_predictions = predict_future_scores(future_games_data, player_statistics)
print(future_predictions)
