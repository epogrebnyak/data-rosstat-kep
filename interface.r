# TODO: clone interface_pandas.py


URL_DIR <- "https://raw.githubusercontent.com/epogrebnyak/rosstat-kep-data/master/output/"
DFA_URL <- paste0(URL_DIR, "data_annual.txt")
DFQ_URL <- paste0(URL_DIR, "data_quarter.txt")
DFM_URL <- paste0(URL_DIR, "data_monthly.txt")

dfa <- read.table(DFA_URL, sep = ",", header = TRUE, row.names = 1) # header=TRUE, sep="", na.strings="NA", dec=".", strip.white=TRUE)
dfq <- read.table(DFQ_URL, sep = ",", header = TRUE, row.names = 1) 
dfm <- read.table(DFM_URL, sep = ",", header = TRUE, row.names = 1)

#TODO: need set frequencies DFQ, DFM / convert to *ts* or *zoo* type

summary(dfa)
summary(dfq)
summary(dfm)