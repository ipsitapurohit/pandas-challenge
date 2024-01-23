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
school_data_complete['passing_reading']= ((school_data_complete['reading_score'] >= 70) * 100)
school_data_complete['passing_overall'] = ((school_data_complete['passing_math'] & school_data_complete['passing_reading']))

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

"""------------------------------------------HIGHEST PERFORMING SCHOOLS----------------------------------------------"""

top_schools = school_summary.sort_values(by='%_Overall_Passing', ascending=False).head(5)
print(top_schools)


"""------------------------------------------LOWEST PERFORMING SCHOOLS-----------------------------------------------"""

bottom_schools = school_summary.sort_values(by='%_Overall_Passing').head(5)
print(bottom_schools)

"""------------------------------------------MATH SCORES BY GRADE-----------------------------------------------------"""

# Use the code provided to separate the data by grade
ninth_graders = school_data_complete[(school_data_complete["grade"] == "9th")]
tenth_graders = school_data_complete[(school_data_complete["grade"] == "10th")]
eleventh_graders = school_data_complete[(school_data_complete["grade"] == "11th")]
twelfth_graders = school_data_complete[(school_data_complete["grade"] == "12th")]

# Group by 'school_name' and take the mean of the 'math_score' column for each grade
ninth_grade_math_scores = ninth_graders.groupby("school_name")["math_score"].mean()
tenth_grade_math_scores = tenth_graders.groupby("school_name")["math_score"].mean()
eleventh_grade_math_scores = eleventh_graders.groupby("school_name")["math_score"].mean()
twelfth_grade_math_scores = twelfth_graders.groupby("school_name")["math_score"].mean()

# Combine each of the scores above into a single DataFrame called 'math_scores_by_grade'
math_scores_by_grade = pd.DataFrame({
    '9th Grade': ninth_grade_math_scores,
    '10th Grade': tenth_grade_math_scores,
    '11th Grade': eleventh_grade_math_scores,
    '12th Grade': twelfth_grade_math_scores
})

# Minor data wrangling
math_scores_by_grade.index.name = 'School Name'

# Display the DataFrame
print(math_scores_by_grade)


"""------------------------------------------READING SCORES BY GRADE---------------------------------------------------"""

# Use the code provided to separate the data by grade
ninth_graders = school_data_complete[(school_data_complete["grade"] == "9th")]
tenth_graders = school_data_complete[(school_data_complete["grade"] == "10th")]
eleventh_graders = school_data_complete[(school_data_complete["grade"] == "11th")]
twelfth_graders = school_data_complete[(school_data_complete["grade"] == "12th")]

# Group by `school_name` and take the mean of the `reading_score` column for each grade
ninth_grade_reading_scores = ninth_graders.groupby("school_name")["reading_score"].mean()
tenth_grade_reading_scores = tenth_graders.groupby("school_name")["reading_score"].mean()
eleventh_grade_reading_scores = eleventh_graders.groupby("school_name")["reading_score"].mean()
twelfth_grade_reading_scores = twelfth_graders.groupby("school_name")["reading_score"].mean()

# Combine each of the scores above into a single DataFrame called `reading_scores_by_grade`
reading_scores_by_grade = pd.DataFrame({
    '9th Grade': ninth_grade_reading_scores,
    '10th Grade': tenth_grade_reading_scores,
    '11th Grade': eleventh_grade_reading_scores,
    '12th Grade': twelfth_grade_reading_scores
})

# Minor data wrangling
reading_scores_by_grade = reading_scores_by_grade[["9th Grade", "10th Grade", "11th Grade", "12th Grade"]]
reading_scores_by_grade.index.name = 'School Name'

# Display the DataFrame
print(reading_scores_by_grade)


"""------------------------------------------SCORES BY SCHOOL SPENDING-------------------------------------------------"""

# Assuming merged_df is the merged DataFrame from above
spending_bins = [0, 585, 630, 645, 680]
labels = ["<$585", "$585-630", "$630-645", "$645-680"]

school_data_complete['Spending Ranges (Per Student)'] = pd.cut(school_data_complete['budget'] / school_data_complete['size'], bins=spending_bins, labels=labels)

spending_summary = school_data_complete.groupby('Spending Ranges (Per Student)').agg({
    'math_score': 'mean',
    'reading_score': 'mean',
    'passing_math': 'mean',
    'passing_reading': 'mean',
    'passing_overall': 'mean'
}).reset_index()

print(spending_summary)


"""-----------------------------------------SCORES BY SCHOOL SIZE--------------------------------------------------------"""

# Assuming you have a per_school_summary DataFrame with 'Total Students' column
size_bins = [0, 1000, 2000, 5000]
labels = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]

# Use pd.cut to categorize school size based on the bins
school_data_complete['School_Size'] = pd.cut(school_data_complete['size'], bins=size_bins, labels=labels)

# Group by 'School_Size' and calculate mean scores
size_summary = school_data_complete.groupby('School_Size').agg({
    'math_score': 'mean',
    'reading_score': 'mean',
    'passing_math': 'mean',
    'passing_reading': 'mean',
    'passing_overall': 'mean'
}).reset_index()

print(size_summary)


"""-----------------------------------------------SCORES BY SCHOOL TYPE--------------------------------------------------"""

# Assuming you have a school_summary DataFrame with 'School_Type' column
type_summary = school_summary.groupby('School_Type').agg({
    'Average_Math_Score': 'mean',
    'Average_Reading_Score': 'mean',
    '%_Passing_Math': 'mean',
    '%_Passing_Reading': 'mean',
    '%_Overall_Passing': 'mean'
}).reset_index()

print(type_summary)



"""--------------------------------------------END OF ASSIGNMENT--------------------------------------------------------"""