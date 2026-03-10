import pandas as pd
from collections import Counter
import random
import matplotlib.pyplot as plt

# -------------------------
# 1. Load dataset
# -------------------------
file_path = "data/lottery_data.csv"
df = pd.read_csv(file_path)

# -------------------------
# 2. Clean dataset
# -------------------------
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df["drawdate"] = pd.to_datetime(df["drawdate"], dayfirst=True)
df = df.sort_values("drawdate")

print("Dataset size:", df.shape)

# -------------------------
# 3. Define main ball columns
# -------------------------
ball_columns = [
    "ball_1",
    "ball_2",
    "ball_3",
    "ball_4",
    "ball_5",
    "ball_6",
]

# -------------------------
# 4. Historical frequency analysis
# -------------------------
all_numbers = []

for col in ball_columns:
    all_numbers.extend(df[col])

counts = Counter(all_numbers)

print("\nTop 10 most frequent numbers:")
for number, count in counts.most_common(10):
    print(f"{number} → {count} times")

# -------------------------
# 5. Recent draw analysis
# -------------------------
recent_df = df.tail(20)

recent_numbers = []

for col in ball_columns:
    recent_numbers.extend(recent_df[col])

recent_counts = Counter(recent_numbers)

print("\nHot numbers (last 20 draws):")
for number, count in recent_counts.most_common(10):
    print(f"{number} → {count} times")

# -------------------------
# 6. Ranking system
# -------------------------
scores = {}

for number in range(1, 60):
    historical_score = counts.get(number, 0)
    recent_score = recent_counts.get(number, 0)

    # Give extra weight to recent appearances
    score = historical_score + (recent_score * 2)

    scores[number] = score

ranked_numbers = sorted(scores.items(), key=lambda x: x[1], reverse=True)

print("\nEstimated strongest numbers:")
for number, score in ranked_numbers[:10]:
    print(f"{number} → score: {score}")

# -------------------------
# 7. Probability-style ranking
# -------------------------
total_score = sum(scores.values())

print("\nEstimated probability ranking:")
for number, score in ranked_numbers[:10]:
    probability = (score / total_score) * 100
    print(f"{number} → {probability:.2f}%")

# -------------------------
# 8. Cold numbers
# -------------------------
print("\nCold numbers (not seen in last 20 draws):")
all_possible_numbers = range(1, 60)

cold_numbers = []

for number in all_possible_numbers:
    if number not in recent_counts:
        cold_numbers.append(number)

print(cold_numbers)

# -------------------------
# 9. Suggested combination
# -------------------------
top_candidates = [num for num, score in ranked_numbers[:20]]
suggested_numbers = sorted(random.sample(top_candidates, 6))

print("\nSuggested combination based on ranking:")
print(suggested_numbers)

# -------------------------
# 10. Frequency chart
# -------------------------
numbers = list(counts.keys())
frequencies = list(counts.values())

plt.figure(figsize=(12, 6))
plt.bar(numbers, frequencies)
plt.title("Lottery Number Frequency Distribution")
plt.xlabel("Number")
plt.ylabel("Times Appeared")
plt.xticks(range(1, 60, 2))
plt.tight_layout()
plt.show()