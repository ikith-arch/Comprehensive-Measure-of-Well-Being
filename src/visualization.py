import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Create image folder automatically
os.makedirs("static/images", exist_ok=True)


# Load Dataset
df = pd.read_csv("dataset/HDI.csv")

print("Dataset Loaded Successfully")


# -------------------------------
# 1. Top 10 HDI Countries
# -------------------------------

top10 = df.sort_values(
    by="HDI",
    ascending=False
).head(10)


plt.figure(figsize=(10, 6))

sns.barplot(
    data=top10,
    x="HDI",
    y="Country",
    hue="Country",
    palette="viridis",
    legend=False
)

plt.title("Top 10 Countries by HDI")
plt.xlabel("HDI Value")
plt.ylabel("Country")

plt.tight_layout()

plt.savefig(
    "static/images/top10_hdi.png",
    dpi=300
)

plt.close()


# -------------------------------
# 2. HDI Distribution
# -------------------------------

plt.figure(figsize=(8, 5))

sns.histplot(
    data=df,
    x="HDI",
    bins=15,
    kde=True,
    color="green"
)

plt.title("HDI Distribution")
plt.xlabel("HDI Value")
plt.ylabel("Number of Countries")

plt.tight_layout()

plt.savefig(
    "static/images/hdi_distribution.png",
    dpi=300
)

plt.close()


# -------------------------------
# 3. Correlation Heatmap
# -------------------------------

plt.figure(figsize=(10, 8))


numeric_df = df.drop(
    columns=["Country"]
)


corr = numeric_df.corr()


sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)


plt.title("Feature Correlation Matrix")

plt.tight_layout()

plt.savefig(
    "static/images/correlation.png",
    dpi=300
)

plt.close()


print("================================")
print("Charts Generated Successfully!")
print("================================")