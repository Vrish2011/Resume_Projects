import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder, StandardScaler, OneHotEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, f1_score, make_scorer
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.multioutput import MultiOutputClassifier
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import ParameterGrid
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.base import clone
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression, RidgeClassifier, SGDClassifier
from sklearn.tree import DecisionTreeClassifier
columns = [
    "Mention the amount of time of physical activity",     
    "How many times a day do you normally eat (include all solid foods i.e., breakfast, lunch, evening snack, dinner)",     
    "Rate you energy levels today",     
    "Age",     
    "Diabetes",     
    "Hypertension",     
    "BMI",
    "How much water do you have in a day (in liters)",     
    "Gender"
    
  
    
    
]
training_data = pd.read_excel("new_cleaned_dataset.xlsx")
print(training_data)
testing_data = pd.read_excel("testing_data.xlsx")[columns]

input_columns = [
    "Mention the amount of time of physical activity",
    "How many times a day do you normally eat (include all solid foods i.e., breakfast, lunch, evening snack, dinner)",
    "Rate you energy levels today",
    "Age",
    "How much water do you have in a day (in liters)",
    
    "BMI",
    "Gender"
]

output_columns = [
    "Diabetes",
    "Hypertension"
]
dict_diet = training_data.to_dict(orient="records")
dict_test = testing_data.to_dict(orient="records")


parameter_grids = {

    "KNN": {
        "model__n_neighbors": [1, 3, 5, 7, 9, 11, 15, 21, 25],
        "model__weights": ["uniform", "distance"],
        "model__p": [1, 2]
    },


    "SVM": [
        {
            "model__estimator__kernel": ["linear"],
            "model__estimator__C": [0.1, 1, 10, 100]
        },

        {
            "model__estimator__kernel": ["rbf"],
            "model__estimator__C": [0.1, 1, 10, 100],
            "model__estimator__gamma": [
                "scale",
                "auto",
                0.01,
                0.1,
                1
            ]
        }
    ],


    "Random Forest": {
        "model__n_estimators": [100, 200, 300],
        "model__max_depth": [None, 5, 10, 20],
        "model__min_samples_split": [2, 5, 10],
        "model__min_samples_leaf": [1, 2, 4],
        "model__max_features": ["sqrt", "log2"]
    },


    "Naive Bayes": {
        "model__estimator__var_smoothing": [
            1e-12,
            1e-11,
            1e-10,
            1e-9,
            1e-8,
            1e-7,
            1e-6
        ]
    },


    "Logistic Regression": [
        {
            "model__estimator__solver": ["liblinear"],
            "model__estimator__penalty": ["l1", "l2"],
            "model__estimator__C": [0.01, 0.1, 1, 10, 100]
        },

        {
            "model__estimator__solver": ["lbfgs"],
            "model__estimator__penalty": ["l2"],
            "model__estimator__C": [0.01, 0.1, 1, 10, 100]
        }
    ],


    "Ridge Classifier": {
        "model__estimator__alpha": [
            0.001,
            0.01,
            0.1,
            1,
            10,
            100
        ],

        "model__estimator__fit_intercept": [
            True,
            False
        ],

        "model__estimator__solver": [
            "auto",
            "lsqr"
        ]
    },


    "Decision Tree": {
        "model__criterion": [
            "gini",
            "entropy",
            "log_loss"
        ],

        "model__max_depth": [
            None,
            3,
            5,
            10,
            20
        ],

        "model__min_samples_split": [
            2,
            5,
            10
        ],

        "model__min_samples_leaf": [
            1,
            2,
            5
        ]
    },


    "Extra Trees": {
        "model__n_estimators": [100, 200, 300],
        "model__max_depth": [None, 5, 10, 20],
        "model__min_samples_split": [2, 5, 10],
        "model__min_samples_leaf": [1, 2, 4],
        "model__max_features": ["sqrt", "log2"]
    },


    "Gradient Boosting": {
        "model__estimator__n_estimators": [
            50,
            100,
            200
        ],

        "model__estimator__learning_rate": [
            0.01,
            0.05,
            0.1
        ],

        "model__estimator__max_depth": [
            1,
            2,
            3
        ],

        "model__estimator__subsample": [
            0.8,
            1.0
        ]
    },


    "SGD Classifier": {
        "model__estimator__loss": [
            "log_loss",
            "modified_huber"
        ],

        "model__estimator__penalty": [
            "l1",
            "l2",
            "elasticnet"
        ],

        "model__estimator__alpha": [
            0.0001,
            0.001,
            0.01
        ]
    }
}


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
                
    

    for row in dict_test:
        for key, value in row.items():
            if "Mention the time" in key:
                if type(row[key]) != int:
                    old = row[key]
                    row[key] = convert_time_to_numbers(old)
                else:
                    pass
                
        

           


normalize_dataset_column()
numerical_columns = []
categorical_columns = []
bool_columns = [
    "Gender"
    
]

def run():
    for row in dict_diet:
        for key, value in row.items():
            if not key in numerical_columns and not key in categorical_columns:
                is_numerical = check_numercal(key)
                if is_numerical:
                    numerical_columns.append(key)
                
                



run()

official_dataset = pd.DataFrame(dict_diet)
print(numerical_columns)
preprocessor = ColumnTransformer([
    ("num", StandardScaler(), numerical_columns),
    ("cat", OrdinalEncoder(), categorical_columns),
    ("bool", OneHotEncoder(drop="if_binary", feature_name_combiner=lambda feature, category: feature), bool_columns)
])


X_train = official_dataset[input_columns]
Y_train = official_dataset[output_columns]
print(Y_train)


X_test = testing_data[["Mention the amount of time of physical activity",
    "How many times a day do you normally eat (include all solid foods i.e., breakfast, lunch, evening snack, dinner)",
    "Rate you energy levels today",
    "Age",
    "How much water do you have in a day (in liters)",
    "BMI",
    "Gender"]]

Y_test = testing_data[[
    "Diabetes",
    "Hypertension"
]].to_numpy()

def evaluate_model(best_params, pipeline):
    clone(pipeline).set_params(**best_params)
    pipeline.fit(X_train, Y_train)
    print(pipeline)
    predictions = np.array(pipeline.predict(X_test))
    overall_accuracy = accuracy_score(Y_test, predictions)
    diabetes_acc = accuracy_score(np.array(Y_test[:, 0]), predictions[:, 0])
    hypertension_acc = accuracy_score(np.array(Y_test[:, 1]), predictions[:, 1])
    overall_f1 = f1_score(Y_test, predictions, average="macro", zero_division=0)
    diabetes_f1 = f1_score(np.array(Y_test[:, 0]), predictions[:, 0], average="macro", zero_division=0)
    hypertension_f1 = f1_score(np.array(Y_test[:, 1]), predictions[:, 1], average="macro", zero_division=0)
    return overall_accuracy, diabetes_acc, hypertension_acc, overall_f1, diabetes_f1, hypertension_f1, best_params


def optimize_model(pipeline, parameters):
    best_f1 = -1
    best_params = None
    for parameter in ParameterGrid(parameters):
        
        current_pipeline = clone(pipeline).set_params(**parameter)
        
        
        current_pipeline.fit(X_train, Y_train)
        predictions = current_pipeline.predict(X_test)
        
        model_f1_score = f1_score(Y_test, predictions, average="macro", zero_division=0)
        if model_f1_score > best_f1:
            best_f1 = model_f1_score
            best_params = parameter.copy()
    

    return evaluate_model(best_params, clone(pipeline))
    


results = []
knn_pipeline = Pipeline([
    ("preprocessor", clone(preprocessor)),
    ("model", KNeighborsClassifier())
])


svm_pipeline = Pipeline([
    ("preprocessor", clone(preprocessor)),
    ("model", MultiOutputClassifier(
        SVC()
    ))
])


random_forest_pipeline = Pipeline([
    ("preprocessor", clone(preprocessor)),
    ("model", RandomForestClassifier(
        random_state=42,
        n_jobs=-1
    ))
])


naive_bayes_pipeline = Pipeline([
    ("preprocessor", clone(preprocessor)),
    ("model", MultiOutputClassifier(
        GaussianNB()
    ))
])


logistic_regression_pipeline = Pipeline([
    ("preprocessor", clone(preprocessor)),
    ("model", MultiOutputClassifier(
        LogisticRegression(
            max_iter=3000,
            class_weight="balanced",
            random_state=42
        )
    ))
])


ridge_pipeline = Pipeline([
    ("preprocessor", clone(preprocessor)),
    ("model", MultiOutputClassifier(
        RidgeClassifier(
            class_weight="balanced"
        )
    ))
])


decision_tree_pipeline = Pipeline([
    ("preprocessor", clone(preprocessor)),
    ("model", DecisionTreeClassifier(
        class_weight="balanced",
        random_state=42
    ))
])


extra_trees_pipeline = Pipeline([
    ("preprocessor", clone(preprocessor)),
    ("model", ExtraTreesClassifier(
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    ))
])


gradient_boosting_pipeline = Pipeline([
    ("preprocessor", clone(preprocessor)),
    ("model", MultiOutputClassifier(
        GradientBoostingClassifier(
            random_state=42
        )
    ))
])


sgd_pipeline = Pipeline([
    ("preprocessor", clone(preprocessor)),
    ("model", MultiOutputClassifier(
        SGDClassifier(
            max_iter=3000,
            class_weight="balanced",
            random_state=42
        )
    ))
])
models = {
    "KNN": knn_pipeline,
    "SVM": svm_pipeline,
    "Random Forest": random_forest_pipeline,
    "Naive Bayes": naive_bayes_pipeline,
    "Logistic Regression": logistic_regression_pipeline,
    "Ridge Classifier": ridge_pipeline,
    "Decision Tree": decision_tree_pipeline,
    "Extra Trees": extra_trees_pipeline,
    "Gradient Boosting": gradient_boosting_pipeline,
    "SGD Classifier": sgd_pipeline
}


for model_name, pipeline in models.items():

    (
        overall_accuracy,
        diabetes_acc,
        hypertension_acc,
        overall_f1,
        diabetes_f1,
        hypertension_f1,
        best_params

    ) = optimize_model(
        
        pipeline,
        parameter_grids[model_name]
    )


    results.append({
        "Model Name": model_name,
        "Overall Accuracy": overall_accuracy,
        "Diabetes Accuracy": diabetes_acc,
        "Hypertension Accuracy": hypertension_acc,
        "Overall F1": overall_f1,
        "Diabetes F1": diabetes_f1,
        "Hypertension F1": hypertension_f1,
        "Best Parameters": str(best_params)
    })


results_df = pd.DataFrame(results)

results_df.to_excel(
    "optimized_model_results.xlsx",
    index=False
)
        
cross_validation = KFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)


# ============================================================
# SCORING FUNCTIONS
# ============================================================

def overall_accuracy_score(y_true, y_pred):

    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)

    return accuracy_score(
        y_true,
        y_pred
    )


def diabetes_accuracy_score(y_true, y_pred):

    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)

    return accuracy_score(
        y_true[:, 0],
        y_pred[:, 0]
    )


def hypertension_accuracy_score(y_true, y_pred):

    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)

    return accuracy_score(
        y_true[:, 1],
        y_pred[:, 1]
    )


def overall_f1_score(y_true, y_pred):

    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)

    return f1_score(
        y_true,
        y_pred,
        average="macro",
        zero_division=0
    )


def diabetes_f1_score(y_true, y_pred):

    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)

    return f1_score(
        y_true[:, 0],
        y_pred[:, 0],
        zero_division=0
    )


def hypertension_f1_score(y_true, y_pred):

    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)

    return f1_score(
        y_true[:, 1],
        y_pred[:, 1],
        zero_division=0
    )


# ============================================================
# MAKE SCORERS
# ============================================================

scoring = {

    "overall_accuracy":
        make_scorer(overall_accuracy_score),

    "diabetes_accuracy":
        make_scorer(diabetes_accuracy_score),

    "hypertension_accuracy":
        make_scorer(hypertension_accuracy_score),

    "overall_f1":
        make_scorer(overall_f1_score),

    "diabetes_f1":
        make_scorer(diabetes_f1_score),

    "hypertension_f1":
        make_scorer(hypertension_f1_score)
}


# ============================================================
# STORE RESULTS
# ============================================================

cv_results = []

optimized_models = {}


# ============================================================
# CROSS-VALIDATE EVERY MODEL
# ============================================================

for model_name, pipeline in models.items():

    print("\nRunning:", model_name)


    grid_search = GridSearchCV(

        estimator=pipeline,

        param_grid=parameter_grids[model_name],

        scoring=scoring,

        # Choose hyperparameters using overall macro F1
        refit="overall_f1",

        cv=cross_validation,

        n_jobs=-1
    )


    # --------------------------------------------------------
    # HYPERPARAMETER TUNING + CROSS VALIDATION
    # --------------------------------------------------------

    grid_search.fit(
        X_train,
        Y_train
    )


    # --------------------------------------------------------
    # BEST MODEL / PARAMETERS
    # --------------------------------------------------------

    best_model = grid_search.best_estimator_

    best_params = grid_search.best_params_

    best_index = grid_search.best_index_


    # Save the optimized fitted model
    optimized_models[model_name] = best_model


    # --------------------------------------------------------
    # CROSS-VALIDATION RESULTS FOR WINNING PARAMETERS
    # --------------------------------------------------------

    cv_overall_accuracy = (
        grid_search.cv_results_[
            "mean_test_overall_accuracy"
        ][best_index]
    )

    cv_diabetes_accuracy = (
        grid_search.cv_results_[
            "mean_test_diabetes_accuracy"
        ][best_index]
    )

    cv_hypertension_accuracy = (
        grid_search.cv_results_[
            "mean_test_hypertension_accuracy"
        ][best_index]
    )

    cv_overall_f1 = (
        grid_search.cv_results_[
            "mean_test_overall_f1"
        ][best_index]
    )

    cv_diabetes_f1 = (
        grid_search.cv_results_[
            "mean_test_diabetes_f1"
        ][best_index]
    )

    cv_hypertension_f1 = (
        grid_search.cv_results_[
            "mean_test_hypertension_f1"
        ][best_index]
    )


    # --------------------------------------------------------
    # FINAL TEST SET
    # --------------------------------------------------------

    predictions = np.asarray(
        best_model.predict(X_test)
    )

    y_test_array = np.asarray(Y_test)


    test_overall_accuracy = accuracy_score(
        y_test_array,
        predictions
    )

    test_diabetes_accuracy = accuracy_score(
        y_test_array[:, 0],
        predictions[:, 0]
    )

    test_hypertension_accuracy = accuracy_score(
        y_test_array[:, 1],
        predictions[:, 1]
    )


    test_overall_f1 = f1_score(
        y_test_array,
        predictions,
        average="macro",
        zero_division=0
    )

    test_diabetes_f1 = f1_score(
        y_test_array[:, 0],
        predictions[:, 0],
        zero_division=0
    )

    test_hypertension_f1 = f1_score(
        y_test_array[:, 1],
        predictions[:, 1],
        zero_division=0
    )


    # --------------------------------------------------------
    # STORE RESULT
    # --------------------------------------------------------

    cv_results.append({

        "Model Name":
            model_name,

        "Best Parameters":
            str(best_params),

        "Mean CV Overall Accuracy":
            cv_overall_accuracy,

        "Mean CV Diabetes Accuracy":
            cv_diabetes_accuracy,

        "Mean CV Hypertension Accuracy":
            cv_hypertension_accuracy,

        "Mean CV Overall F1":
            cv_overall_f1,

        "Mean CV Diabetes F1":
            cv_diabetes_f1,

        "Mean CV Hypertension F1":
            cv_hypertension_f1,

        "Final Test Overall Accuracy":
            test_overall_accuracy,

        "Final Test Diabetes Accuracy":
            test_diabetes_accuracy,

        "Final Test Hypertension Accuracy":
            test_hypertension_accuracy,

        "Final Test Overall F1":
            test_overall_f1,

        "Final Test Diabetes F1":
            test_diabetes_f1,

        "Final Test Hypertension F1":
            test_hypertension_f1

    })


# ============================================================
# DATAFRAME
# ============================================================

cv_results_df = pd.DataFrame(
    cv_results
)


# ============================================================
# SAVE TO EXCEL
# ============================================================

cv_results_df.to_excel(
    "cross_validation_results.xlsx",
    index=False
)


print(cv_results_df)
print("\nSaved to cross_validation_results.xlsx")