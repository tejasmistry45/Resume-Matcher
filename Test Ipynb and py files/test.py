import pandas as pd

df = pd.read_csv('C:/Users/Admin/Downloads/final_resume.csv')
# df.head(1)

column_name = 'resume_text'

column_data = df[column_name].tolist()
print(column_data[1])
