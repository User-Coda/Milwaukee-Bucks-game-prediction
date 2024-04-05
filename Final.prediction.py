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

# Function to predict score for one future game and allocate points to players
def predict_and_allocate_points(future_game_data, player_stats):
    # Get team IDs for the home and away teams
    home_team_id = future_game_data['HOME_TEAM_ID'].iloc[0]
    away_team_id = future_game_data['AWAY_TEAM_ID'].iloc[0]
    
    # Convert player IDs to strings and split them
    home_player_ids = future_game_data['HOME_PLAYER_IDS'].astype(str).str.split('\n')
    away_player_ids = future_game_data['AWAY_PLAYER_IDS'].astype(str).str.split('\n')

    # Extract player IDs from the lists and convert to integers
    home_player_ids = [int(player_id) for sublist in home_player_ids for player_id in sublist if player_id.strip()]
    away_player_ids = [int(player_id) for sublist in away_player_ids for player_id in sublist if player_id.strip()]

    # Get player statistics for players in the future game
    home_player_stats = player_stats[player_stats['PLAYER_ID'].isin(home_player_ids)]
    away_player_stats = player_stats[player_stats['PLAYER_ID'].isin(away_player_ids)]
    
    # Divide player scores by ten and round to nearest whole number
    home_player_stats['PTS'] = round(home_player_stats['PTS'] / 10)
    away_player_stats['PTS'] = round(away_player_stats['PTS'] / 10)
    
    # Calculate total points for each team and round to nearest whole number
    home_team_total_points = round(home_player_stats['PTS'].sum())
    away_team_total_points = round(away_player_stats['PTS'].sum())
    
    # Allocate points to home team players
    home_player_allocation = {}
    for index, row in home_player_stats.iterrows():
        player_id = row['PLAYER_ID']
        player_points = row['PTS']
        allocation = min(player_points, home_team_total_points)
        home_player_allocation[player_id] = round(allocation)
    
    # Allocate points to away team players
    away_player_allocation = {}
    for index, row in away_player_stats.iterrows():
        player_id = row['PLAYER_ID']
        player_points = row['PTS']
        allocation = min(player_points, away_team_total_points)
        away_player_allocation[player_id] = round(allocation)
    
    # Return total scores and allocated points for home and away teams
    return home_team_total_points, away_team_total_points, home_player_allocation, away_player_allocation



# Load future games data from Excel file (replace 'Test.data.xlsx' with the actual file path)
future_game_data = pd.read_excel('Test.data.xlsx')

# Predict scores for one future game and allocate points to players
home_team_score, away_team_score, home_allocation, away_allocation = predict_and_allocate_points(future_game_data, player_statistics)

# Print predicted scores for the game
print("\nPredicted Scores:")
print(f"Home Team Score: {home_team_score}")
print(f"Away Team Score: {away_team_score}")

# Print allocated points for home team players
print("\nHome Team Players and Their Allocated Points:")
for player_id, allocation in home_allocation.items():
    print(f"Player ID: {player_id}, Allocated Points: {allocation}")

# Print allocated points for away team players
print("\nAway Team Players and Their Allocated Points:")
for player_id, allocation in away_allocation.items():
    print(f"Player ID: {player_id}, Allocated Points: {allocation}")
