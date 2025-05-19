def assign_financial_quarter(month):
    if month >= 7 and month <= 9:
        return "Q1"
    elif month >= 10 and month <= 12:
        return "Q2"
    elif month >= 1 and month <= 3:
        return "Q3"
    else:
        return "Q4"

def assign_financial_year(row):
    year = row['Month'].year
    if row['Month'].month >= 7:
        return f"{year}-{year+1}"
    else:
        return f"{year-1}-{year}"

# In your data processing after 'Month' column exists
all_data["Financial_Quarter"] = all_data["Month"].dt.month.apply(assign_financial_quarter)
all_data["Financial_Year"] = all_data.apply(assign_financial_year, axis=1)
all_data["Fin_Quarter_Label"] = all_data["Financial_Year"] + " " + all_data["Financial_Quarter"]