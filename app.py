import pandas as pd
import xlwings as xw
import matplotlib.pyplot as plt
import os

file_path = 'inventory-report.xlsx'

df = pd.read_excel(file_path, header= 14)


df['Unnamed: 0'].head(12)
df.rename(columns={'Unnamed: 0' : 'Month'}, inplace=True)

# Subset for Each month of the year
subset_df_monthly = df.iloc[0 : 10].copy()
subset_df_monthly['Month'] = pd.to_datetime(subset_df_monthly['Month'], format='%b-%y')
subset_df_monthly['Month_Label'] = subset_df_monthly['Month'].dt.strftime('%b-%y')



print(subset_df_monthly.head(12))



# Creating the total work table for Carry over cases and cases allocated
subset_df_monthly['Total Work'] = subset_df_monthly['Carry Over Cases'] + subset_df_monthly['Cases Allocated']
subset_df_monthly['Target Cases'] = 30 * subset_df_monthly['No. of Working Days (Excluding Public Holidays and Weekends)']

subset_df_monthly['% Work Done'] = (subset_df_monthly['Actual Done'] / subset_df_monthly['Total Work']) * 100


# plotting a bar graph
subset_df_monthly.plot.bar(x='Month_Label', y= '% Work Done', color='skyblue',width=0.3,legend=False, ax=plt.gca())
plt.ylabel('% Work Done')
plt.title('Work Done by Year')
plt.xticks(rotation=0)
plt.show()

# print(df.columns)

# print(df[['Total Work', 'Target Cases', 'Actual Done', '% Work Done' ]].head())



