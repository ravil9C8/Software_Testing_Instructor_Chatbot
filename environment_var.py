import os

# Iterate over all environment variables and print them
for key, value in os.environ.items():
    print(f"{key}: {value}")
    print(end="\n")