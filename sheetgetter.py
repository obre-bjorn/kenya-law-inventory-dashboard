import pandas as pd

# Gets Data from every user and combine them 
import pandas as pd

def assign_financial_quarter(month):
    if 7 <= month <= 9:
        return "Q1"
    elif 10 <= month <= 12:
        return "Q2"
    elif 1 <= month <= 3:
        return "Q3"
    else:
        return "Q4"

def assign_financial_year(row):
    year = row['Month'].year
    if row['Month'].month >= 7:
        return f"{year}-{year+1}"
    else:
        return f"{year-1}-{year}"


def getDataFromExcelSheets(excel_path):
    # Read all sheets with header on row 14 (index 14)
    sheets = pd.read_excel(excel_path, sheet_name=None, header=14)
    
    data_by_person = {}

    for name, df in sheets.items():
        df = df.iloc[0:10]  # Only take first 10 rows

        # Rename columns
        df.columns = ["Month", "Working Days", "Carry", "Cases", "Target", "Actual", 
                    "Variance", "Pending", "Results", "Comment", "Annual"]
        
        df["Person"] = name  # Add person info

        # Drop rows where 'Month' is NaN
        df = df.dropna(subset=['Month'])

        # Convert 'Month' to datetime
        df['Month'] = pd.to_datetime(df['Month'], format='%b-%y', errors='coerce')

        # Drop rows where conversion failed
        df = df.dropna(subset=['Month'])

        # Create readable label and sort
        df['Month_Label'] = df['Month'].dt.strftime('%b-%y')
        df = df.sort_values(by='Month')
        
        
        # Add quarter and financial year columns
        df["Financial_Quarter"] = df["Month"].dt.month.apply(assign_financial_quarter)
        df["Financial_Year"] = df.apply(assign_financial_year, axis=1)
        df["Fin_Quarter_Label"] = df["Financial_Year"] + " " + df["Financial_Quarter"]
        
        
        

        # Compute Fair Target = Carry + Cases
        df['Fair_Target'] = df['Carry'] + df['Cases']

        # Compute Performance % safely
        df['Performance_%'] = (df['Actual'] / df['Fair_Target']) * 100
        df['Performance_%'] = df['Performance_%'].round(2)

        # Add Flag
        def grade(p):
            if pd.isna(p):
                return "❓ No Data"
            elif p >= 70:
                return "✅ Met Expectation"
            else:
                return "⚠️ Underperformed"
            
        
        df['Flag'] = df['Performance_%'].apply(grade)

        data_by_person[name] = df

    # Combine all persons’ data into one DataFrame
    all_data = pd.concat(data_by_person.values(), ignore_index=True)

    return all_data
