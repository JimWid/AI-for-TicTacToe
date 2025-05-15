import TicTacToe
import random

# Creating AI agent or QLearningAgent
class AI_Agent:
    def __init__(self, alpha, gamma, epsilon, epsilon_decay, min_epsilon, player_mark):
        self.alpha = alpha #0.3 # Learning Rate
        self.gamma = gamma #0.95 # Discount factor
        self.epsilon = epsilon #1.0 # Exploration Rate
        self.epsilon_decay = epsilon_decay #0.9995
        self.min_epsilon = min_epsilon

        self.player_mark = player_mark

        self.q_table = {}

    def get_q_value(self, state, action):
        return self.q_table.get(state, {}).get(action, 0.0)

    # Function to choose valid moves and play
    def choose_action(self, game, available_actions):
        if not available_actions:
            return None # This should not happen if game is not over ofc
        
        if random.uniform(0, 1) < self.epsilon:
            # Exploration: Choose a random action
            return random.choice(available_actions)
        
        else:
            # Exploitation: Choose the action with the highest Q-value
            current_state = game.get_board_state_tuple()
            q_values = {action: self.get_q_value(current_state, action) for action in available_actions}
            
            # If all q_values are 0, pick randomly
            if all(values == 0 for values in q_values.values()):
                return random.choice(available_actions)
            
            return max(q_values, key=q_values.get)
        
    # Function that manages the Rewards 
    def get_reward(self, game, action_taken_by_agent):
        if game.current_winner == self.player_mark:
            return 10.0 # Win
        elif game.current_winner is not None and game.current_winner != self.player_mark:
            return -10.0 # Loss
        elif game.check_if_tie():
            return 1.0 # Tie is better than losing
        elif not action_taken_by_agent: # Opponet made a move leading to this state 
            return 0.0
        else:
            return -0.1 # Small penalty for each move, encourages faster wins

    # Updates the Q table
    def update_q_table(self, old_state, action, reward, new_state, game):
        
        old_q_vlaue = self.get_q_value(old_state, action)

        next_available_actions = game.get_empty_cells()

        if not next_available_actions or game.is_game_over():
            max_q_prime = 0.0
        else:
            q_prime_values = [self.get_q_value(new_state, new_action) for new_action in next_available_actions]
            max_q_prime = max(q_prime_values) if q_prime_values else 0.0
        
        # Q-learning formula
        new_q_value = old_q_vlaue + self.alpha * (reward + self.gamma * max_q_prime - old_q_vlaue)

        # Update the Q-table
        if old_state not in self.q_table:
            self.q_table[old_state] = {}
        self.q_table[old_state][action] = new_q_value

    def decay_epsilon(self):
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)


# Main Function that trains the AI
alpha = 0.1 # Learning Rate
gamma = 0.9 # Discount factor
epsilon = 1.0 # Exploration Rate
epsilon_decay = 0.999
min_epsilon = 0.1

def train_ai(episodes):

    player_x = AI_Agent(alpha, gamma, epsilon, epsilon_decay, min_epsilon, player_mark = "X")
    player_o = AI_Agent(alpha, gamma, epsilon, epsilon_decay, min_epsilon, player_mark = "O")
    env = TicTacToe.TicTacToe()

    stats = {"X_wins": 0, "O_wins": 0, "Ties": 0}

    for episode in range(episodes):
        env.reset_board() # Creating enviroment
        current_player = player_x
        oppenent_player = player_o

        turn = 0
        game_history = []

        while not env.is_game_over():
            old_state = env.get_board_state_tuple()
            available_actions = env.get_empty_cells()

            if not available_actions: # Should be caught by is_game_over, but as a safeguard 
                break

            action = current_player.choose_action(env, available_actions)
            
            if action is None: #No valid moves (should not happen in a normal game)
                break

            env.make_move(action, current_player.player_mark)
            new_state = env.get_board_state_tuple()

            # Stores step's info
            # For reward to be determined at the of each game or opponent's turn
            game_history.append({'old_state': old_state,
                                 'action': action,
                                 'new_state': new_state,
                                 'agent': current_player,
                                 'turn': turn})

            # Switch player
            if current_player == player_x:
                current_player = player_o
                #oppenent_player = player_x
            else:
                current_player = player_x
                #oppenent_player = player_o

            turn += 1

        # Game ended, assigning rewards and updating Q-tables
        final_reward_x = player_x.get_reward(env, False) # False as game is over
        final_reward_o = player_o.get_reward(env, False)

        # Going through the game history in reverse to assign delayed rewards
        for i in range(len(game_history) -1, -1, -1):
            step = game_history[i]
            agent_acted = step["agent"]
            old_s = step["old_state"]
            act = step["action"]
            new_s = step["new_state"] # The state after a player(AI/s) made a move

            reward = 0

            if env.is_game_over(): # If this move led to game over
                if agent_acted.player_mark == 'X':
                    reward = final_reward_x
                else: # agent_acted.player_letter == 'O'
                    reward = final_reward_o
            else:
                reward = agent_acted.get_reward(env, True) # True because agent made this move

            # Updating q_table for each agent action/move
            agent_acted.update_q_table(old_s, act, reward, new_s, env)

        # Update stats
        if env.current_winner == "X":
            stats["X_wins"] += 1
        elif env.current_winner == "O":
            stats["O_wins"] += 1
        else:
            stats["Ties"] += 1

        # Decay epsilon for both AI's
        player_x.decay_epsilon()
        player_o.decay_epsilon()

        # Printing out stats
        if (episode + 1) % (episodes // 100) == 0 or episode == 0:
            print(f"Episode {episode + 1} / {episodes}")
            print(f"Stats: X Wins: {stats["X_wins"]}, O Wins: {stats["O_wins"]}, Ties: {stats["Ties"]}")

    # Printing Final Stats
    print("\nTraining Finished!")
    print(f"Final Stats: X Wins: {stats['X_wins']}, O Wins: {stats['O_wins']}, Ties: {stats['Ties']}")
    print(f"Player X Q-table size: {len(player_x.q_table)}")
    print(f"Player O Q-table size: {len(player_o.q_table)}")

    # Returning Trained AI's
    return player_x, player_o

def play_with_ai(ai_agent, human_player_mark):
    game = TicTacToe.TicTacToe()
    ai_agent.epsilon = 0 # Exploit only
    human_turn = (human_player_mark == "X")

    while not game.is_game_over():
        game.display_board()
        available_actions = game.get_empty_cells()

        if human_turn:
            print(f"Human Player ({human_player_mark}), your turn.")
            while True:
                try:
                    move = int(input("Enter move (1-9): ")) - 1
                    if move in available_actions:
                        game.make_move(move, human_player_mark)
                        break
                    else:
                        print("Invalid move. Cell not empty or out of bounds. Try again.")
                except IndexError:
                    print("Invalid input. Row or column out of bounds.")

        else:
            print(f"AI player ({ai_agent.player_mark}), AI's turn.")
            action = ai_agent.choose_action(game, available_actions)
            if action:
                game.make_move(action, ai_agent.player_mark)
            else: # Should not happen if game is not over
                print("AI has no moves available but game is not over?")
                break   
        
        if game.is_game_over():
            game.display_board()
            if game.current_winner:
                print(f"Player {game.current_winner} Wins!")
            elif game.check_if_tie():
                print("It is a Tie!")
            break

        human_turn = not human_turn

if __name__ == "__main__":
    # --- Training Phase ---
    print("Starting AI Training...")
    
    episodes = 100_000
    trained_ai_x, trained_ai_o = train_ai(episodes)

    human_player_mark = "O"
    print(f"\nYou are player {human_player_mark}. AI is player X.")

    #play_with_ai(trained_ai_o, human_player_mark) # Play against O
    play_with_ai(trained_ai_x, human_player_mark) # Play against X