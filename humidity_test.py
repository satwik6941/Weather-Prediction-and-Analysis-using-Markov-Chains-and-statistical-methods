import pandas as pd
from scipy.stats import pearsonr

df = pd.read_csv("weather_Data_updated.csv")

humid_temp_corr = df["temperature_2m"].corr(df["humidity_2m"])
humid_precip_corr = df["precipitation"].corr(df["humidity_2m"])

print(humid_temp_corr)
print(humid_precip_corr)

# correlation_coeff_1, p_val_1 = pearsonr(df["temperature_2m"], df["humidity_2m"])
# correlation_coeff_2, p_val_2 = pearsonr(df["precipitation"], df["humidity_2m"])

# print(f"Correlation coeff_1: {correlation_coeff_1}")
# print(f"P-val_1: {p_val_1}")
# print(f"Correlation coeff_2: {correlation_coeff_2}")
# print(f"P-val_2: {p_val_2}")