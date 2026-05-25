import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE 
import joblib  # Used to save the trained model object

print("Downloading dataset and preparing training data...")
url = "https://storage.googleapis.com/download.tensorflow.org/data/creditcard.csv"
df = pd.read_csv(url)

X = df.drop(columns=['Class'])
y = df['Class']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Applying SMOTE balancing...")
smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

print("Training Random Forest Model (using all CPU cores)...")
model = RandomForestClassifier(n_estimators=100, n_jobs=-1, random_state=42)
model.fit(X_train_res, y_train_res)


print("Saving model artifacts...")
joblib.dump(model, "fraud_model.pkl") 
joblib.dump(X_test.iloc[0], "input_template.pkl")

print("✅ Training complete! 'fraud_model.pkl' has been generated successfully.")
