import seaborn as sms
from scipy.stats.contingency import association
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_excel("Indian_Diet.xlsx")
categorical_column_names = [
    "Gender",
    "Ethnicity",
    "Country",
    "Current Location",
    "Food Preference",
    "Water Intake",
    "Lifestyle (Exercise)",

    "Rate you energy levels today",

    "Mention the solid food you had for Breakfast",
    "How would you rate the portion size of your Breakfast",

    "Mention the solid food you had for Lunch",
    "How would you rate the portion size of your lunch",

    "Mention the solid food you had for evening Snacks",
    "How would you rate the portion size of your snack",

    "Mention the solid food you had for evening Dinner",
    "How would you rate the portion size of your Dinner",

    "Mention any fruits you had in the day",

    "On a scale of 0 to 10, how thirsty do you feel today",

    "Did you consume any other beverages today?",
    "If Yes, Mention the type of drink.",

    "Do you have any diagnosed dietary health conditions?",

    "If you did Physical Activity, mention what activities did you do",

    "Are you currently following any exercise regimen recommended by a healthcare professional",

    "Are you on any type of medication",
    "Mention the medicines you take, and the amount of dosage",

    "On a scale of 0 to 10,  how would you rate your stress/anxiety level",

    "If you did feel stressed today, how did you deal with it",

    "Does any of your close family have the same health conditions as you",

    "If yes, mention what condition do you have in common",

    "If Yes, Mention your relationship to the person who has the same condition as you.",

    "Is there anything else you would like to share about your dietary habits or health that has not been covered in this survey?"
]

results = []
def association_heatmap_diabetes():
    for category in categorical_column_names:
        table = pd.crosstab(df[category], df["Diabetes"])
        value = association(table.to_numpy(), method="cramer")
        results.append({"feature": category, "value": value})
    
    df_results = pd.DataFrame(results).set_index("feature")
    print(df_results)
    sms.heatmap(df_results)
    plt.title("Diabetes association Heatmap")
    plt.ylabel("Features")
    plt.xlabel("")
    plt.tight_layout()

   





    plt.savefig("diabetes_categorical_heatmap.png",  bbox_inches="tight", dpi=600)
    plt.show()

    


association_heatmap_diabetes()


results = []
def association_heatmap_hypertension():
    plt.close()
    for category in categorical_column_names:
        table = pd.crosstab(df[category], df["Diabetes"])
        value = association(table.to_numpy(), method="cramer")
        results.append({"feature": category, "value": value})
    
    df_results = pd.DataFrame(results).set_index("feature")
    print(df_results)
    sms.heatmap(df_results)
    plt.title("Hypertension association Heatmap")
    plt.ylabel("Features")
    plt.xlabel("")
   
    plt.tight_layout()

   





    plt.savefig("hypertension_categorical_heatmap.png",  bbox_inches="tight",dpi=600)
    plt.show()

    


association_heatmap_hypertension()
