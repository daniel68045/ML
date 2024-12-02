from sklearn.linear_model import LinearRegression
import numpy as np


# LINEAR REGRESSION PRACTICE
# A model that predicts a student's score based on the number of hours they study
# Using the formula y = mx + b, the model calculates the best values for m and b, to predict
# scores based on the training data defined

# Example data: Hours studied vs. Exam scores
# Features (Hours studied)
X = np.array([[1], [2], [3], [4], [5]])  # Each sublist represents one input
# Labels (Scores achieved)
y = np.array([50, 55, 65, 70, 75])  # Corresponding scores

# Create and train the model
model = LinearRegression()
model.fit(X, y)

# Test the model with a new input
hours_studied = np.array([[6]])  # Predict for 6 hours of studying
predicted_score = model.predict(hours_studied)

print(f"Predicted score for studying {hours_studied[0][0]} hours: {predicted_score[0]:.2f}")
