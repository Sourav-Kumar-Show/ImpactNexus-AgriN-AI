import os
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

def train_crop_model():
    # Update 'crop_recommendation.csv' to match your actual dataset filename
    data_path = os.path.join("data", "crop_recommendation.csv")
    
    if not os.path.exists(data_path):
        data_path = os.path.join("..", "data", "crop_recommendation.csv")

    print(f"Loading dataset from: {data_path}")
    df = pd.read_csv(data_path)
    
    # Drop accidental index column if it exists
    if "Unnamed: 0" in df.columns:
        df = df.drop("Unnamed: 0", axis=1)
        print("Dropped 'Unnamed: 0' column successfully.")
    
    # Define features and target (adjust column names if your dataset differs slightly)
    X = df[['N', 'P', 'K', 'temperature', 'pH', 'rainfall']]
    y = df['Crop']
    
    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize and train Gaussian Naive Bayes model
    print("Training Gaussian Naive Bayes model...")
    model = GaussianNB()
    model.fit(X_train, y_train)
    
    # Evaluate accuracy
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Model Training Complete! Accuracy: {acc * 100:.2f}%")
    
    # Save the trained model to ml/model.pkl
    model_output_path = os.path.join("ml", "model.pkl")
    if not os.path.exists("ml"):
        model_output_path = "model.pkl"
        
    with open(model_output_path, "wb") as f:
        pickle.dump(model, f)
        
    print(f"Model successfully saved to {model_output_path}")

if __name__ == "__main__":
    train_crop_model()
