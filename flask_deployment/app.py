from flask import Flask, request, render_template
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder

app = Flask(__name__)

# Load your model (ensure model.pkl is in flask_deployment)
model = joblib.load('model.pkl')

# Recreate preprocessors (match your notebook exactly)
scaler = StandardScaler()
# Fit scaler on dummy data or load if saved; for simplicity, assume you refit here with sample data
# Example: scaler.fit([[mean_values]]) – replace with your training data means if needed
le_warehouse = LabelEncoder()
le_warehouse.fit(['A', 'B', 'C', 'D', 'F'])  # From your notebook

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Extract form data (based on your notebook features)
    customer_care_calls = float(request.form['Customer_care_calls'])
    cost_of_product = float(request.form['Cost_of_the_Product'])
    prior_purchases = float(request.form['Prior_purchases'])
    product_importance = request.form['Product_importance']
    gender = request.form['Gender']
    discount_offered = float(request.form['Discount_offered'])
    weight_in_gms = float(request.form['Weight_in_gms'])
    warehouse_block = request.form['Warehouse_block']
    mode_of_shipment = request.form['Mode_of_Shipment']

    # Preprocess (replicate notebook: encoding, scaling)
    warehouse_encoded = le_warehouse.transform([warehouse_block])[0]
    # One-hot for product_importance (as in your notebook)
    prod_low = 1 if product_importance == 'low' else 0
    prod_medium = 1 if product_importance == 'medium' else 0
    prod_high = 1 if product_importance == 'high' else 0
    gender_encoded = 1 if gender == 'M' else 0  # Binary

    # Create input DataFrame (match your model's columns)
    input_data = pd.DataFrame({
        'Customer_care_calls': [customer_care_calls],
        'Cost_of_the_Product': [cost_of_product],
        'Prior_purchases': [prior_purchases],
        'Product_importance_low': [prod_low],
        'Product_importance_medium': [prod_medium],
        'Product_importance_high': [prod_high],
        'Gender': [gender_encoded],
        'Discount_offered': [discount_offered],
        'Weight_in_gms': [weight_in_gms],
        'Warehouse_block': [warehouse_encoded],
        # Add mode_of_shipment if used in model (e.g., one-hot or encoded)
    })

    # Scale numerical columns (as in notebook)
    numerical_cols = ['Customer_care_calls', 'Cost_of_the_Product', 'Prior_purchases', 'Discount_offered', 'Weight_in_gms']
    # Note: For accuracy, fit scaler on your original training data here or load a saved scaler
    input_data[numerical_cols] = scaler.fit_transform(input_data[numerical_cols])  # Temporary; use real fit if possible

    # Predict
    prediction = model.predict(input_data)[0]
    result = "Reached on Time" if prediction == 1 else "Delayed"  # Based on your target

    return render_template('index.html', prediction_text=f'Prediction: {result}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Codespaces-specific for public access