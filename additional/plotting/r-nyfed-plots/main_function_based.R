require(ggplot2)
require(scales)
require(wq)
require(zoo)


setwd("D:\\rfolder\\rcode\\nyfed-plots\\csv\\")
# setwd("c:\\Users\\user\\Dropbox\\work\\pogrebnyak\\") # where the script and *.csv is placed

# creating new theme, based on the default ggplot2 theme: theme_bw
# * updating plot back to have black border and white background
# * removing major grid
# * adding dashed minor grid with grey color
# * updating font size and face for title, hjust=0 - left-aligned text.
# * removing axis ticks

theme_my <- theme_set(theme_bw())
theme_my <- theme_update(panel.background=element_rect(fill="white", colour="black")
                         , panel.border=element_rect(fill=NA, colour="black", size=0.5)
                         , panel.grid.major.x=element_blank()
                         , panel.grid.minor.x=element_line(linetype = "dotted", colour="grey")
                         , panel.grid.major.y=element_line(linetype = "dotted", colour="grey")
                         , panel.grid.minor.y=element_blank()
                         , plot.title=element_text(size=16, face="bold", colour="black", hjust=0)
                         , axis.ticks=element_blank()
                         #, axis.text.x=element_text(size=14)
                         #, axis.text.y=element_text(size=12)
                         )


# MONTHLY PLOTTING
# This is a minimum formulation to run gg plot
  gg_monthly = function(ts, caption.text, y.limits, y.breaks, x.limits)
  {	gg <- ggplot(ts, aes(x=date, y=value, group=1)) +  geom_line(size=1)
	return(gg)	}
# gg_monthly(industrial, caption.text, y.limits, y.breaks, x.limits) 

# This is an extended formulation to run gg plot

  # adding title and removing axis labels
  labs(title="Gross Domestic Product\nFour-quarter percentage change", x="", y="") +
  # adding X limits and ticks, writting them as a full year
  scale_x_date(expand = c(0,0), limits=as.Date(c("2009-01-01", "2015-01-01")), labels=date_format("%Y"), breaks=seq(as.Date("2009-07-01"), as.Date("2014-07-01"), by="year"), minor_breaks="year") +
  # limits and ticks for Y
  scale_y_continuous(expand = c(0,0), limits=c(-6, 6), breaks=seq(-6, 6, 2)) +
  geom_line(size=1) +
  # horizontal line
  geom_hline(yintercept=0) +
  # point on the end of the data-set
  geom_point(aes(x=tail(gross$date, 1), y=tail(gross$product, 1))) +
  # annotation near the end of the data-set
  geom_text(aes(x=tail(gross$date, 1) + 60, y=tail(gross$product, 1)), label=paste("Q3", "\n", sprintf("%.1f", tail(gross$product, 1))), hjust=0, vjust=0.5)




  gg_main = function(ts, caption.text, y.limits, y.breaks, x.limits)
  {	gg <- ggplot(ts, aes(x=date, y=value, group=1)) +
       	
		# adding title and removing axis labels
		labs(title=caption.text, x="", y="") +
		# TODO 1:  we want title to be plain, not in bold and smaller font 
		# TODO 2:  we want second line (subtitle) to be in smaller font

		# adding X limits and ticks, writting them as a full year
		scale_x_date(expand = c(0,0), limits=as.Date(x.limits), labels=date_format("%Y"), 
			breaks=seq(as.Date("2009-07-01"), as.Date("2014-07-15"), by="year"), minor_breaks="year") +
		# TODO 3:  calculate "breaks" based on "x.limits" 

		# limits and ticks for Y
		scale_y_continuous(expand = c(0,0), limits=y.limits, breaks=y.breaks) +

            geom_line(size=1) +

       	# point on the end of the data-set
		geom_point(aes(x=tail(ts$date, 1), y=tail(ts$value, 1)))

	return(gg)	
		}


  # annotation near the end of the data-set
  gg_tail_label_monthly = function(ts){
		geom_text(aes(x=tail(ts$date, 1) + 60, y=tail(ts$value, 1)), 
				label=paste(format(tail(ts$date, 1), format="%b"), "\n", 
	            	sprintf("%.1f", tail(ts$value, 1))), hjust=0, vjust=0.5)
		# TODO 4:  change formatting of number so that it sticks to the left of the box
		# TODO 5:  suggest other formatting of month different from format="%b"
	}

  gg_tail_label_quarter = function(ts){
	  geom_text(aes(x=tail(ts$date, 1) + 60, y=tail(ts$value, 1)), 
			label=paste("Q3", "\n", sprintf("%.1f", tail(ts$value, 1))), 
				hjust=0, vjust=0.5)
		# TODO 6:  change "Q3" - compute it based on last observation date
	}


  industrial <- read.csv("industrial.csv", sep=";", dec=",", header=FALSE, col.names=c("date", "value"))
  industrial$date <- as.Date(industrial$date, "%d.%m.%Y")
  ts = industrial 
  caption.text = "Industrial Production\nIndex, 1997=100"
  x.limits = c("2009-01-01", "2015-01-01")
  y.limits =c(76, 108)
  y.breaks = seq(76, 108, 4)
  y.intercept = 100
  industrial_plot  = gg_main(industrial, caption.text, y.limits, y.breaks, x.limits) + 
                      geom_hline(yintercept=y.intercept) +  gg_tail_label_monthly(ts)
  # industrial_plot

  unemployement <- read.csv("unemployement.csv", sep=";", dec=",", header=FALSE, col.names=c("date", "value"))
  unemployement$date <- as.Date(unemployement$date, "%d.%m.%Y")
  ts = unemployement
  caption.text = "Unemployment Rate\nPercent"
  x.limits = c("2009-01-01", "2015-01-01")
  y.limits = c(6.5, 11.5)
  y.breaks = seq(6.5, 11.5)
  y.intercept = 0
  unemployement_plot  = gg_main(ts, caption.text, y.limits, y.breaks, x.limits) +
					gg_tail_label_monthly(ts) 

  # unemployement_plot


  price <- read.csv("price.csv", sep=";", dec=",", header=FALSE, col.names=c("date", "value"))
  price$date <- as.Date(price$date, "%d.%m.%Y")
  ts = price 
  caption.text = "Consumer Price Index\n12-Month Percentage Change"
  x.limits = c("2009-01-01", "2015-01-01")
  y.limits = c(-4, 6)
  y.breaks = seq(-4, 6, 2)
  y.intercept = 0
  price_plot  = gg_main(ts, caption.text, y.limits, y.breaks, x.limits) + 
					gg_tail_label_monthly(ts)

  # price_plot

# QUARTERLY PLOTTING
  gross <- read.csv("gross.csv", sep=";", dec=",", header=FALSE, col.names=c("date", "value"))
  gross$date <- as.Date(gross$date, "%d.%m.%Y") # updating first column to actual Date objects
  gross$value <- gross$value * 100
  ts = gross 
  caption.text = "Gross Domestic Product\nFour-quarter percentage change"
  x.limits = c("2009-01-01", "2015-01-01")
  y.limits = c(-6, 6)
  y.breaks = seq(-6, 6, 2)
  y.intercept = 0
  gdp_plot = gg_main(ts, caption.text, y.limits, y.breaks, x.limits) + 
		 geom_hline(yintercept=y.intercept) + gg_tail_label_quarter(ts)
  gdp_plot

# PLOT 4 GRAPHS ON A PAGE
  windows()
  gdp_plot
  industrial_plot
  unemployement_plot
  price_plot

		# TODO 7: all plots are displayed separately OK, but layOut fails with warnings:

#Ошибка в unit(x, default.units) : 'x' and 'units' must have length > 0
#Вдобавок: Предупреждения
#1: Removed 57 rows containing missing values (geom_point). 
#2: Removed 57 rows containing missing values (geom_text). 

  layOut(list(gdp_plot, 1, 1), list(industrial_plot, 1, 2), 
		list(unemployement_plot, 2, 1), list(price_plot, 2, 2))