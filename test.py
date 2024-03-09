import random

# Set the lambda parameter (inverse of the mean)
lambd = 0.5  # You can adjust this based on your desired mean

# Generate a random number from the exponential distribution
random_number = random.expovariate(lambd)

print("Generated random number:", random_number)