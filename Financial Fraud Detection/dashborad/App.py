import streamlit as st
import pandas as pd
import joblib

# Title
st.title("AI-Powered Financial Fraud Detection System")

# Load model
model = joblib.load('models/fraud_model.pkl')

# Upload CSV
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:

    data = pd.read_csv(uploaded_file)

    st.write("Uploaded Dataset")
    st.dataframe(data.head())

    # Remove target column if exists
    if 'Class' in data.columns:
        data = data.drop('Class', axis=1)

    # Predict
    predictions = model.predict(data)

    # Add predictions
    data['Prediction'] = predictions

    st.write("Prediction Results")
    st.dataframe(data.head())
#fraud count
    fraud_count = data['Prediction'].sum()

    st.write("Fraud Transactions:", fraud_count)
#fraud percentgae
    fraud_percentage = (fraud_count / len(data)) * 100

    st.write("Fraud Percentage:", round(fraud_percentage, 2), "%")

#show only fraud transacrion
    fraud_data = data[data['Prediction'] == 1]

    st.write("Detected Fraud Transactions")

    st.dataframe(fraud_data)
    #visualization
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    data['Prediction'].value_counts().plot(kind='bar', ax=ax)

    st.pyplot(fig)

    #sql analysis
    import sqlite3

    conn = sqlite3.connect('fraud_detection.db')

    data.to_sql('transactions', conn, if_exists='replace', index=False)

    query = '''
    SELECT Prediction, COUNT(*) as total
    FROM transactions
    GROUP BY Prediction
    '''

    result = pd.read_sql(query, conn)

    st.write(result)
