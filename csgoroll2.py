import random
import math

# Initial values
total = 80  # Starting with 80 coins
current = 1  # Initial bet of 1 coin (1% of total)
current_lose = 0
current_win = 0
counter = 0
green_hits = 0
greatest_total = total
total_iterations = 0
bets_list = []  # List to store all bets placed in each round

# Probabilities and options
probabilities = [0.4666, 0.4666, 0.0666]  # 'c' has a 6.66% chance (the win)
options = ['a', 'b', 'c']

# Main simulation loop
while total > 0:
    greatest_total = max(greatest_total, total)
    counter += 1
    total_iterations += 1

    # Ensure current remains reasonable (bet should not go negative or extremely high)
    if (current * 13) + current_lose <= 0:
        current = math.ceil(((abs(current_lose) + current + 2) / 14) * 100) / 100

    # Round the current bet to 2 decimal places before recording it
    current = round(current, 2)
    bets_list.append(current)

    # Select option based on probabilities
    selected_option = random.choices(options, probabilities)[0]

    # Process result
    if selected_option != 'c':  # Not a win
        total -= current  # Deduct current bet from total
        current_lose -= current  # Add to current losses
        # Increase bet by 10% to 20% after each loss (to recover), rounded to 2 decimal places
        current += current * random.uniform(0.1, 0.2)
    else:  # Win
        winnings = current * 14 - (current_lose + current)
        total += current * 13  # Add winnings to total
        current_win += winnings
        current_lose = 0  # Reset losses
        current = 1  # Reset bet to 1 coin
        green_hits += 1
        counter = 0  # Reset counter after a win

    # Exit if funds are exhausted
    if total <= 0:
        break

# Simulation Results
print("LOST")
print("Total:", total)
print("Current Losses:", current_lose)
print("Green Hits:", green_hits)
print("Total Rounds:", total_iterations)
print("Greatest Total Coins:", greatest_total)

# Print the list of bets placed in each round
print("Bets placed in each round:", bets_list)

# Probability Calculation after losing streak
p = 0.9334  # Probability of not hitting 'c'
k = counter  # Length of losing streak

# Use binomial probability formula to estimate odds
if k > 0:
    probability_decimal = (p ** k) * 100
    print("The odds for this no-green run is:", probability_decimal, "%")
else:
    print("No losing streak to calculate odds for.")
