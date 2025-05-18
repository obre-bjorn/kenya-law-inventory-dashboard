import pandas as pd

# Gets Data from every user and combine them 
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

        # Create a human-readable label
        df['Month_Label'] = df['Month'].dt.strftime('%b-%y')

        # Sort by month
        df = df.sort_values(by='Month')

        data_by_person[name] = df

    # Combine all persons’ data into one DataFrame
    all_data = pd.concat(data_by_person.values(), ignore_index=True)

    return all_data

if __name__ == "__main__":
    getDataFromExcelSheets('inventory-report.xlsx')