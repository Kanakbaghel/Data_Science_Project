import os
from flask import Flask, request, render_template
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Initialize Flask app and specify template and static folders
app = Flask(__name__, 
            template_folder='templates', 
            static_folder='static')

# Load the trained ML model
model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
model = joblib.load(model_path)

# Initialize LabelEncoders and other preprocessors (use your exact notebook logic)
le_warehouse = LabelEncoder()
le_warehouse.fit(['A', 'B', 'C', 'D', 'F'])  # Example categories

scaler = StandardScaler()
# NOTE: For real deployment, fit the scaler on training data and save it separately,
# Then load here. For demonstration, scaler is fit on dummy data
dummy_data = np.array([[0,0,0,0,0]])  # Adjust shape as needed
scaler.fit(dummy_data)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract input data from form
        data = request.form
        customer_care_calls = float(data['Customer_care_calls'])
        cost_of_product = float(data['Cost_of_the_Product'])
        prior_purchases = float(data['Prior_purchases'])
        product_importance = data['Product_importance']
        gender = data['Gender']
        discount_offered = float(data['Discount_offered'])
        weight_in_gms = float(data['Weight_in_gms'])
        warehouse_block = data['Warehouse_block']
        mode_of_shipment = data['Mode_of_Shipment']

        # Encode categorical variables
        warehouse_encoded = le_warehouse.transform([warehouse_block])[0]
        prod_low = 1 if product_importance == 'low' else 0
        prod_medium = 1 if product_importance == 'medium' else 0
        prod_high = 1 if product_importance == 'high' else 0
        gender_encoded = 1 if gender == 'M' else 0

        # Prepare DataFrame with inputs
        input_df = pd.DataFrame({
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
            # Add mode_of_shipment encoding here if applicable
        })

        # Scale numerical columns (replace with real scaler fit on training data)
        numerical_cols = ['Customer_care_calls', 'Cost_of_the_Product', 'Prior_purchases', 'Discount_offered', 'Weight_in_gms']
        input_df[numerical_cols] = scaler.transform(input_df[numerical_cols])

        # Predict using the loaded model
        prediction = model.predict(input_df)[0]
        result = "Reached on Time" if prediction == 1 else "Delayed"

        return render_template('index.html', prediction_text=f'Shipment Status: {result}')
    
    except Exception as e:
        # In case of error, return with error message
        return render_template('index.html', prediction_text=f'Error: {str(e)}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)