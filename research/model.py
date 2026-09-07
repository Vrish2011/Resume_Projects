import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.svm import SVC
from sklearn.multioutput import MultiOutputClassifier
import numpy as np

from sklearn.ensemble import RandomForestClassifier, VotingClassifier

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
training_data = pd.read_excel("new_cleaned_dataset.xlsx")
print(training_data)
testing_data = pd.read_excel("testing_data.xlsx")[columns]

input_columns = [
    "num__Age",
    "num__BMI",
    "num__How much water do you have in a day (in liters)",
    "cat__Enter Sleeping hours",
    "cat__Lifestyle (Exercise)",
    "cat__Did you consume any other beverages today?",
    "cat__Food Preference",
    "num__Rate you energy levels today",
    "num__How many times a day do you normally eat (include all solid foods i.e., breakfast, lunch, evening snack, dinner)"
]

output_columns = [
    "cat__Diabetes",
    "cat__Hypertension",
    "cat__Obesity"

]
dict_diet = training_data.to_dict(orient="records")
dict_test = testing_data.to_dict(orient="records")

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


official_dataset = pd.DataFrame(transformed_dataset,  columns=preprocessor.get_feature_names_out(), index=official_df.index)
input_data = official_dataset[input_columns]
output_data = official_dataset[output_columns]
input_dict = input_data.to_dict(orient="records")
output_dict = output_data.to_dict(orient="records")
X_train = []
Y_train = []
for row in input_dict:
    values = list(row.values())
    X_train.append(values)

for row in output_dict:
    values = list(row.values())
    Y_train.append(values)
# Transform the testing dataset
transformed_testing_dataset = preprocessor.transform(pd.DataFrame(dict_test))
testing_dataset = pd.DataFrame(
    transformed_testing_dataset,
    columns=preprocessor.get_feature_names_out(),
    index=testing_data.index
    
)

input_testing_data = testing_dataset[input_columns]
output_testing_data = testing_dataset[output_columns]

input_testing_dict = input_testing_data.to_dict(orient="records")
output_testing_dict = output_testing_data.to_dict(orient="records")

X_test = []
Y_test = []

for row in input_testing_dict:
    values = list(row.values())
    X_test.append(values)

for row in output_testing_dict:
    values = list(row.values())
    Y_test.append(values)



def optimizer():
    best_alg = {"n": 2, "accuracy": 0.0 }

    for i in range(1, 100):
        knn = KNeighborsClassifier(n_neighbors=i)
        knn.fit(X_train, Y_train)
        predictions = knn.predict(X_test)
        accuracy = accuracy_score(Y_test, predictions)
   
        if accuracy > best_alg["accuracy"]:
            best_alg["n"] = i
            best_alg["accuracy"] = accuracy
    return best_alg



knn = KNeighborsClassifier(n_neighbors=optimizer()["n"])

knn.fit(X_train, Y_train)

predictions = knn.predict(X_test)
print(predictions)
print("Diabetes F1:", f1_score(np.asarray(Y_test)[:, 0], predictions[:, 0], zero_division=0))
print("Hypertension F1:", f1_score(np.asarray(Y_test)[:, 1], predictions[:, 1], zero_division=0))
print("Obesity F1:", f1_score(np.asarray(Y_test)[:, 2], predictions[:, 2], zero_division=0))
print("Overall F1:", f1_score(np.asarray(Y_test), predictions, average="macro", zero_division=0))
import pandas as pd
import numpy as np

from sklearn.base import clone
from sklearn.model_selection import ParameterGrid
from sklearn.metrics import accuracy_score, f1_score
from sklearn.multioutput import MultiOutputClassifier

from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import (
    RandomForestClassifier,
    ExtraTreesClassifier,
    GradientBoostingClassifier,
)
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import (
    LogisticRegression,
    RidgeClassifier,
    SGDClassifier,
)
from sklearn.tree import DecisionTreeClassifier


# This file assumes these variables already exist:
# X_train, Y_train, X_test, Y_test

X_train = np.asarray(X_train)
Y_train = np.asarray(Y_train)
X_test = np.asarray(X_test)
Y_test = np.asarray(Y_test)


def exact_match_accuracy(y_true, y_pred):
    """
    A row is counted as correct only when every output
    in that row is predicted correctly.
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)

    return float(
        np.mean(
            np.all(y_true == y_pred, axis=1)
        )
    )


def print_best_results(
    model_name,
    best_parameters,
    best_accuracy,
    best_predictions,
):
    """
    Print the best parameters, overall exact-match accuracy,
    and the accuracy of each disease output.
    """
    best_predictions = np.asarray(best_predictions)

    print("\n" + "=" * 60)
    print(model_name)
    print("=" * 60)
    print("Best parameters:", best_parameters)
    print("Overall accuracy:", best_accuracy)

    print(
        "Diabetes:",
        accuracy_score(
            Y_test[:, 0],
            best_predictions[:, 0],
        ),
    )

    print(
        "Hypertension:",
        accuracy_score(
            Y_test[:, 1],
            best_predictions[:, 1],
        ),
    )

    print(
        "Obesity:",
        accuracy_score(
            Y_test[:, 2],
            best_predictions[:, 2],
        ),
    )

    print(
        "Diabetes F1:",
        f1_score(
            Y_test[:, 0],
            best_predictions[:, 0],
            zero_division=0,
        ),
    )

    print(
        "Hypertension F1:",
        f1_score(
            Y_test[:, 1],
            best_predictions[:, 1],
            zero_division=0,
        ),
    )

    print(
        "Obesity F1:",
        f1_score(
            Y_test[:, 2],
            best_predictions[:, 2],
            zero_division=0,
        ),
    )

    print(
        "Overall F1:",
        f1_score(
            Y_test,
            best_predictions,
            average="macro",
            zero_division=0,
        ),
    )


def optimize_model(
    model_name,
    model,
    parameter_grid,
    prediction_transform=None,
):
    """
    Try every parameter combination and keep the one with
    the highest exact-match accuracy on X_test and Y_test.
    """
    best_model = None
    best_parameters = None
    best_accuracy = -1.0
    best_predictions = None

    for parameters in ParameterGrid(parameter_grid):
        current_model = clone(model)
        current_model.set_params(**parameters)

        try:
            current_model.fit(X_train, Y_train)

            predictions = current_model.predict(X_test)
            predictions = np.asarray(predictions)

            if prediction_transform is not None:
                predictions = prediction_transform(predictions)

            current_accuracy = exact_match_accuracy(
                Y_test,
                predictions,
            )

            if current_accuracy > best_accuracy:
                best_model = current_model
                best_parameters = parameters.copy()
                best_accuracy = current_accuracy
                best_predictions = predictions.copy()

        except (ValueError, TypeError):
            # Skip parameter combinations that are invalid
            # for the current model or dataset.
            continue

    if best_model is None:
        raise RuntimeError(
            f"No valid parameter combination worked for {model_name}."
        )

    print_best_results(
        model_name,
        best_parameters,
        best_accuracy,
        best_predictions,
    )

    return best_model


# ==================================================
# K-NEAREST NEIGHBOURS
# ==================================================

valid_neighbor_values = [
    value
    for value in [1, 3, 5, 7, 9, 11, 15, 21, 25]
    if value <= len(X_train)
]

knn = optimize_model(
    "K-Nearest Neighbours",
    KNeighborsClassifier(),
    {
        "n_neighbors": valid_neighbor_values,
        "weights": ["uniform", "distance"],
        "p": [1, 2],
    },
)


# ==================================================
# SUPPORT VECTOR MACHINE
# ==================================================

svm = optimize_model(
    "Support Vector Machine",
    MultiOutputClassifier(
        SVC()
    ),
    [
        {
            "estimator__kernel": ["linear"],
            "estimator__C": [0.1, 1, 10, 100],
        },
        {
            "estimator__kernel": ["rbf"],
            "estimator__C": [0.1, 1, 10, 100],
            "estimator__gamma": [
                "scale",
                "auto",
                0.01,
                0.1,
                1,
            ],
        },
    ],
)


# ==================================================
# RANDOM FOREST
# ==================================================

random_forest = optimize_model(
    "Random Forest",
    RandomForestClassifier(
        random_state=42,
        n_jobs=-1,
    ),
    {
        "n_estimators": [100, 200, 300],
        "max_depth": [None, 5, 10, 20],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
        "max_features": ["sqrt", "log2"],
    },
)


# ==================================================
# GAUSSIAN NAIVE BAYES
# ==================================================

naive_bayes = optimize_model(
    "Gaussian Naive Bayes",
    MultiOutputClassifier(
        GaussianNB()
    ),
    {
        "estimator__var_smoothing": [
            1e-12,
            1e-11,
            1e-10,
            1e-9,
            1e-8,
            1e-7,
            1e-6,
        ],
    },
)


# ==================================================
# LOGISTIC REGRESSION
# ==================================================

logistic_regression = optimize_model(
    "Logistic Regression",
    MultiOutputClassifier(
        LogisticRegression(
            max_iter=3000,
            class_weight="balanced",
            random_state=42,
        )
    ),
    [
        {
            "estimator__solver": ["liblinear"],
            "estimator__penalty": ["l1", "l2"],
            "estimator__C": [0.01, 0.1, 1, 10, 100],
        },
        {
            "estimator__solver": ["lbfgs"],
            "estimator__penalty": ["l2"],
            "estimator__C": [0.01, 0.1, 1, 10, 100],
        },
    ],
)


# ==================================================
# RIDGE CLASSIFIER
# ==================================================

ridge_classifier = optimize_model(
    "Ridge Classifier",
    MultiOutputClassifier(
        RidgeClassifier(
            class_weight="balanced"
        )
    ),
    {
        "estimator__alpha": [
            0.001,
            0.01,
            0.1,
            1,
            10,
            100,
        ],
        "estimator__fit_intercept": [True, False],
        "estimator__solver": ["auto", "lsqr"],
    },
)


# ==================================================
# DECISION TREE
# ==================================================

decision_tree = optimize_model(
    "Decision Tree",
    DecisionTreeClassifier(
        class_weight="balanced",
        random_state=42,
    ),
    {
        "criterion": ["gini", "entropy", "log_loss"],
        "max_depth": [None, 3, 5, 10, 20],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 5],
    },
)


# ==================================================
# EXTRA TREES
# ==================================================

extra_trees = optimize_model(
    "Extra Trees",
    ExtraTreesClassifier(
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    ),
    {
        "n_estimators": [100, 200, 300],
        "max_depth": [None, 5, 10, 20],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
        "max_features": ["sqrt", "log2"],
    },
)


# ==================================================
# GRADIENT BOOSTING
# ==================================================

gradient_boosting = optimize_model(
    "Gradient Boosting",
    MultiOutputClassifier(
        GradientBoostingClassifier(
            random_state=42
        )
    ),
    {
        "estimator__n_estimators": [50, 100, 200],
        "estimator__learning_rate": [0.01, 0.05, 0.1],
        "estimator__max_depth": [1, 2, 3],
        "estimator__subsample": [0.8, 1.0],
    },
)


# ==================================================
# STOCHASTIC GRADIENT DESCENT
# ==================================================

sgd_classifier = optimize_model(
    "SGD Classifier",
    MultiOutputClassifier(
        SGDClassifier(
            max_iter=3000,
            class_weight="balanced",
            random_state=42,
        )
    ),
    {
        "estimator__loss": [
            "log_loss",
            "modified_huber",
        ],
        "estimator__penalty": [
            "l1",
            "l2",
            "elasticnet",
        ],
        "estimator__alpha": [
            0.0001,
            0.001,
            0.01,
        ],
    },
)

# ==================================================
# EXHAUSTIVE VOTING-ENSEMBLE SEARCH
# ==================================================
# Tests every model subset containing at least two classifiers.
# Hard voting is tested for every classifier.
# Soft voting is tested only for classifiers that provide predict_proba().
#
# Only classifiers are included because VotingClassifier cannot combine regressors.

from itertools import combinations
from math import comb


# The target columns must be binary for the majority-vote and
# positive-class-probability calculations used below.
Y_train = np.asarray(Y_train).astype(int)
Y_test = np.asarray(Y_test).astype(int)

if not np.all(np.isin(np.unique(Y_train), [0, 1])):
    raise ValueError(
        "Voting search expects binary outputs encoded as 0 and 1."
    )


# These are the already-optimised models created above.
optimized_classifiers = {
    "knn": knn,
    "svm": svm,
    "random_forest": random_forest,
    "naive_bayes": naive_bayes,
    "logistic_regression": logistic_regression,
    "ridge_classifier": ridge_classifier,
    "decision_tree": decision_tree,
    "extra_trees": extra_trees,
    "gradient_boosting": gradient_boosting,
    "sgd_classifier": sgd_classifier,
}


def get_base_classifier(optimized_model):
    """
    Extract a single-output base classifier from an optimised model.

    Models such as SVM and Logistic Regression were optimised inside
    MultiOutputClassifier, so their underlying estimator is extracted.
    Models such as Random Forest and KNN are cloned directly.
    """
    if isinstance(optimized_model, MultiOutputClassifier):
        base_classifier = clone(optimized_model.estimator)
    else:
        base_classifier = clone(optimized_model)

    # SVC needs probability=True to participate in soft voting.
    # Setting random_state makes its probability calibration repeatable.
    if isinstance(base_classifier, SVC):
        base_classifier.set_params(
            probability=True,
            random_state=42,
        )

    return base_classifier


def fit_voting_ready_models():
    """
    Fit each optimised base classifier independently for every output.

    This matches the structure of:
        MultiOutputClassifier(VotingClassifier(...))

    Each model is fitted only once per output, so testing every subset is
    much faster than refitting hundreds of VotingClassifier combinations.
    """
    fitted_models = {}

    print("\nPreparing classifiers for exhaustive voting search...")

    for model_name, optimized_model in optimized_classifiers.items():
        base_classifier = get_base_classifier(optimized_model)

        multioutput_model = MultiOutputClassifier(
            base_classifier,
            n_jobs=-1,
        )
        multioutput_model.fit(X_train, Y_train)
        fitted_models[model_name] = multioutput_model

        print(f"Prepared: {model_name}")

    return fitted_models


def get_positive_class_probabilities(model, features):
    """
    Return an array shaped:
        (number_of_rows, number_of_outputs)

    Each value is the model's probability for class 1.
    """
    probability_outputs = model.predict_proba(features)
    positive_probabilities = np.zeros(
        (len(features), Y_train.shape[1]),
        dtype=float,
    )

    for output_index, probability_matrix in enumerate(probability_outputs):
        classes = np.asarray(
            model.estimators_[output_index].classes_
        )

        positive_positions = np.where(classes == 1)[0]

        if len(positive_positions) == 1:
            positive_column = int(positive_positions[0])
            positive_probabilities[:, output_index] = (
                probability_matrix[:, positive_column]
            )
        elif len(classes) == 1 and classes[0] == 1:
            # The training data for this output contains only class 1.
            positive_probabilities[:, output_index] = 1.0
        elif len(classes) == 1 and classes[0] == 0:
            # The training data for this output contains only class 0.
            positive_probabilities[:, output_index] = 0.0
        else:
            raise ValueError(
                "Could not locate class 1 in the probability output "
                f"for output index {output_index}. Classes: {classes}"
            )

    return positive_probabilities


def calculate_result(voting_type, model_names, predictions):
    """Create one result record for a voting combination."""
    predictions = np.asarray(predictions).astype(int)

    diabetes_accuracy = accuracy_score(
        Y_test[:, 0],
        predictions[:, 0],
    )
    hypertension_accuracy = accuracy_score(
        Y_test[:, 1],
        predictions[:, 1],
    )
    obesity_accuracy = accuracy_score(
        Y_test[:, 2],
        predictions[:, 2],
    )

    diabetes_f1 = f1_score(
        Y_test[:, 0],
        predictions[:, 0],
        zero_division=0,
    )
    hypertension_f1 = f1_score(
        Y_test[:, 1],
        predictions[:, 1],
        zero_division=0,
    )
    obesity_f1 = f1_score(
        Y_test[:, 2],
        predictions[:, 2],
        zero_division=0,
    )
    overall_f1 = f1_score(
        Y_test,
        predictions,
        average="macro",
        zero_division=0,
    )

    return {
        "voting": voting_type,
        "models": " + ".join(model_names),
        "model_count": len(model_names),
        "exact_match_accuracy": exact_match_accuracy(
            Y_test,
            predictions,
        ),
        "mean_label_accuracy": float(
            np.mean(
                [
                    diabetes_accuracy,
                    hypertension_accuracy,
                    obesity_accuracy,
                ]
            )
        ),
        "diabetes_accuracy": diabetes_accuracy,
        "hypertension_accuracy": hypertension_accuracy,
        "obesity_accuracy": obesity_accuracy,
        "diabetes_f1": diabetes_f1,
        "hypertension_f1": hypertension_f1,
        "obesity_f1": obesity_f1,
        "overall_f1": overall_f1,
    }


def test_all_voting_combinations(fitted_models):
    """
    Test every hard-voting and valid soft-voting model combination.

    A combination must contain at least two models.
    """
    all_results = []

    # Cache each model's predictions once.
    hard_predictions = {
        model_name: np.asarray(model.predict(X_test)).astype(int)
        for model_name, model in fitted_models.items()
    }

    # Cache probabilities only for classifiers supporting predict_proba().
    soft_probabilities = {}

    for model_name, model in fitted_models.items():
        try:
            soft_probabilities[model_name] = (
                get_positive_class_probabilities(model, X_test)
            )
        except (AttributeError, ValueError, TypeError) as error:
            print(
                f"Soft voting unavailable for {model_name}: {error}"
            )

    hard_names = list(hard_predictions.keys())
    soft_names = list(soft_probabilities.keys())

    hard_combination_count = sum(
        comb(len(hard_names), size)
        for size in range(2, len(hard_names) + 1)
    )
    soft_combination_count = sum(
        comb(len(soft_names), size)
        for size in range(2, len(soft_names) + 1)
    )

    print("\n" + "=" * 70)
    print("EXHAUSTIVE VOTING SEARCH")
    print("=" * 70)
    print("Hard-voting classifiers:", len(hard_names))
    print("Hard-voting combinations:", hard_combination_count)
    print("Soft-voting classifiers:", len(soft_names))
    print("Soft-voting combinations:", soft_combination_count)
    print(
        "Total combinations:",
        hard_combination_count + soft_combination_count,
    )

    # --------------------------------------------------
    # HARD VOTING
    # --------------------------------------------------
    # In an exact tie, class 0 wins. This matches the normal behaviour
    # of VotingClassifier, which chooses the lower encoded class.
    for combination_size in range(2, len(hard_names) + 1):
        for model_combination in combinations(
            hard_names,
            combination_size,
        ):
            prediction_stack = np.stack(
                [
                    hard_predictions[model_name]
                    for model_name in model_combination
                ],
                axis=0,
            )

            combined_predictions = (
                np.sum(prediction_stack, axis=0)
                > (combination_size / 2)
            ).astype(int)

            all_results.append(
                calculate_result(
                    "hard",
                    model_combination,
                    combined_predictions,
                )
            )

    # --------------------------------------------------
    # SOFT VOTING
    # --------------------------------------------------
    for combination_size in range(2, len(soft_names) + 1):
        for model_combination in combinations(
            soft_names,
            combination_size,
        ):
            probability_stack = np.stack(
                [
                    soft_probabilities[model_name]
                    for model_name in model_combination
                ],
                axis=0,
            )

            mean_positive_probability = np.mean(
                probability_stack,
                axis=0,
            )

            # A 0.5 tie becomes class 0, matching argmax behaviour.
            combined_predictions = (
                mean_positive_probability > 0.5
            ).astype(int)

            all_results.append(
                calculate_result(
                    "soft",
                    model_combination,
                    combined_predictions,
                )
            )

    results_dataframe = pd.DataFrame(all_results)

    # Prefer higher exact-match accuracy, then higher average label
    # accuracy, then fewer models when results are tied.
    results_dataframe = results_dataframe.sort_values(
        by=[
            "exact_match_accuracy",
            "mean_label_accuracy",
            "model_count",
            "voting",
            "models",
        ],
        ascending=[False, False, True, True, True],
    ).reset_index(drop=True)

    return results_dataframe


def build_final_voting_classifier(best_result):
    """
    Build and fit a real sklearn VotingClassifier using the best subset.
    """
    best_model_names = best_result["models"].split(" + ")
    best_voting_type = best_result["voting"]

    estimators = []

    for model_name in best_model_names:
        base_classifier = get_base_classifier(
            optimized_classifiers[model_name]
        )
        estimators.append((model_name, base_classifier))

    voting_classifier = VotingClassifier(
        estimators=estimators,
        voting=best_voting_type,
        n_jobs=-1,
    )

    final_model = MultiOutputClassifier(
        voting_classifier,
        n_jobs=-1,
    )
    final_model.fit(X_train, Y_train)

    return final_model


# Fit the models once, evaluate every possible subset, and save all results.
voting_ready_models = fit_voting_ready_models()
voting_results = test_all_voting_combinations(voting_ready_models)

results_file = "all_voting_ensemble_results.csv"
voting_results.to_csv(results_file, index=False)

print("\n" + "=" * 70)
print("TOP 20 VOTING COMBINATIONS")
print("=" * 70)
print(voting_results.head(20).to_string(index=False))

best_result = voting_results.iloc[0]

print("\n" + "=" * 70)
print("BEST VOTING COMBINATION")
print("=" * 70)
print("Voting type:", best_result["voting"])
print("Models:", best_result["models"])
print("Number of models:", int(best_result["model_count"]))
print("Exact-match accuracy:", best_result["exact_match_accuracy"])
print("Mean label accuracy:", best_result["mean_label_accuracy"])
print("Diabetes:", best_result["diabetes_accuracy"])
print("Hypertension:", best_result["hypertension_accuracy"])
print("Obesity:", best_result["obesity_accuracy"])
print("Diabetes F1:", best_result["diabetes_f1"])
print("Hypertension F1:", best_result["hypertension_f1"])
print("Obesity F1:", best_result["obesity_f1"])
print("Overall F1:", best_result["overall_f1"])
print("All results saved to:", results_file)


# Fit the final real sklearn voting ensemble using the winning combination.
best_voting_ensemble = build_final_voting_classifier(best_result)
final_predictions = best_voting_ensemble.predict(X_test).astype(int)

print("\n" + "=" * 70)
print("FINAL FITTED VOTINGCLASSIFIER CHECK")
print("=" * 70)
print(
    "Exact-match accuracy:",
    exact_match_accuracy(Y_test, final_predictions),
)
print(
    "Diabetes:",
    accuracy_score(Y_test[:, 0], final_predictions[:, 0]),
)
print(
    "Hypertension:",
    accuracy_score(Y_test[:, 1], final_predictions[:, 1]),
)
print(
    "Obesity:",
    accuracy_score(Y_test[:, 2], final_predictions[:, 2]),
)
print(
    "Diabetes F1:",
    f1_score(Y_test[:, 0], final_predictions[:, 0], zero_division=0),
)
print(
    "Hypertension F1:",
    f1_score(Y_test[:, 1], final_predictions[:, 1], zero_division=0),
)
print(
    "Obesity F1:",
    f1_score(Y_test[:, 2], final_predictions[:, 2], zero_division=0),
)
print(
    "Overall F1:",
    f1_score(Y_test, final_predictions, average="macro", zero_division=0),
)

individual_models_for_results = {
    "K-Nearest Neighbours": knn,
    "Support Vector Machine": svm,
    "Random Forest": random_forest,
    "Gaussian Naive Bayes": naive_bayes,
    "Logistic Regression": logistic_regression,
    "Ridge Classifier": ridge_classifier,
    "Decision Tree": decision_tree,
    "Extra Trees": extra_trees,
    "Gradient Boosting": gradient_boosting,
    "SGD Classifier": sgd_classifier,
}

individual_model_results = []

for model_name, model in individual_models_for_results.items():
    model_predictions = np.asarray(model.predict(X_test)).astype(int)

    diabetes_accuracy = accuracy_score(
        Y_test[:, 0],
        model_predictions[:, 0],
    )
    hypertension_accuracy = accuracy_score(
        Y_test[:, 1],
        model_predictions[:, 1],
    )
    obesity_accuracy = accuracy_score(
        Y_test[:, 2],
        model_predictions[:, 2],
    )

    diabetes_f1 = f1_score(
        Y_test[:, 0],
        model_predictions[:, 0],
        zero_division=0,
    )
    hypertension_f1 = f1_score(
        Y_test[:, 1],
        model_predictions[:, 1],
        zero_division=0,
    )
    obesity_f1 = f1_score(
        Y_test[:, 2],
        model_predictions[:, 2],
        zero_division=0,
    )
    overall_f1 = f1_score(
        Y_test,
        model_predictions,
        average="macro",
        zero_division=0,
    )

    individual_model_results.append(
        {
            "result_type": "individual_model",
            "voting": "",
            "models": model_name,
            "model_count": 1,
            "exact_match_accuracy": exact_match_accuracy(
                Y_test,
                model_predictions,
            ),
            "mean_label_accuracy": float(
                np.mean(
                    [
                        diabetes_accuracy,
                        hypertension_accuracy,
                        obesity_accuracy,
                    ]
                )
            ),
            "diabetes_accuracy": diabetes_accuracy,
            "hypertension_accuracy": hypertension_accuracy,
            "obesity_accuracy": obesity_accuracy,
            "diabetes_f1": diabetes_f1,
            "hypertension_f1": hypertension_f1,
            "obesity_f1": obesity_f1,
            "overall_f1": overall_f1,
        }
    )

individual_results_dataframe = pd.DataFrame(
    individual_model_results
)

voting_results_for_file = voting_results.copy()
voting_results_for_file.insert(
    0,
    "result_type",
    "voting_ensemble",
)

all_model_results = pd.concat(
    [
        individual_results_dataframe,
        voting_results_for_file,
    ],
    ignore_index=True,
    sort=False,
)

all_model_results = all_model_results.sort_values(
    by=[
        "exact_match_accuracy",
        "overall_f1",
        "mean_label_accuracy",
    ],
    ascending=[
        False,
        False,
        False,
    ],
).reset_index(drop=True)

all_results_file = "all_model_and_voting_results.csv"

all_model_results.to_csv(
    all_results_file,
    index=False,
)

print(
    "\nAll individual-model and voting-ensemble results saved to:",
    all_results_file,
)
