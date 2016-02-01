# TODO: clone interface_pandas.py


URL_DIR <- "https://raw.githubusercontent.com/epogrebnyak/rosstat-kep-data/master/output/"
DFA_URL <- URL_DIR +"data_annual.txt"
DFQ_URL <- URL_DIR +"data_quarter.txt"
DFM_URL <- URL_DIR +"data_monthly.txt"

dfa <- read.table(DFA_URL) # header=TRUE, sep="", na.strings="NA", dec=".", strip.white=TRUE)
dfq <- read.table(DFQ_URL) 
dfm <- read.table(DFM_URL) 

#need set frequencies DFQ, DFM

summary(DFA)
