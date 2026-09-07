import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, AgglomerativeClustering
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score




df = pd.read_excel("new_cleaned_dataset.xlsx")
dict_diet = df.to_dict(orient="records")

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
                if type(row[key]) != int:
                    old = row[key]
                    row[key] = convert_time_to_numbers(old)
                else:
                    pass
                

            



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

preprocessor = ColumnTransformer([
    ("num", StandardScaler(), numerical_columns),
    ("cat", OrdinalEncoder(), categorical_columns)
])

transformed_dataset = preprocessor.fit_transform(official_df)

pca = PCA(n_components=2)

X_pca = pca.fit_transform(transformed_dataset)

kmeans = KMeans(
    n_clusters=3,
    random_state=42
)

labels_kmeans = kmeans.fit_predict(X_pca)

agg = AgglomerativeClustering(
    n_clusters=3
)

labels_agg = agg.fit_predict(X_pca)

def optimize_clusters():
    best_cluster_kmeans = {"cluster" : 3, "score": 0}
    best_cluster_agg = {"cluster": 3, "score": 0}
    for i in range(2, 100):
        kmeans = KMeans(n_clusters=i, random_state=42)
        labels_kmeans = kmeans.fit_predict(X_pca)
        agg = AgglomerativeClustering(n_clusters=i)
        labels_agg = agg.fit_predict(X_pca)
        score_k = silhouette_score(X_pca, labels_kmeans)
        score_ag = silhouette_score(X_pca, labels_agg)
        print(score_k)
        print(score_ag)
        if float(score_k) > float(best_cluster_kmeans["score"]):
            best_cluster_kmeans["cluster"] = i
            best_cluster_kmeans["score"] = score_k
        if float(score_ag) > float(best_cluster_agg["score"]):
            best_cluster_agg["cluster"] = i
            best_cluster_agg["score"] = score_ag
        
    return best_cluster_agg, best_cluster_kmeans


best_agg, best_kmeans = optimize_clusters()

kmeans = KMeans(
    best_kmeans["cluster"],
    random_state=42
)

labels_kmeans = kmeans.fit_predict(X_pca)

agg = AgglomerativeClustering(
    best_agg["cluster"]
)

labels_agg = agg.fit_predict(X_pca)


plt.scatter(
    X_pca[:,0],
    X_pca[:,1],
    c=labels_kmeans
)
plt.xlabel("PCA_axis_1")
plt.ylabel("PCA_axis_2")
plt.title("Cluster Analysis using Kmeans")

plt.tight_layout()

plt.savefig("Cluster_analysis_Kmeans.png", dpi=300, bbox_inches="tight")

plt.show()

plt.close()

plt.scatter(
    X_pca[:,0],
    X_pca[:,1],
    c=labels_agg
)
plt.xlabel("PCA_axis_1")
plt.ylabel("PCA_axis_2")
plt.title("Cluster Analysis using Hierarchel Clustering")

plt.tight_layout()

plt.savefig("Cluster_analysis_hierarchel.png", dpi=300, bbox_inches="tight")

plt.show()

plt.close()
encoder = OrdinalEncoder()
transformed_dataset = encoder.fit_transform(official_df)
transformed_dataset = pd.DataFrame(
    transformed_dataset,
    columns=official_df.columns,
    index=official_df.index
)
analysis_columns = categorical_columns + ["Diabetes", "Hypertension", "Obesity"]
transformed_dataset["Cluster_kmeans"] = labels_kmeans
transformed_dataset["Cluster_agg"] = labels_agg
official_df["Cluster_kmeans"] = labels_kmeans
official_df["Cluster_agg"] = labels_agg
official_df.to_excel("clustered_dataset.xlsx")
cluster_means_kmeans = official_df.groupby("Cluster_kmeans").mean(numeric_only=True)
cluster_means_agg = official_df.groupby("Cluster_agg").mean(numeric_only=True)
cluster_means_kmeans.to_excel("Kmeans_analyzed_numeric.xlsx")
cluster_means_agg.to_excel("Agg_analyzed_numeric.xlsx")
cluster_means_kmeans_cat = transformed_dataset.groupby("Cluster_kmeans")[analysis_columns].mean()
cluster_means_agg_cat = transformed_dataset.groupby("Cluster_agg")[analysis_columns].mean()
cluster_means_kmeans_cat.to_excel("Kmeans_analyzed_categorical.xlsx")
cluster_means_agg_cat.to_excel("Agg_analyzed_cat.xlsx")