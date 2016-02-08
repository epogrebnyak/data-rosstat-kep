##
## R interface to 'rosstat-kep-data' dataset
## Imports 'ts' class timeseries from local files or web
## 
## To access data, use syntax like below
##
##    cpi = get_ts('m', 'CPI_rog')
##
##    # 'm' indictates monthly frequency (must be 'm', 'q' or 'a')
##    # 'CPI_rog' is time series code
##       
## For available time series codes see:
## https://raw.githubusercontent.com/epogrebnyak/rosstat-kep-data/master/output/varnames.md
##

FILENAMES = c(a = "data_annual.txt", 
              q = "data_quarter.txt",
              m = "data_monthly.txt")

# deltat: 1 if dfa, 1/4 if dfq, 1/12 if dfm  
DELTAS =    c(a = 1, 
              q = 1/4,
              m = 1/12)

URL_DIR = "https://raw.githubusercontent.com/epogrebnyak/rosstat-kep-data/master/output/"

#
# when using local files change LOCAL_FOLDER to path of folder containing
# data_annual.txt, data_quarter.txt and data_monthly.txt files
#
# may use file.path() to concat foolder name, e.g. file.path("c:","temp") will give "c:/temp"
#
LOCAL_FOLDER = "output" #default in 'kep' repository

get_path = function(freq){
  filename = FILENAMES[freq]
  local_path = file.path(LOCAL_FOLDER, filename)
  # look for local file first
  if (file.exists(local_path)) 
    return (local_path)
  else 
    # look at web if not found
    return (paste0(URL_DIR, filename))  
}

get_frame <- function (freq){
  path = get_path(freq)
  td = DELTAS[freq]
  # we assume dataframe always starts with 1999, must change later
  start.year <- 1999
  df  <- read.table(path, sep = ",", header = TRUE, row.names = 1)
  return(ts(data=df,start=start.year,deltat=td))
}

# time series holders
dfa = get_frame('a')
dfq = get_frame('q')
dfm = get_frame('m')

# check class conversion 
stopifnot(class(dfa) == c("mts", "ts", "matrix"))
stopifnot(class(dfq) == c("mts", "ts", "matrix"))
stopifnot(class(dfm) == c("mts", "ts", "matrix"))
stopifnot(class(dfa[,1]) == "ts")
stopifnot(class(dfq[,1]) == "ts")
stopifnot(class(dfm[,1]) == "ts")

# warpper to access time series
get_ts <- function (freq, tag)
{
  if (freq == 'm') {return (dfm[,tag])}
  else if (freq == 'q') {return (dfq[,tag])}
  else if (freq == 'a') {return (dfa[,tag])}
}

#Example:
RU_CPI <- get_ts('m', "CPI_rog")
USDRUB <- get_ts('m', "RUR_USD_eop")
GDP.nominal <- get_ts('q', "GDP_bln_rub")
housing <- get_ts('a', 'DWELL_mln_m2')

# For available time series codes see:
# https://raw.githubusercontent.com/epogrebnyak/rosstat-kep-data/master/output/varnames.md

# Development:
# - todo: we assume dataframe always starts with 1999 in get_frame(), must change later
# - may do: conversion to 'zoo' type, if necessary