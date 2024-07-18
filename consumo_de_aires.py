# Define the power consumption in watts and usage time in hours
power_consumption_watts = 3200  # 1200 W
usage_time_hours_per_day = 1    # 1 hour per day

# Calculate daily consumption in kilowatt-hours (kWh)
daily_consumption_kwh = (power_consumption_watts * usage_time_hours_per_day) / 1000  # Convert to kWh

# Assume a month has 30 days for calculation
days_per_month = 30

# Calculate monthly consumption
monthly_consumption_kwh = daily_consumption_kwh * days_per_month

# Print the monthly consumption
print(f"The monthly consumption of the air conditioner is {monthly_consumption_kwh} kWh.")

