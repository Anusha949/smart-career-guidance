import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
import pickle

# Load dataset
df = pd.read_csv("data set\smart_career_guidance_dataset_v3.csv")

# Preprocess Skills
df['Skills'] = df['Skills'].apply(lambda x: x.split(", "))

# One-hot encode skills
mlb = MultiLabelBinarizer()
skills_encoded = mlb.fit_transform(df['Skills'])
skills_df = pd.DataFrame(skills_encoded, columns=mlb.classes_)

# Encode Interests and Career
le_interests = LabelEncoder()
df['Interests'] = le_interests.fit_transform(df['Interests'])

le_career = LabelEncoder()
df['Recommended_Career'] = le_career.fit_transform(df['Recommended_Career'])

# Combine features
X = pd.concat([df[['10th_score', '12th_score', 'UG_score', 'Interests']], skills_df], axis=1)
y = df['Recommended_Career']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train the model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model and encoders
with open("model/model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("model/le_interests.pkl", "wb") as f:
    pickle.dump(le_interests, f)

with open("model/le_career.pkl", "wb") as f:
    pickle.dump(le_career, f)

with open("model/mlb_skills.pkl", "wb") as f:
    pickle.dump(mlb, f)

print("✅ Model trained and saved successfully!")