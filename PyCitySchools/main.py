# Dependencies and Setup
import pandas as pd
from pathlib import Path

# File to Load (Remember to Change These)
school_data_to_load = Path("C:/Users/ipsit/Downloads/Starter_Code/PyCitySchools/Resources/schools_complete.csv")
student_data_to_load = Path("C:/Users/ipsit/Downloads/Starter_Code/PyCitySchools/Resources/students_complete.csv")

# Read School and Student Data File and store into Pandas DataFrames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset.  
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])
school_data_complete.head()

"""---------------------------------------------DISTRICT SUMMARY------------------------------------------------------"""

school_count = school_data_complete['school_name'].nunique()
print (school_count)

student_count  = school_data_complete['Student_ID'].nunique()
print (student_count)

total_budget = school_data['budget'].sum()
print (total_budget)

avg_math_score = student_data['math_score'].mean()
print (avg_math_score)

avg_reading_score = student_data['reading_score'].mean()
print (avg_reading_score)

passing_math_count = school_data_complete[(school_data_complete["math_score"] >= 70)].count()["student_name"]
passing_math_percentage = passing_math_count / float(student_count) * 100
print (passing_math_percentage)

passing_reading_count = school_data_complete[(school_data_complete["reading_score"] >= 70)].count()["student_name"]
passing_reading_percentage = passing_reading_count / float(student_count) * 100
print (passing_reading_percentage)

passing_math_reading_count = school_data_complete[
    (school_data_complete["math_score"] >= 70) & (school_data_complete["reading_score"] >= 70)
].count()["student_name"]
overall_passing_rate = passing_math_reading_count /  float(student_count) * 100
print (overall_passing_rate)

# Create a summary dataframe
district_summary = pd.DataFrame({
    'Total Schools': [school_count],
    'Total Students': [student_count],
    'Total Budget': [total_budget],
    'Average Math Score': [avg_math_score],
    'Average Reading Score': [avg_reading_score],
    '% Passing Math': [passing_math_percentage],
    '% Passing Reading': [passing_reading_percentage],
    '% Overall Passing': [overall_passing_rate]
})

print (district_summary)

"""--------------------------------------------------SCHOOL SUMMARY--------------------------------------------------"""

school_type = school_data['type'].unique()
print(school_type)

school_data_complete['per_student_budget'] = school_data_complete['budget'] / school_data_complete['size']

# Calculate average math and reading scores
school_data_complete['average_math_score'] = school_data_complete['math_score'].mean()
school_data_complete['average_reading_score'] = school_data_complete['reading_score'].mean()

# Calculate the percentage passing math, reading, and overall passing
school_data_complete['passing_math'] = ((school_data_complete['math_score'] >= 70) * 100)
#school_data_complete['passing_math']  = school_data_complete['passing_math'].round(2)
school_data_complete['passing_reading']= ((school_data_complete['reading_score'] >= 70) * 100)
#school_data_complete['passing_reading'] = school_data_complete['passing_reading'].round(2)

school_data_complete['passing_overall'] = ((school_data_complete['passing_math'] & school_data_complete['passing_reading']))
#school_data_complete['passing_overall'] = school_data_complete['passing_overall'].round(2)

school_summary = school_data_complete.groupby(['school_name','type']).agg({
    'size': 'count',
    'budget': 'first',
    'per_student_budget': 'first',
    'math_score': 'mean',
    'reading_score': 'mean',
    'passing_math': 'mean',
    'passing_reading': 'mean',
    'passing_overall': 'mean'
}).reset_index()

school_summary.columns = [
    'School_Name', 'School_Type', 'Total_Students', 'Total_School_Budget', 
    'Per_Student_Budget', 'Average_Math_Score', 'Average_Reading_Score',
    '%_Passing_Math', '%_Passing_Reading', '%_Overall_Passing'
    ]

school_summary['Average_Math_Score'] = school_summary['Average_Math_Score'].round(2)
school_summary['Average_Reading_Score'] = school_summary['Average_Reading_Score'].round(2)
school_summary['%_Passing_Math'] = school_summary['%_Passing_Math'].round(2)
school_summary['%_Passing_Reading'] = school_summary['%_Passing_Reading'].round(2)
school_summary['%_Overall_Passing'] = school_summary['%_Overall_Passing'].round(2)


print (school_summary)

"""------------------------------------------HIGHEST PERFORMING SCHOOLS------------------------------------------"""

