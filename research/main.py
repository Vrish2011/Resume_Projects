import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import statistics
import re
df = pd.read_excel("Indian_Diet.xlsx")

dict_diet = df.to_dict(orient="records")
is_run = False
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


def check_numercal(key_want):
    for row in dict_diet:
        for key, value in row.items():
            if key == key_want:
                if type(value) != float and type(value) != int and pd.notna(value):
                    print(value)
                    return False
                
    return True



def normalize_dataset_column():
    for row in dict_diet:
        for key,value in row.items():
            if "Mention the time" in key and pd.notna(value):
                old = row[key]
                print(str(old))
                row[key] = int(convert_time_to_numbers(str(old)))
                
            if type(value) == bool:
                if value== False:
                    row[key] = 0
                if value == True:
                    row[key] = 1
            elif type(value) == str:
                if value.lower().strip() == "no":
                    row[key] = 0
                elif value.lower().strip() == "yes":
                    row[key] = 1
                elif value.lower().strip() == "false":
                    row[key] = 0
                elif value.lower().strip() == "true":
                    row[key] = 1


print(normalize_dataset_column)
                
                

def filter_dict(dict_to_filter, category, value_want, x):
    values = []
    
    
    
    

    for row in dict_to_filter:
        
        
        
        if row.get(x) == category:
            values.append(int(row.get(value_want)))

    
            
    return values



def categorize_(x, y):
   
    plt.clf()
   
   
    categories = []
    probabilities = []
    date = False
    for row in dict_diet:
        if row[x]:
            if pd.notna(row[x]) and row[x] not in categories:
                

               
                categories.append(row[x])
                
               
               
            
                    
               
                
    
    for category in categories:
        if category:
           
            row_category = filter_dict(dict_diet, category, y, x)
            amount_disease = []
            
            
            
            try:
                
                
                
                for value in row_category:
                    try:
                        if int(value) == 1:
                            amount_disease.append(int(value))
                    except (ValueError, TypeError):
                        pass
                

            except (TypeError, ValueError):
                pass
            
            if len(row_category) != 0:
                x_probability = len(amount_disease) / len(row_category)
                
                probabilities.append(x_probability)
            
    
    
            
            
    plt.xlabel(x)
    
    plt.ylabel(y)
    population_sd = 0
    
   
    population_sd = statistics.pstdev(probabilities)
    
    
    plt.bar(categories, probabilities, label=f"{population_sd}") 
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout() 

    
            
        

            
            
        
        
    

    
    
    


       
    

    
    plt.legend()
    
    plt.savefig(f"best_bar_graph{x} by {y}.png", dpi=1000, bbox_inches="tight")
    
    plt.show()
    plt.close()

    return population_sd



        



def plot(x, y):
    
    plt.close()
    model = LinearRegression()
    x_values = []
    y_values = []
    x_train = []
    y_train = []
    for row in dict_diet:
        for key, value in row.items():
            if key == x and pd.notna(value) and pd.notna(row.get(y)):

                x_values.append(float(row[x]))
                y_values.append(float(row[y]))
                x_train.append([float(row[x])])
                y_train.append(float(row[y]))
    

    

    
    
    model.fit(x_train, y_train)
    weight = model.coef_[0]
    
    bias = model.intercept_
    y_data = []

    for x_ in x_values:
        y_ = weight * x_ + bias
        y_data.append(y_)

    

    plt.xlabel(x)
    plt.ylabel(y)
    plt.scatter(x_values, y_values)
    plt.plot(x_values, y_data, label=f"r = {model.coef_[0]}")
    plt.legend()
    plt.savefig(f"best_fit_graph{x} by {y}.png", dpi=1000, bbox_inches="tight")
    
    plt.show()
    plt.close()
    return float(abs(model.coef_[0]))
    




                






normalize_dataset_column()

def run():
    plt.clf()

    numerical_d = []
    categorical_d = []
    numerical_h = []
    categorical_h = []
    numerical_o = []
    categorical_o = []

    # Go through each column only once
    for key in dict_diet[0].keys():

        if "Disease" in key:
            break

        if (
            "Date" in key
            or "Ethnicity" in key
            or "solid" in key
            or "fruit" in key
        ):
            continue

        print(key)

        if check_numercal(key):
            r_d = plot(key, "Diabetes")
            numerical_d.append({key: r_d})

            r_h = plot(key, "Hypertension")
            numerical_h.append({key: r_h})

            r_o = plot(key, "Obesity")
            numerical_o.append({key: r_o})

        else:
            c_d = categorize_(key, "Diabetes")
            categorical_d.append({key: c_d})

            c_h = categorize_(key, "Hypertension")
            categorical_h.append({key: c_h})

            c_o = categorize_(key, "Obesity")
            categorical_o.append({key: c_o})

    return (
        numerical_d,
        numerical_o,
        numerical_h,
        categorical_d,
        categorical_o,
        categorical_h
    )
numerical_d, numerical_o, numerical_h, categorical_d, categorical_o, categorical_h = run()


# Each variable above is a list of dictionaries, for example:
# [{"Age": 0.12}, {"BMI": 0.47}, {"Water Intake": 0.31}]

dictionaries = [
    numerical_d,
    numerical_o,
    numerical_h,
    categorical_d,
    categorical_o,
    categorical_h
]

dictionary_names = [
    "Numerical Diabetes",
    "Numerical Obesity",
    "Numerical Hypertension",
    "Categorical Diabetes",
    "Categorical Obesity",
    "Categorical Hypertension"
]


def combine_list_of_dicts(list_of_dicts):
    combined_dictionary = {}

    for dictionary in list_of_dicts:
        combined_dictionary.update(dictionary)

    return combined_dictionary


def get_highest_columns(list_of_dicts):
    if not list_of_dicts:
        return set()

    combined_dictionary = combine_list_of_dicts(list_of_dicts)

    if not combined_dictionary:
        return set()

    highest_value = max(combined_dictionary.values())

    highest_columns = {
        column
        for column, value in combined_dictionary.items()
        if value == highest_value
    }

    return highest_columns


highest_columns = []

for dictionary_list in dictionaries:
    columns = get_highest_columns(dictionary_list)
    highest_columns.append(columns)


print("\nHighest columns in each category:")

for name, columns in zip(dictionary_names, highest_columns):
    print(f"{name}: {columns}")


# Find columns that are highest in all six lists
if highest_columns and all(highest_columns):
    shared_columns = set.intersection(*highest_columns)
else:
    shared_columns = set()


print("\nColumns shared across all highest-value groups:")
print(shared_columns)