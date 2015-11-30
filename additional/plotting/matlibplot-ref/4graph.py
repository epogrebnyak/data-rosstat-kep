from xls import get_file_path_in_project_directory
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import datetime
import numpy

csv_filename = "sa2_Dbase.csv"
csv_path = get_file_path_in_project_directory(csv_filename)
df = pd.read_csv(csv_path, index_col = 0)

z = df[["SA2_2","SA2_3","SA2_4","SA2_5"]]

# A dict with for each plot the axis and data:
to_plot = {
			"ts1": { "axis": [], "plot": df["SA2_2"] },
			"ts2": { "axis": [], "plot": df["SA2_3"] },
			"ts3": { "axis": [], "plot": df["SA2_4"] },
			"ts4": { "axis": [], "plot": df["SA2_5"] }
		  }

# For each plot:
for i in to_plot.keys() :
	# We compute the axis:
	ts_tmp = dict()
	axis = []
	for date in to_plot[i]["plot"].keys() :
		to_plot[i]["axis"].append(datetime.date(int(date.split("-")[0]), int(date.split("-")[1]), int(date.split("-")[2])))
		ts_tmp[date] = to_plot[i]["plot"][date]

	# to_plot[i]["axis"].append(datetime.date(2014, 10, 01))
	# to_plot[i]["axis"].append(datetime.date(2014, 11, 01))
	# to_plot[i]["axis"].append(datetime.date(2014, 12, 01))
	# to_plot[i]["axis"].append(datetime.date(2015, 01, 01))

	# to_plot[i]["plot"]["2014-10-01"] = numpy.nan
	# to_plot[i]["plot"]["2014-11-01"] = numpy.nan
	# to_plot[i]["plot"]["2014-12-01"] = numpy.nan
	# to_plot[i]["plot"]["2015-01-01"] = numpy.nan

	# And create a time serie:
	to_plot[i]["plot"] = pd.Series(ts_tmp, index=to_plot[i]["plot"].keys())

# The title:
matplotlib.rcParams.update({'font.size': 15})
plt.suptitle("US")
plt.suptitle("US Summary Indicators", x=.5, y=.98, ha="center", fontsize=15)

matplotlib.pyplot.grid(True)

# --------------- Start plotting ------------------

matplotlib.rc('xtick', labelsize=6)
matplotlib.rc('ytick', labelsize=6)
matplotlib.rcParams.update({'font.size': 9})

# ts1:
plt.subplot(2, 2, 1)
plt.plot(to_plot["ts1"]["axis"], to_plot["ts1"]["plot"])
plt.grid(b=True, which='both', color='0.65',linestyle=':')
plt.figtext(.125,.93,'Gross Domestic Product', fontsize=9, ha='left')
plt.figtext(.125,.91,"Four-quarter percentage change",fontsize=6,ha="left")
plt.xlim(datetime.date(2005,01,01), datetime.date(2016,12,01))
# The last value tag:
last_date = to_plot["ts1"]["axis"][len(to_plot["ts1"]["axis"]) - 1]
last_date_value = to_plot["ts1"]["plot"][last_date.strftime("%Y-%m-%d")]
plt.gca().scatter(last_date, last_date_value, s=10)
plt.annotate("Q1", xy = (last_date, last_date_value), xytext = (16, 5), textcoords = 'offset points', ha = 'right', va = 'center', fontsize = 7)
plt.annotate("3.0", xy = (last_date, last_date_value), xytext = (17, -5), textcoords = 'offset points', ha = 'right', va = 'center', fontsize = 7)

# ts2:
plt.subplot(222)
plt.plot(to_plot["ts2"]["axis"], to_plot["ts2"]["plot"])
plt.grid(b=True, which='both', color='0.65',linestyle=':')
plt.figtext(.55,.93,'Industrial Production', fontsize=9, ha='left')
plt.figtext(.55,.91,"Index, 1997=100",fontsize=6,ha="left")
plt.xlim(datetime.date(2005,01,01), datetime.date(2016,12,01))
# The last value tag:
last_date = to_plot["ts2"]["axis"][len(to_plot["ts2"]["axis"]) - 1]
last_date_value = to_plot["ts2"]["plot"][last_date.strftime("%Y-%m-%d")]
plt.gca().scatter(last_date, last_date_value, s=10)
plt.annotate("Apr", xy = (last_date, last_date_value), xytext = (20, 5), textcoords = 'offset points', ha = 'right', va = 'center', fontsize = 7)
plt.annotate("105.2", xy = (last_date, last_date_value), xytext = (25, -5), textcoords = 'offset points', ha = 'right', va = 'center', fontsize = 7)

# ts3:
plt.subplot(223)
plt.plot(to_plot["ts3"]["axis"], to_plot["ts3"]["plot"])
plt.grid(b=True, which='both', color='0.65',linestyle=':')
plt.figtext(.125,.49,'Unemployement Rate', fontsize=9, ha='left')
plt.figtext(.125,.47,"Percent",fontsize=6,ha="left")
plt.xlim(datetime.date(2005,01,01), datetime.date(2016,12,01))
# The last value tag:
last_date = to_plot["ts3"]["axis"][len(to_plot["ts3"]["axis"]) - 1]
last_date_value = to_plot["ts3"]["plot"][last_date.strftime("%Y-%m-%d")]
plt.gca().scatter(last_date, last_date_value, s=10)
plt.annotate("Apr", xy = (last_date, last_date_value), xytext = (20, 5), textcoords = 'offset points', ha = 'right', va = 'center', fontsize = 7)
plt.annotate("5.4", xy = (last_date, last_date_value), xytext = (18, -5), textcoords = 'offset points', ha = 'right', va = 'center', fontsize = 7)

# ts4:
plt.subplot(224)
plt.plot(to_plot["ts4"]["axis"], to_plot["ts4"]["plot"])
plt.grid(b=True, which='both', color='0.65',linestyle=':')
plt.figtext(.55,.49,'Consumer Price Index', fontsize=9, ha='left')
plt.figtext(.55,.47,"12-Month Percentage Change",fontsize=6,ha="left")
plt.xlim(datetime.date(2005,01,01), datetime.date(2016,12,01))
# The last valuee tag:
last_date = to_plot["ts4"]["axis"][len(to_plot["ts4"]["axis"]) - 1]
last_date_value = to_plot["ts4"]["plot"][last_date.strftime("%Y-%m-%d")]
plt.gca().scatter(last_date, last_date_value, s=10)
plt.annotate("Mar", xy = (last_date, last_date_value), xytext = (20, 5), textcoords = 'offset points', ha = 'right', va = 'center', fontsize = 7)
plt.annotate("-0.1", xy = (last_date, last_date_value), xytext = (20, -5), textcoords = 'offset points', ha = 'right', va = 'center', fontsize = 7)

# Uncomment to see matplotlib result:
# plt.show()

# And we save it in a pdf:
plt.savefig("foo.pdf", format="pdf")


#  - how can one save and reuse parameters of the graph, when 
#    changing appearance using controls in a pop-up window?
   
#  - last dot value label on graph 
