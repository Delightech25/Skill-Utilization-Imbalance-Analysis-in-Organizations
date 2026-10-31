import pandas as pd
import numpy as np

np.random.seed(42)

skills = ["Python", "ML", "SQL", "Management", "Cloud"]

data = []

for i in range(200):
    employee_skills = np.random.randint(1, 10, len(skills))
    required_skills = np.random.randint(1, 10, len(skills))
    
    utilization = required_skills / employee_skills
    avg_util = np.mean(utilization)

    if avg_util < 0.7:
        label = "Underutilized"
    elif avg_util > 1.2:
        label = "Overloaded"
    else:
        label = "Balanced"

    row = list(employee_skills) + list(required_skills) + [avg_util, label]
    data.append(row)

columns = [f"E_{s}" for s in skills] + \
          [f"R_{s}" for s in skills] + \
          ["avg_utilization", "label"]

df = pd.DataFrame(data, columns=columns)
df.to_csv("dataset.csv", index=False)

print("Dataset created successfully.")