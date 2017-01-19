def multiple_of_5(x)
  x - x % 5
end

def mins_multiple_of_5(time)
  time - (time.min % 5).minutes
end

def expect_same_minute(datetime_1, datetime_2)
  expect(mins_multiple_of_5(datetime_1).strftime("%F %R")).to eq(mins_multiple_of_5(datetime_2).strftime("%F %R"))
end

def illegal_dates
  cur = Date.current
  non_leap_year = cur.year % 4 == 0 ? cur.year + 1 : cur.year
  [ {month: 'Feb', day: '30'}, {month: 'Feb', day: '31'},
    {year: non_leap_year, month: 'Feb', day: '29'}, {month: 'Apr', day: '31'},
    {month: 'Jun', day: '31'}, {month: 'Sep', day: '31'},
    {month: 'Nov', day: '31'} ]
end
