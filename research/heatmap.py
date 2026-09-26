import pandas as pd
import seaborn as sms
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

numerical_columns = [
    "Age",
    "Weight (kg)",
    "Height (cm)",
    "Rate you energy levels today",
    "How many times a day do you normally eat (include all solid foods i.e., breakfast, lunch, evening snack, dinner)",

    "Mention the time when you had Breakfast",
    "Mention the time when you had Lunch",
    "Mention the time when you had evening Snacks",
    "Mention the time when you had Dinner",

    "On a scale of 0 to 10, how thirsty do you feel today",
    "How much water do you have in a day (in liters)",

    "Mention the amount of time of physical activity",

    "What time did you sleep last night",
    "What time did wake up today",

    "On a scale of 0 to 10,  how would you rate your stress/anxiety level",
    "BMI"

    
]

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
                print(key)
                row[key] = int(convert_time_to_numbers(str(old)))
            
            elif "What time" in key and pd.notna(value):
                old = row[key]
                print(key)
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


normalize_dataset_column()
def create_hypertension_heatmap_data():
    y = "Hypertension"
    
    
    
    plt.close()
  
    

    Coorelations = []

    for numerical in numerical_columns:
        print(numerical)
        x_values = []
        y_values = []
        x_train = []
        y_train = []
    
    
    
        x = numerical
       
        model = LinearRegression()
        for row in dict_diet:
            for key, value in row.items():
               
                if key == x and pd.notna(value) and pd.notna(row.get(y)) and (type(row[x]) == int or type(row[x]) == float) :
                    
                    
                    
                    x_train.append([float(row[x])])
                    y_train.append(float(row[y]))
        try:
            model.fit(x_train, y_train)
            weight = model.coef_[0]
            
            Coorelations.append({"Feature": numerical, "Coorelations": weight})
        except:
            continue

        
        
        
        

    
               
                
               
           

                
    
        
        



        
    

    df = pd.DataFrame(Coorelations)
    df = df.set_index("Feature")
    print(df)
    sms.heatmap(df)
    plt.xlabel("Diseases")
    plt.ylabel("Features")
    plt.tight_layout()

    plt.show()
    plt.legend()
    plt.savefig("hypertension_heatmap.png",  bbox_inches="tight", dpi=300)



create_hypertension_heatmap_data()



def create_diabetes_heatmap_data():
    y = "Diabetes"
    
    
    plt.close()
  
    
    

    Coorelations = []

    for numerical in numerical_columns:
        
        x_values = []
        y_values = []
        x_train = []
        y_train = []
    
    
    
        x = numerical
        model = LinearRegression()
        for row in dict_diet:
            for key, value in row.items():
                if key == x and pd.notna(value) and pd.notna(row.get(y)) and (type(row[x]) == int or type(row[x]) == float) :
                    
                    x_train.append([float(row[x])])
                    y_train.append(float(row[y]))
        try:
            model.fit(x_train, y_train)
            weight = model.coef_[0]
            Coorelations.append({"Feature": numerical, "Coorelations": weight})
        except:
            continue
        
        
        
        

   
        
            
                
               
           

                
    
        
        



        
    

    df = pd.DataFrame(Coorelations)
    df = df.set_index("Feature")
    sms.heatmap(df)
    plt.xlabel("Diseases")
    plt.ylabel("Features")
    plt.tight_layout()

    
    plt.savefig("diabeties_heatmap.png",  bbox_inches="tight", dpi=300)
    plt.show()
    



create_diabetes_heatmap_data()

    
    
    

    

    
    
    

    
    


def create_diabeties_heatmap():
    df = pd.read_csv("diabetes_correlations.csv")
    df = df.set_index("Correlations")
    sms.heatmap(df)
    plt.show()
    plt.title("Diabetes Correlation Heatmap")
    plt.ylabel("Features")
    plt.xlabel("")
    plt.tight_layout()
   





    plt.savefig("diabeties_heatmap.png", dpi=600)
    plt.show()
    



def create_hypertension_heatmap():
    plt.close()
    df = pd.read_csv("hypertension_correlations.csv")
    df = df.set_index("Correlations")
    sms.heatmap(df)
    plt.show()
    plt.title("Hypertension Correlation Heatmap")
    plt.ylabel("Features")
    plt.xlabel("")
    plt.tight_layout()
   





    plt.savefig("hypertension_heatmap.png", dpi=600)
    plt.show()


