import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# Load the dataset
print("Loading dataset...")
data = pd.read_csv('dataset/upi_transactions.csv')
# Preprocess the data
print("Preprocessing data...")
# Convert categorical variables to numerical
le_risk = LabelEncoder()
le_result = LabelEncoder()

data['risk_level_encoded'] = le_risk.fit_transform(data['risk_level'])
data['result_encoded'] = le_result.fit_transform(data['result'])

# Define features and target
X = data[['amount', 'risk_level_encoded']]
y = data['result_encoded']

# Split the data
print("Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
print("Training Random Forest model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
print("Making predictions...")
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=le_result.classes_))

# Save the model and encoders
print("Saving model and encoders...")
joblib.dump(model, 'fraud_detection_model.pkl')
joblib.dump(le_risk, 'label_encoder_risk.pkl')
joblib.dump(le_result, 'label_encoder_result.pkl')
print("Model training completed!")
print("Files saved:")
print("- fraud_detection_model.pkl")
print("- label_encoder_risk.pkl")
print("- label_encoder_result.pkl")