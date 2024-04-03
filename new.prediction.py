# Load the necessary libraries
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
    home_players_scores = {}
    away_players_scores = {}
    
    for index, row in future_games_data.iterrows():
        # Get team IDs for the home and away teams
        home_team_id = row['HOME_TEAM_ID']
        away_team_id = row['AWAY_TEAM_ID']
        
        # Get player IDs for players in the future game
        home_player_ids = future_games_data.loc[index, 'HOME_PLAYER_IDS']
        away_player_ids = future_games_data.loc[index, 'AWAY_PLAYER_IDS']
        
        # Check if player IDs are not NaN
        if not pd.isna(home_player_ids):
            home_player_ids = [int(float(player_id)) for player_id in str(home_player_ids).split()]
        else:
            home_player_ids = []
            
        if not pd.isna(away_player_ids):
            away_player_ids = [int(float(player_id)) for player_id in str(away_player_ids).split()]
        else:
            away_player_ids = []

        # Get player statistics for players in the future game
        home_player_stats = player_stats[player_stats['PLAYER_ID'].isin(home_player_ids)]
        away_player_stats = player_stats[player_stats['PLAYER_ID'].isin(away_player_ids)]
        
        # Calculate predicted score based on player statistics
        home_team_score = home_player_stats['PTS'].sum()
        away_team_score = away_player_stats['PTS'].sum()
        
        # Store individual player scores for home team
        for player_id, points in home_player_stats.set_index('PLAYER_ID')['PTS'].to_dict().items():
            home_players_scores[player_id] = points
        
        # Store individual player scores for away team
        for player_id, points in away_player_stats.set_index('PLAYER_ID')['PTS'].to_dict().items():
            away_players_scores[player_id] = points
        
        predicted_scores.append({
            'home_team_score': home_team_score,
            'away_team_score': away_team_score,
        })
    
    return predicted_scores, home_players_scores, away_players_scores

# Load future game data
future_games_data = pd.read_excel('test.data.xlsx')
# Predict scores for future games
future_predictions, home_players_scores, away_players_scores = predict_future_scores(future_games_data, player_statistics)

# Print the predicted scores for each future game
for i, prediction in enumerate(future_predictions):
    print(f"Game {i+1}:")
    print(f"Home Team Score: {prediction['home_team_score']}")
    print(f"Away Team Score: {prediction['away_team_score']}")
    print()

# Print the scores for each player in the home team
print("Home Team Players and Their Scores:")
for player_id, score in home_players_scores.items():
    print(f"Player ID: {player_id}, Points: {score}")

# Print the scores for each player in the away team
print("Away Team Players and Their Scores:")
for player_id, score in away_players_scores.items():
    print(f"Player ID: {player_id}, Points: {score}")
