# 
# Example of R 'seasonal' library
# 
# http://cran.r-project.org/web/packages/seasonal/index.html
# https://github.com/christophsax/seasonal
# https://www.census.gov/srd/www/winx13/winx13_down.html
# 
# Reference:
# http://cran.r-project.org/web/packages/seasonal/vignettes/seas.pdf
# https://www.census.gov/ts/TSMS/WIX13/winx13doc.pdf
# 

# 
# See also: http://ec.europa.eu/eurostat/web/research-methodology/seasonal-adjustment
# 
# 

library(seasonal)
Sys.setenv(X13_PATH = "D:\\seasonality\\winx13\\x13as")
checkX13()

# Example 1
m=seas(AirPassengers)
plot(AirPassengers)
lines(final(m), col = "red")

