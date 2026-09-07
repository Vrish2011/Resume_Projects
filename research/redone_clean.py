import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, AgglomerativeClustering
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split

columns = [
    "Age",
    "BMI",
    "How much water do you have in a day (in liters)",
    "Enter Sleeping hours",
    "Lifestyle (Exercise)",
    "Did you consume any other beverages today?",
    "Food Preference",

    
    
    "Rate you energy levels today",
    "How many times a day do you normally eat (include all solid foods i.e., breakfast, lunch, evening snack, dinner)",
    "Diabetes", "Hypertension","Obesity"
]

n_columns = [
    "num__Age",
    "num__BMI",
    "num__How much water do you have in a day (in liters)",
    "cat__Enter Sleeping hours",
    "cat__Lifestyle (Exercise)",
    

    
    "num__Rate you energy levels today",
    "num__How many times a day do you normally eat (include all solid foods i.e., breakfast, lunch, evening snack, dinner)",
    "cat__Diabetes", "cat__Hypertension","cat__Obesity","cat__Stress","cat__Chronic Disease"
]


excel = pd.read_excel("Indian_Diet.xlsx")
X_data = excel.dropna(subset=columns)[columns]
dict_diet = X_data.to_dict(orient="records")

def check_numercal(key_want):
   
    for row in dict_diet:
        for key, value in row.items():
            
            if key == key_want:
                
                if type(value) != int and type(value) != float and value != None:
                    return False
            
                
    return True

def convert_time_to_numbers(time):
    hour, minute, second = time.split(":")
    hour, minute, second = hour.lstrip("0"), minute.lstrip("0"), second.lstrip("0")
    hour_score = 0
    minute_score = 0
    second_score = 0
    if hour.strip():
        hour_score = int(hour) * 3600
    if minute.strip():
        minute_score = int(minute) * 60
    if second.strip():
        second_score = int(second)
    
    time_score = minute_score + hour_score + second_score
    return time_score




def normalize_dataset_column():
    for row in dict_diet:
        for key,value in row.items():
            if "Mention the time" in key:
                old = str(row[key])
                row[key] = convert_time_to_numbers(old)

            



normalize_dataset_column()
numerical_columns = []
categorical_columns = []
diseases = []

def run():
    for row in dict_diet:
        for key, value in row.items():
            if not key in numerical_columns and not key in categorical_columns:
                is_numerical = check_numercal(key)
                if is_numerical:
                    numerical_columns.append(key)
                elif not is_numerical:
                    categorical_columns.append(key)


run()

official_df = pd.DataFrame(dict_diet)

X__train, X__test = train_test_split(
    official_df,
    
    test_size=0.25,
    random_state=42
)

preprocessor = ColumnTransformer([
    ("num", StandardScaler(), numerical_columns),
    ("cat", OrdinalEncoder(), categorical_columns)
])

transformed_array = preprocessor.fit_transform(X__train)

transformed_dataset = pd.DataFrame(
    transformed_array,
    columns=preprocessor.get_feature_names_out(),
    index=X__train.index
)

print(transformed_dataset)


model = IsolationForest(
    contamination=0.05,
    random_state=42
)
results = model.fit_predict(transformed_dataset)

transformed_dataset["Anomaly"] = results

# Get every anomalous row
non_anomalous_values = X__train[transformed_dataset["Anomaly"] == 1][columns]
print(len(non_anomalous_values))
print(non_anomalous_values)


non_anomalous_values.to_excel(
    "new_cleaned_dataset.xlsx",
    index=False
)

pd.DataFrame(X__test,columns=non_anomalous_values.columns,
    ).to_excel("testing_data.xlsx")
