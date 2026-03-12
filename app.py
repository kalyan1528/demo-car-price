from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

# Load model
model = joblib.load("models.pkl")

@app.route('/', methods=['GET'])
def Home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        Present_Price        = float(request.form['Present_Price'])
        Kms_Driven           = int(request.form['Kms_Driven'])
        Owner                = int(request.form['Owner'])
        Age                  = int(request.form['Age'])

        Fuel_Type            = request.form['Fuel_Type']
        Fuel_Type_Petrol     = 1 if Fuel_Type == 'Petrol' else 0
        Fuel_Type_Diesel     = 1 if Fuel_Type == 'Diesel' else 0

        Seller_Type          = request.form['Seller_Type']
        Seller_Type_Individual = 1 if Seller_Type == 'Individual' else 0

        Transmission         = request.form['Transmission']
        Transmission_Manual  = 1 if Transmission == 'Manual' else 0

        prediction = model.predict([[
            Present_Price, Kms_Driven, Owner, Age,
            Fuel_Type_Diesel, Fuel_Type_Petrol,
            Seller_Type_Individual, Transmission_Manual
        ]])

        output = round(prediction[0], 2)

        if output < 0:
            # ✅ No <h2> tags — template handles styling
            return render_template('result.html',
                prediction_text="Sorry you cannot sell this car")
        else:
            return render_template('result.html',
                prediction_text="You can sell the car at {} Lacs".format(output))

    return render_template('index.html')


if __name__ == "__main__":
    import webbrowser
    import threading
    
    # Open browser after a delay to ensure server is ready
    def open_browser():
        import time
        time.sleep(2)
        webbrowser.open("http://localhost:5000")
    
    threading.Thread(target=open_browser, daemon=True).start()
    app.run(debug=True)
