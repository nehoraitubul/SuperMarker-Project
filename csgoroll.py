import random
import math

total = 80
current = 1
current_lose = 0
current_win = 0
counter = 0
green_hits = 0


total_iterations = 0

# Define the probabilities for each option
probabilities = [0.4666, 0.4666, 0.0666]
options = ['a', 'b', 'c']

# Initialize counts for each option
counts = {'a': 0, 'b': 0, 'c': 0}

greatest_total = total


while total > 0:
    if greatest_total < total:
        greatest_total = total
    counter += 1
    total_iterations += 1
    while (current*13) + (current_lose) <= 0:
        current = math.ceil(((abs(current_lose) + current + 2) / 14) * 100) / 100
    print("current = ", current)
    selected_option = random.choices(options, probabilities)[0]
    if selected_option != 'c':
        total = total - current
        current_lose -= current
    if selected_option == 'c':
        current_win += (current*14)-(current_lose+current)
        current_lose = 0
        # print(total)
        total += current*13
        # print(total)
        current = 1
        # print("counter", counter)
        counter = 0
        green_hits += 1

    # if counter == 100:
    #     odds =  counter / total_iterations
    #     print("odds", odds)
    #     print("green_hits", green_hits)
    #     break

print("LOST")
print("total", total)
print("current_lose", current_lose)
print("counter", counter)
print("green_hits", green_hits)
print("total rounds in this run: ", total_iterations)
print("the most coins i had in this run: ", greatest_total)


# Probability of success
p = 0.9334

# Total number of trials
n = counter

# Number of successes
k = counter

# Calculate the probability using the binomial probability formula
probability_decimal1 = math.comb(n, k) * (p ** k) * ((1 - p) ** (n - k))
probability_decimal2 = (((p/100) ** k) * 100)

print("The odds for this no green run is:", probability_decimal1)
print("The odds for this no green run is:", probability_decimal2)

# Convert the probability to a percentage
probability_percentage = probability_decimal1 * 100
print("The odds for this no green run is:", probability_percentage)

# Run the selection process 100 times
# for _ in range(100):
#     selected_option = random.choices(options, probabilities)[0]
#     counts[selected_option] += 1
#
# # Print the counts for each option
# for option, count in counts.items():
#     print(f"Option {option}: {count} times")