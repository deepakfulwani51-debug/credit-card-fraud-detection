import pandas as pd
import joblib
import sys
import select

# Load the pre-trained model brains instantly
model = joblib.load("fraud_model.pkl")
template_row = joblib.load("input_template.pkl")

print("\n--- Live Transaction Checker App Booted ---")

def get_user_prediction():
    while select.select([sys.stdin], [], [], 0.0)[0]:
        sys.stdin.read(1)
        
    print("\nPlease enter transaction details for analysis:")
    
    while True:
        try:
            amount_input = input("Enter Transaction Amount: ").strip()
            if not amount_input: continue
            amount = float(amount_input)
            break
        except ValueError:
            print("❌ Invalid input. Numbers only.")
            
    while True:
        try:
            time_input = input("Enter Time (seconds elapsed): ").strip()
            if not time_input: continue
            time = float(time_input)
            break
        except ValueError:
            print("❌ Invalid input. Numbers only.")
    
    # Rebuild input dataframe using the template column headers
    custom_input = template_row.copy()
    custom_input['Amount'] = amount
    custom_input['Time'] = time
    
    final_input = pd.DataFrame([custom_input])
    
    prediction = model.predict(final_input)[0]
    probability = model.predict_proba(final_input)[0][1]
    
    print("\n--- ANALYSIS RESULT ---")
    if prediction == 1:
        print(f"⚠️ ALERT: High Risk! Potential Fraud Detected. (Confidence: {probability*100:.2f}%)")
    else:
        print(f"✅ Safe: Normal Transaction. (Fraud Probability: {probability*100:.2f}%)")

if __name__ == "__main__":
    get_user_prediction()
