library(seasonal)
Sys.setenv(X13_PATH = "D:\\seasonality\\winx13\\x13as")
setwd("D:\\seasonality")

filename = "avia.txt"
data = read.table(filename, sep = "\t", header = TRUE, dec = ",")
dates = as.Date(data[,1], format="%d.%m.%Y")
val = data[,2] 	
index = !is.na(val)
dates = dates [index]
val   = val   [index]

month = as.numeric(format(dates[1], "%m")) 
year = as.numeric(format(dates[1], "%Y"))
start1 = c(year, month)
ru_air = ts(val, start = start1, frequency = 12)

m=seas(ru_air)
plot(ru_air)
lines(final(m), col = "red")

write.csv(ru_air, "avia_sa.txt")

#Write back as CSV
