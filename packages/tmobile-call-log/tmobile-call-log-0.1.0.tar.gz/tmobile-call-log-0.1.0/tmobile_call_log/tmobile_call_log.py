import pandas as pd
import matplotlib.pyplot as plt
import os, shutil
from matplotlib import cm
import numpy as np


###############################################################################	
## Classes and Functions
###############################################################################	

class CallActivity:

	def __init__(self, data_dir, ignore_number=None):
		self.ignore_number = ignore_number
		self.data_dir = data_dir
		self.plots_dir = './plots/'+os.path.basename(os.path.dirname(self.data_dir))+'/'
		self.make_output_dir()
		self.df = self.concatAllFiles(self.data_dir)
		self.pie_chart_n = 9
		self.bar_chart_n = 9
		self.fig_dpi = 200
		
		
	def make_output_dir(self):
		if not os.path.exists(self.plots_dir):
			os.makedirs(self.plots_dir)

		
	def plot_pie(self, n=9):
		if len(self.df) == 0:
			print('Log is empty; add files to data directory.')
			return
		self.plotPieByCount(self.df, top=n)
		self.plotPieByDuration(self.df, top=n)
		
		
	def plot_bar(self, n=9):
		if len(self.df) == 0:
			print('Log is empty; add files to data directory.')
			return
		self.plotAllCountCharts(self.df, top=n)
		self.plotAllMinutesCharts(self.df, top=n)
		
		
	def getFileData(self, inputFileName):
		""" Get and parse data from one file; return as dataframe. """
		df = pd.read_csv(
			inputFileName,                              # file to read
			parse_dates=[['Date', 'Time']],             # combine date and time 
			skiprows=6,                                 # skip rows at the beginning
			)
		df = df[:-1]                                    # last row is not data; drop it
		if self.ignore_number:
			df = df[df['Number'] != self.ignore_number] # ignore calls to/from my google voice number
		df.drop(df.columns[[-1]],axis=1,inplace=True)   # the last column is empty; drop it
		return df

		
	def concatAllFiles(self, directory):
		""" Concatenate data from all files in directory; return as one dataframe. """
		frame = pd.DataFrame()
		list_ = []
		for fl in os.listdir(directory):
			if fl.endswith(".csv"):
				print(fl)
				df = self.getFileData(directory+fl)
				list_.append(df)
		frame = pd.concat(list_)
		return frame
		
		
	def plotCountChart(self, dataframe, chart_title='', min_call_time=1, top=None):
		""" Plot a single bar chart """
		dataframe = dataframe[dataframe['Minutes'] >= min_call_time]
		if top:
			ax = dataframe.groupby('Number').size().sort_values().tail(top).plot.bar();
			ax.set(xlabel="Phone number", ylabel="Number of calls", title=chart_title+' (top '+str(top)+' only)')
		else:
			ax = dataframe.groupby('Number').size().sort_values().plot.bar();
			ax.set(xlabel="Phone number", ylabel="Number of calls", title=chart_title)	
		plt.tight_layout()
		#plt.show()
		output_filename = self.plots_dir+chart_title+'_by_count.png'
		plt.savefig(output_filename,dpi=self.fig_dpi, bbox_inches='tight')
		plt.close()
		
		
	def plotAllCountCharts(self, dataframe, min_call_time=1, top=None):
		""" Plot all bar charts """
		df = dataframe
		incoming_calls = df[df['Destination']=='Incoming']
		outgoing_calls = df[df['Destination']!='Incoming']

		for subset, title in zip([df, incoming_calls,outgoing_calls],['All call types','Incoming calls','Outgoing calls']):
			self.plotCountChart(subset, chart_title=title, min_call_time=min_call_time, top=top)

			
	def plotMinutesChart(self, dataframe, chart_title='', min_call_time=1, top=None):
		""" Plot a single bar chart """
		dataframe = dataframe[dataframe['Minutes'] >= min_call_time]
		if top:
			ax = dataframe.groupby('Number').sum().sort_values(by='Minutes',ascending=True).tail(top).plot.bar();
			ax.set(xlabel="Phone number", ylabel="Minutes of talk time", title=chart_title+' (top '+str(top)+' only)')
			ax.legend_.remove()
		else:
			ax = dataframe.groupby('Number').sum().sort_values(by='Minutes',ascending=True).plot.bar();
			ax.set(xlabel="Phone number", ylabel="Minutes of talk time", title=chart_title)
			ax.legend_.remove()
		plt.tight_layout()
		#plt.show()
		output_filename = self.plots_dir+chart_title+'_by_min.png'
		plt.savefig(output_filename,dpi=self.fig_dpi, bbox_inches='tight')
		plt.close()

		
	def plotAllMinutesCharts(self, dataframe, min_call_time=1, top=None):
		""" Plot all bar charts """
		df = dataframe
		incoming_calls = df[df['Destination']=='Incoming']
		outgoing_calls = df[df['Destination']!='Incoming']

		for subset, title in zip([df, incoming_calls,outgoing_calls],['All call types','Incoming calls','Outgoing calls']):
			self.plotMinutesChart(subset, chart_title=title, min_call_time=min_call_time, top=top)

			
	def plotPieFromDF(self, df, chart_title=''):
		plt.gca().axis("equal")
		pie = plt.pie(df['Percent'], startangle=0, autopct='%1.0f%%', pctdistance=0.9, radius=1.2)
		labels=df['Number'].unique()
		plt.title(chart_title, weight='bold', size=14)
		plt.legend(pie[0],labels, bbox_to_anchor=(1,0.5), loc="center right", fontsize=10, 
				   bbox_transform=plt.gcf().transFigure)
		plt.subplots_adjust(left=0.0, bottom=0.1, right=0.85)
		#plt.show()
		output_filename = self.plots_dir+chart_title+'.png'
		plt.savefig(output_filename,dpi=self.fig_dpi, bbox_inches='tight')
		plt.close()

		
	def plotPieByCount(self, dataset, top=9):
		chart_title = 'Percent of call count'
		
		# NEW DataFrame for counts
		df = dataset.groupby('Number').size().reset_index()
		df.columns = ['Number','Count']
		total_count = df['Count'].sum()
		print(f'You made or received {total_count} calls')
		df['Percent'] = 100.0 * df['Count'] / total_count
		df = df.sort_values(by='Count', ascending=False)

		new_row = [('Other',df[top:]['Count'].sum(),df[top:]['Percent'].sum())]
		df = df.head(top).append(pd.DataFrame.from_records(new_row, columns=['Number','Count','Percent']))

		self.plotPieFromDF(df,chart_title=chart_title)
		
		
	def plotPieByDuration(self, dataset, top=9):
		chart_title = 'Percent of call time'

		# NEW DataFrame for minutes
		df = dataset.groupby('Number').sum().reset_index()
		df.columns = ['Number','Minutes']
		total_minutes = df['Minutes'].sum()
		print(f'You used {total_minutes} minutes of talk time')
		df['Percent'] = 100.0 * df['Minutes'] / total_minutes
		df = df.sort_values(by='Minutes', ascending=False)

		new_row = [('Other',df[top:]['Minutes'].sum(),df[top:]['Percent'].sum())]
		df = df.head(top).append(pd.DataFrame.from_records(new_row, columns=['Number','Minutes','Percent']))

		self.plotPieFromDF(df,chart_title=chart_title)

		
###############################################################################	
## Example script 
###############################################################################	

## Create log object to compile all data
# log = CallActivity(data_dir='./data/', ignore_number='(123) 555-1234')

## Plot bar charts
# log.plot_bar(n=15)

## Plot pie charts
# log.plot_pie(n=9)




		

	

