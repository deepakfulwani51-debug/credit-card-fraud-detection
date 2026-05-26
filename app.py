import os
import sys
import joblib
import pandas as pd

print("\n--- Live Transaction Checker App Booted ---\n")

# Load compiled binary artifacts defensively
if not os.path.exists("fraud_model.pkl") or not os.path.exists("input_template.pkl"):
    print("Error: Missing serialized model artifact brains. Aborting.")
    sys.exit(1)

model = joblib.load("fraud_model.pkl")
template_cols = joblib.load("input_template.pkl")

def get_user_prediction():
    try:
        print("Please enter transaction details for analysis:")
        amount = float(input("Enter Transaction Amount: "))
        trans_time = float(input("Enter Time (seconds elapsed): "))
        
        # Build structural dataframe mapping to exact baseline schema order
        input_data = pd.DataFrame([[amount, trans_time]], columns=template_cols)
        
        # Calculate evaluations
        prediction = model.predict(input_data)[0]
        probabilities = model.predict_proba(input_data)[0]
        confidence = probabilities[prediction] * 100
        
        print("\n--- ANALYSIS RESULT ---")
        if prediction == 1:
            print(f"⚠️ ALERT: High Risk! Potential Fraud Detected. (Confidence: {confidence:.2f}%)")
        else:
            print(f"✅ Approved: Low Risk Transaction. (Confidence: {confidence:.2f}%)")
        print("\n")
    except Exception as e:
        print(f"Error parsing operational input criteria: {str(e)}")

if __name__ == "__main__":
    # Keeps container running interactively for continuous transaction testing
    while True:
        get_user_prediction()
