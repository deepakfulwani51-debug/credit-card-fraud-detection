import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
import joblib

print("Generating realistic transaction data distribution...")
np.random.seed(42)
n_samples = 10000

# 1. Generate realistic transaction amounts (mostly small entries, a few large ones)
amounts = np.random.exponential(scale=300, size=n_samples) + 5

# 2. Generate realistic times (seconds in a full day: 0 to 86400)
times = np.random.uniform(0, 86400, size=n_samples)

df = pd.DataFrame({'Amount': amounts, 'Time': times})

# 3. Establish a logical real-world rule for Fraud:
# Transactions with an Amount greater than 1500 Rupees are flagged as high-risk fraud (1).
# Transactions under 1500 Rupees are marked as legitimate/safe (0).
df['Class'] = np.where(df['Amount'] > 1500, 1, 0)

X = df[['Amount', 'Time']]
y = df['Class']

print(f"Initial Imbalance: {sum(df['Class'] == 1)} fraud cases out of {n_samples} total transactions.")

print("Applying SMOTE to balance the minority class...")
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

print("Training Random Forest Classifier on clean patterns...")
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

print("Saving updated model artifacts...")
template_columns = ['Amount', 'Time']
joblib.dump(template_columns, "input_template.pkl")
joblib.dump(model, "fraud_model.pkl")
print("🚀 Successfully fixed the model brains! Clean decision boundary set at 1500.")
