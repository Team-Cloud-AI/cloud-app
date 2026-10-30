allowance = 1000
print(allowance)
# monthly fixed costs
phone = 50 
groceries = 250
eatingOut = 125
emergency = 200
left_over = allowance - phone - groceries - eatingOut - emergency
print(left_over)

daily = left_over / 30
print(daily)

purchase = 8 

today_left = daily - purchase

month_left = left_over - purchase

print(today_left)
print(month_left)