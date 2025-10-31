app = Flask(__name__)
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    # Expected input: JSON with keys matching features (e.g., {"Warehouse_block": 0, "Mode_of_Shipment": 1, ...})
    input_df = pd.DataFrame([data])
    # Encode categoricals (using same encoder)
    for col in categorical_cols:
        if col in input_df:
            input_df[col] = le.transform(input_df[col])
    # Scale numericals
    input_df[numerical_cols] = scaler.transform(input_df[numerical_cols])
    # Predict
    prediction = best_rf.predict(input_df)[0]
    result = "On Time" if prediction == 1 else "Delayed"
    return jsonify({'prediction': result})
if __name__ == '__main__':
    app.run(debug=True)
