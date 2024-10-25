from bs4 import BeautifulSoup
from collections import Counter
import statistics
import random
import psycopg2


with open("index.html", "r") as file:
    html_content = file.read()


# Parsing HTML with BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")


# colors for each day
color_data = []
for row in soup.find_all("tbody")[0].find_all("tr"):
    day = row.find_all("td")[0].text.strip()
    colors = row.find_all("td")[1].text.strip().replace(" ", "").split(",")
    color_data.extend(colors)

print(color_data)


# .........................QUESTION ONE (MEAN COLOUR).........................

# occurrences of each color
color_counts = Counter(color_data)

# the color with the highest count
mean_color = color_counts.most_common(1)[0][0]
print("Mean color:", mean_color)



# .........................QUESTION TWO (MOST WORN COLOR).........................

most_worn_color = mean_color
print("Most worn color:", most_worn_color)



# .........................QUESTION THREE (MEDIAN COLOR).........................

# colors by count and then lexicographically
sorted_colors = sorted(color_counts.items(), key=lambda x: (x[1], x[0]))
median_color = sorted_colors[len(sorted_colors) // 2][0]
print("Median color:", median_color)



# .........................QUESTION FOUR (VARIANCE OF COLORS).........................

# frequencies as a list
frequencies = list(color_counts.values())
variance = statistics.variance(frequencies)
print("Variance of color frequencies:", variance)


# .........................QUESTION FIVE (PROBABILITY OF SELECTING RED).........................

# probability of red
total_colors = len(color_data)
red_count = color_counts.get("RED", 0)
probability_red = red_count / total_colors
print("Probability of choosing Red:", probability_red)

# .........................QUESTION SIX (SAVE COLORS & FREQUENCIES TO POSTGRESQL DATABASE).........................



# Connecting to PostgreSQL
conn = psycopg2.connect(
    dbname="enter_name", user="postgres", password="enter_password", host="localhost"
)
cur = conn.cursor()

# Creating table
cur.execute("""
    CREATE TABLE IF NOT EXISTS color_frequencies (
        color VARCHAR(50),
        frequency INT
    );
""")

# Inserting data
for color, freq in color_counts.items():
    cur.execute("INSERT INTO color_frequencies (color, frequency) VALUES (%s, %s)", (color, freq))

conn.commit()
cur.close()
conn.close()



# .........................QUESTION SEVEN (RECURSIVE SEARCH ALGORITHM).........................

def recursive_search(lst, target, index=0):
    if index >= len(lst):
        return -1  # Not found
    if lst[index] == target:
        return index  # Found
    return recursive_search(lst, target, index + 1)


numbers = [1, 2, 3, 4, 5]
target = 3
print("Index of target:", recursive_search(numbers, target))



# .........................QUESTION EIGHT (GENERATE RANDOM 4-DIGIT BINARY NUMBER AND COVERT TO BASE 10).........................

# Generating a random 4-digit binary number
binary_number = ''.join(random.choice('01') for _ in range(4))
base_10_number = int(binary_number, 2)
print("Binary number:", binary_number)
print("Base 10 equivalent:", base_10_number)


# .........................QUESTION NINE (SUM OF FIRST 50 FIBONACCI SEQUENCE NUMBERS).........................


def fibonacci_sum(n):
    a, b = 0, 1
    total = 0
    for _ in range(n):
        total += a
        a, b = b, a + b
    return total

print("Sum of first 50 Fibonacci numbers:", fibonacci_sum(50))
