"""
Number Guessing Game
A fun interactive game where players guess a random number
Created for B.Tech First Year Project
"""

import random
import json
import os
from datetime import datetime

class NumberGuessingGame:
    def __init__(self):
        self.player_name = ""
        self.score = 0
        self.games_played = 0
        self.total_attempts = 0
        self.high_scores_file = "high_scores.json"
        self.high_scores = self.load_high_scores()
    
    def load_high_scores(self):
        """Load previous high scores from file"""
        if os.path.exists(self.high_scores_file):
            try:
                with open(self.high_scores_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_high_scores(self):
        """Save high scores to file"""
        # Sort by score (highest first) and keep top 5
        self.high_scores.sort(key=lambda x: x['score'], reverse=True)
        self.high_scores = self.high_scores[:5]
        
        with open(self.high_scores_file, 'w') as f:
            json.dump(self.high_scores, f, indent=4)
    
    def welcome_screen(self):
        """Display welcome message and get player name"""
        print("\n" + "="*50)
        print("🎯 WELCOME TO THE NUMBER GUESSING GAME 🎯")
        print("="*50)
        print("\nI'll think of a number, and you try to guess it!")
        print("I'll give you hints if you're too high or too low.")
        
        self.player_name = input("\nEnter your name: ").strip()
        if not self.player_name:
            self.player_name = "Player"
        
        print(f"\nHello, {self.player_name}! Let's play! 🎮")
    
    def choose_difficulty(self):
        """Let player choose difficulty level"""
        print("\n" + "-"*30)
        print("SELECT DIFFICULTY LEVEL")
        print("-"*30)
        print("1. Easy 🌱 (1-50, 10 chances)")
        print("2. Medium 🌿 (1-100, 7 chances)")
        print("3. Hard 🌲 (1-200, 5 chances)")
        print("4. Extreme 🔥 (1-500, 4 chances)")
        
        while True:
            try:
                choice = int(input("\nEnter your choice (1-4): "))
                if choice == 1:
                    return 50, 10, "Easy"
                elif choice == 2:
                    return 100, 7, "Medium"
                elif choice == 3:
                    return 200, 5, "Hard"
                elif choice == 4:
                    return 500, 4, "Extreme"
                else:
                    print("Please enter 1, 2, 3, or 4")
            except ValueError:
                print("Invalid input! Please enter a number.")
    
    def give_hint(self, secret_number, attempts, max_number):
        """Give helpful hints based on attempts"""
        if attempts == 2:
            if secret_number % 2 == 0:
                print("💡 Hint: The number is EVEN")
            else:
                print("💡 Hint: The number is ODD")
        
        elif attempts == 4:
            if secret_number > max_number // 2:
                print("💡 Hint: The number is in the UPPER HALF")
            else:
                print("💡 Hint: The number is in the LOWER HALF")
        
        elif attempts == 6 and max_number > 100:
            # Give range hint
            lower = (secret_number // 10) * 10
            upper = lower + 10
            print(f"💡 Hint: The number is between {lower} and {upper}")
    
    def play_round(self):
        """Play one round of the game"""
        max_number, max_attempts, difficulty = self.choose_difficulty()
        secret_number = random.randint(1, max_number)
        attempts = 0
        guessed_numbers = []
        
        print(f"\n🎯 I'm thinking of a number between 1 and {max_number}")
        print(f"You have {max_attempts} attempts. Good luck!\n")
        
        while attempts < max_attempts:
            try:
                # Show remaining attempts
                remaining = max_attempts - attempts
                print(f"📊 Attempts left: {remaining}")
                
                # Get player's guess
                guess = int(input(f"Guess #{attempts + 1}: "))
                
                # Validate guess
                if guess < 1 or guess > max_number:
                    print(f"❌ Please guess between 1 and {max_number}")
                    continue
                
                if guess in guessed_numbers:
                    print("⚠️ You already guessed that number! Try a different one.")
                    continue
                
                # Add to guessed numbers
                guessed_numbers.append(guess)
                attempts += 1
                
                # Check guess
                if guess == secret_number:
                    # Calculate score based on attempts and difficulty
                    base_score = 100
                    attempt_bonus = (max_attempts - attempts + 1) * 10
                    difficulty_multiplier = {
                        "Easy": 1,
                        "Medium": 1.5,
                        "Hard": 2,
                        "Extreme": 3
                    }
                    
                    round_score = int((base_score + attempt_bonus) * difficulty_multiplier[difficulty])
                    
                    print(f"\n🎉🎉 CORRECT! 🎉🎉")
                    print(f"You guessed it in {attempts} attempts!")
                    print(f"✨ You earned {round_score} points! ✨")
                    
                    self.score += round_score
                    self.total_attempts += attempts
                    self.games_played += 1
                    
                    # Check if it's a high score
                    self.check_high_score(round_score)
                    
                    return True
                
                elif guess < secret_number:
                    print("📈 Too LOW! Try a higher number.")
                else:
                    print("📉 Too HIGH! Try a lower number.")
                
                # Give hint every 2 attempts
                if attempts % 2 == 0 and attempts < max_attempts:
                    self.give_hint(secret_number, attempts, max_number)
                
                # Show guessed numbers
                if guessed_numbers:
                    print(f"🔍 Numbers guessed: {sorted(guessed_numbers)}")
                
            except ValueError:
                print("❌ Invalid input! Please enter a NUMBER.")
        
        # Game over - no attempts left
        print(f"\n😞 GAME OVER! The number was {secret_number}")
        self.games_played += 1
        return False
    
    def check_high_score(self, round_score):
        """Check if current score is a high score"""
        high_score_entry = {
            'name': self.player_name,
            'score': self.score,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'games_played': self.games_played
        }
        
        self.high_scores.append(high_score_entry)
        self.save_high_scores()
    
    def show_high_scores(self):
        """Display high scores leaderboard"""
        print("\n" + "🏆"*15)
        print("   HIGH SCORES LEADERBOARD")
        print("🏆"*15)
        
        if not self.high_scores:
            print("\nNo high scores yet. Be the first!")
        else:
            for i, entry in enumerate(self.high_scores[:5], 1):
                print(f"\n{i}. {entry['name']}")
                print(f"   Score: {entry['score']} points")
                print(f"   Date: {entry['date']}")
    
    def show_statistics(self):
        """Display player statistics"""
        print("\n" + "📊"*10)
        print("   YOUR STATISTICS")
        print("📊"*10)
        
        print(f"\nPlayer: {self.player_name}")
        print(f"Games Played: {self.games_played}")
        print(f"Total Score: {self.score}")
        
        if self.games_played > 0:
            avg_score = self.score / self.games_played
            print(f"Average Score per game: {avg_score:.1f}")
        
        if self.total_attempts > 0 and self.games_played > 0:
            avg_attempts = self.total_attempts / self.games_played
            print(f"Average Attempts per win: {avg_attempts:.1f}")
    
    def show_rules(self):
        """Display game rules"""
        print("\n" + "📋"*10)
        print("   GAME RULES")
        print("📋"*10)
        print("""
1. Choose a difficulty level
2. Guess the secret number within the given attempts
3. Get hints after every 2 wrong guesses
4. Score more by guessing quickly
5. Higher difficulty = More points!
6. Try to make it to the leaderboard!
        """)
    
    def play(self):
        """Main game loop"""
        self.welcome_screen()
        
        while True:
            print("\n" + "="*40)
            print("           MAIN MENU")
            print("="*40)
            print("1. 🎮 Play Game")
            print("2. 📊 View My Statistics")
            print("3. 🏆 View High Scores")
            print("4. 📋 Game Rules")
            print("5. ❌ Exit")
            print("="*40)
            
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                self.play_round()
            elif choice == '2':
                self.show_statistics()
            elif choice == '3':
                self.show_high_scores()
            elif choice == '4':
                self.show_rules()
            elif choice == '5':
                print(f"\nThanks for playing, {self.player_name}! 🎯")
                print(f"Final Score: {self.score}")
                print("See you again soon! 👋")
                self.save_high_scores()
                break
            else:
                print("Invalid choice! Please enter 1-5")
            
            input("\nPress Enter to continue...")

# Run the game
if __name__ == "__main__":
    game = NumberGuessingGame()
    game.play()