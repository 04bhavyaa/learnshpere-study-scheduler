import pandas as pd
import pickle
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Load datasets
df_mat = pd.read_csv("data/student-mat.csv", sep=";")
df_por = pd.read_csv("data/student-por.csv", sep=";")

# Merge datasets
merge_columns = ["school", "sex", "age", "address", "famsize", "Pstatus",
                 "Medu", "Fedu", "Mjob", "Fjob", "reason", "nursery", "internet"]
df = pd.merge(df_mat, df_por, on=merge_columns, suffixes=('_mat', '_por'))

# Numerical columns to average
numerical_cols = ["age", "Medu", "Fedu", "traveltime", "studytime", "failures", "famrel", 
                  "freetime", "goout", "Dalc", "Walc", "health", "absences", "G1", "G2", "G3"]

# Averaging numerical values
for col in numerical_cols:
    if f"{col}_mat" in df.columns and f"{col}_por" in df.columns:
        df[col] = (df[f"{col}_mat"] + df[f"{col}_por"]) / 2
        df[col] = df[col].round(1)  # Keep one decimal

# Keeping categorical `_mat` versions
categorical_cols = [col[:-4] for col in df.columns if col.endswith("_mat")]
for col in categorical_cols:
    df[col] = df[f"{col}_mat"]

# Drop old columns
df.drop(columns=[col for col in df.columns if col.endswith("_mat") or col.endswith("_por")], inplace=True)

# Rename columns
column_mappings = {
    "sex": "Gender",
    "Mjob": "Mother Job",
    "Fjob": "Father Job",
    "studytime": "Study Time",
    "schoolsup": "School Support",
    "famsup": "Family Support",
    "paid": "Extra Paid Class", 
    "internet": "Internet Access",
    "freetime": "Free Time",
    "absences": "Absences",
    "G3": "Final Grade",
    "activities": "Extracurricular",
    "higher": "Higher Education",
    "romantic": "Romantic Relationship",
    "G1": "Previous Grade 1",
    "G2": "Previous Grade 2"
}
df.rename(columns=column_mappings, inplace=True)

# Drop unnecessary columns
df.drop(columns=['school', 'address', 'famsize', 'reason', 'guardian', 'nursery', 'famrel', 
                 'Dalc', 'Walc', 'health', 'age', 'goout', 'failures'], inplace=True)

# Preprocessing
column_names = ["Gender", "Mother Job", "Father Job", "Previous Grade 1", "Previous Grade 2", "Study Time", "Absences", "School Support", 
                "Family Support","Extra Paid Class", "Extracurricular", "Internet Access", "Higher Education", "Romantic Relationship", "Subjects"]

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), df[column_names].select_dtypes(include=['int64', 'float64']).columns.tolist()),
        ('cat', OneHotEncoder(handle_unknown="ignore"), df[column_names].select_dtypes(include=['object']).columns.tolist())
    ]
)

preprocessor.fit(df[column_names])

# Save the preprocessor
with open("artifacts/preprocess.pkl", "wb") as f:
    pickle.dump(preprocessor, f)

# Transform & Save Processed Data
df_transformed = preprocessor.transform(df[column_names])
pd.DataFrame(df_transformed).to_csv("data/student-merged.csv", index=False)

print("Preprocessing pipeline saved successfully!")
print("Preprocessed data saved successfully!")
