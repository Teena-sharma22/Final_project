import pandas as pd


# 1. Load Data

data = pd.read_csv("retail_datasett_edit.csv", parse_dates=['Date'])
print(data.head())


# 2. Data Cleaning

# Check initial nulls
print("Before Cleaning:\n", data.info())

# Fill Gender
data["Gender"] = data["Gender"].fillna(data['Gender'].mode()[0])

# Fill Age
data['Age'] = data['Age'].fillna(data['Age'].mean())

# Fill Cost Price
data['Cost_Price'] = data['Cost_Price'].fillna(data['Cost_Price'].mean())

# Fill Region
data['Region'] = data['Region'].fillna(data['Region'].mode()[0])

# Drop remaining nulls if any
data.dropna(inplace=True)

# Remove duplicates
data.drop_duplicates(inplace=True)

# Convert categorical fields
data['Gender'] = data['Gender'].astype('category')
data['Category'] = data['Category'].astype('category')
data['Sub-Category'] = data['Sub-Category'].astype('category')
data['Region'] = data['Region'].astype('category')

print("✅ Data cleaned:")
print(data.info())


# 3. Profit Calculations

data['Profit'] = data['Total_Sales'] - data['Total Cost']
data['Profit_Margin'] = (data['Profit'] / data['Total_Sales']) * 100

category_profit = data.groupby(['Category', 'Sub-Category'])[['Total_Sales', 'Total Cost', 'Profit']].sum().reset_index()
category_profit['Profit_Margin'] = (category_profit['Profit'] / category_profit['Total_Sales']) * 100

# 4. Inventory Turnover Analysis

data['Average_Inventory'] = (data['Opening_Inventory'] + data['Closing_Inventory']) / 2
data['Inventory_Days'] = data['Average_Inventory'] / (data['Total_Sales'] / data['Date'].dt.daysinmonth)

# Correlation
correlation = data[['Inventory_Days', 'Profit']].corr()
print("📊 Correlation between Inventory Days and Profit:\n", correlation)


# 5. Seasonal Analysis

def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'

data['Month'] = data['Date'].dt.month
data['Season'] = data['Month'].apply(get_season)

seasonal_profit = data.groupby(['Season', 'Category'])['Profit'].sum().reset_index()

# 6. Strategic Flags

data['Slow_Moving'] = (data['Inventory_Days'] > data['Inventory_Days'].quantile(0.75)) & \
(data['Profit'] < data['Profit'].quantile(0.25))

data['Overstocked'] = data['Opening_Inventory'] > (data['Closing_Inventory'] * 1.5)

strategic_flags = data[data['Slow_Moving'] | data['Overstocked']]


# 7. Export to CSV file

data.to_csv('processed_retail_data.csv', index=False)
category_profit.to_csv('category_profit.csv', index=False)
seasonal_profit.to_csv('seasonal_profit.csv', index=False)
strategic_flags.to_csv('strategic_flags.csv', index=False)

print("✅ All cleaned and analyzed data exported.")

