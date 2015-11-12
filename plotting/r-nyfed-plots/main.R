
require(ggplot2)
require(scales)
require(wq)

# package.include("zoo")
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

gross <- read.csv("gross.csv", sep=";", dec=",", header=FALSE, col.names=c("date", "product"))
gross$date <- as.Date(gross$date, "%d.%m.%Y") # updating first column to actual Date objects
gross$product <- gross$product * 100

gross_plot <- ggplot(gross, aes(x=date, y=product, group=1)) +
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

industrial <- read.csv("industrial.csv", sep=";", dec=",", header=FALSE, col.names=c("date", "production"))
industrial$date <- as.Date(industrial$date, "%d.%m.%Y")

industrial_plot <- ggplot(industrial, aes(x=date, y=production, group=1)) +
  labs(title="Industrial Production\nIndex, 1997=100", x="", y="") +
  scale_x_date(expand = c(0,0), limits=as.Date(c("2009-01-01", "2015-01-01")), labels=date_format("%Y"), breaks=seq(as.Date("2009-06-01"), as.Date("2014-06-15"), by="year"), minor_breaks="year") +
  scale_y_continuous(expand = c(0,0), limits=c(76, 108), breaks=seq(76, 108, 4)) +
  geom_line(size=1) +
  geom_hline(yintercept=100) +
  geom_point(aes(x=tail(industrial$date, 1), y=tail(industrial$production, 1))) +
  geom_text(aes(x=tail(industrial$date, 1) + 60, y=tail(industrial$production, 1)), label=paste(format(tail(industrial$date, 1), format="%b"), "\n", sprintf("%.1f", tail(industrial$production, 1))), hjust=0, vjust=0.5)

unemployement <- read.csv("unemployement.csv", sep=";", dec=",", header=FALSE, col.names=c("date", "rate"))
unemployement$date <- as.Date(unemployement$date, "%d.%m.%Y")

unemployement_plot <- ggplot(unemployement, aes(x=date, y=rate, group=1)) +
  labs(title="Unemployment Rate\nPercent", x="", y="") +
  scale_x_date(expand = c(0,0), limits=as.Date(c("2009-01-01", "2015-01-01")), labels=date_format("%Y"), breaks=seq(as.Date("2009-06-01"), as.Date("2014-06-01"), by="year"), minor_breaks="year") +
  scale_y_continuous(expand = c(0,0), limits=c(6.5, 11.5), breaks=seq(6.5, 11.5)) +
  geom_line(size=1) +
  geom_point(aes(x=tail(unemployement$date, 1), y=tail(unemployement$rate, 1))) +
  geom_text(aes(x=tail(unemployement$date, 1) + 60, y=tail(unemployement$rate, 1)), label=paste(format(tail(unemployement$date, 1), format="%b"), "\n", sprintf("%.1f", tail(unemployement$rate, 1))), hjust=0, vjust=0.5)

price <- read.csv("price.csv", sep=";", dec=",", header=FALSE, col.names=c("date", "index"))
price$date <- as.Date(price$date, "%d.%m.%Y")

price_plot <- ggplot(price, aes(x=date, y=index, group=1)) +
  labs(title=" Consumer Price Index\n12-Month Percentage Change", x="", y="") +
  scale_x_date(expand = c(0,0), limits=as.Date(c("2009-01-01", "2015-01-01")), labels=date_format("%Y"), breaks=seq(as.Date("2009-06-01"), as.Date("2014-06-01"), by="year"), minor_breaks="year") +
  scale_y_continuous(expand = c(0,0), limits=c(-4, 6)) +
  geom_line(size=1) +
  geom_hline(yintercept=0) +
  geom_point(aes(x=tail(price$date, 1), y=tail(price$index, 1))) +
  geom_text(aes(x=tail(price$date, 1) + 60, y=tail(price$index, 1)), label=paste(format(tail(price$date, 1), format="%b"), "\n", sprintf("%.1f", tail(price$index, 1))), hjust=0, vjust=0.5, fill="white")

layOut(list(gross_plot, 1, 1), list(industrial_plot, 1, 2), list(unemployement_plot, 2, 1), list(price_plot, 2, 2))