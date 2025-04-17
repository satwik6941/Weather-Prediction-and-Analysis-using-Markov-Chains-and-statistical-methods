import pandas as pd
from scipy.stats import ttest_ind

df = pd.read_csv("weather_Data_updated.csv")

df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d-%m-%Y %H.%M')

df['year_month'] = df['timestamp'].dt.to_period('M')

monthly_groups = df.groupby('year_month')['temperature_2m'].apply(list)

t_test_results = []

for i in range(len(monthly_groups) - 1):
    month1 = monthly_groups.index[i]
    month2 = monthly_groups.index[i + 1]
    temps1 = monthly_groups.iloc[i]
    temps2 = monthly_groups.iloc[i + 1]

    t_stat, p_value = ttest_ind(temps1, temps2, equal_var=False)

    t_test_results.append({
        'Month 1': str(month1),
        'Month 2': str(month2),
        'T-Statistic': t_stat,
        'P-Value': p_value
    })

t_test_df = pd.DataFrame(t_test_results)

print(t_test_df)