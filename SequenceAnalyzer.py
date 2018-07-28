import pandas as pd 

class SequenceAnalyzer(object):
	"""
	This class determines the base from the highest signal intensity for each position. 
	This class calculates the %error for each run compared to ref sequence.
	Lines for exporting data are commented out. 

	Attributes:
		path: path to sequencing_data_biochem.csv files 
		reference: list of reference bases
		basecall: list of determined bases 

	"""

	def __init__(self, path):
		"""
		This is the initizalier for class SequenceAnalyzer.

		"""
		self.path = path
		self.reference = []
		self.basecall = []

	def import_csv(self):
		"""
		This method imports the sequencing_data_biochem.csv file.

		Returns
		-------
		pd.DataFrame
			imported data from the sequencing_data_biochem.csv file 

		"""
		return pd.read_csv(self.path)

	def no_max(self, row):
		"""
		This method determines if there is no maximum value which is used to determine if basecall is 'N'.

		Parameters
		----------
		row: pd.Series
			current row in sequence 

		Returns
		-------
		Boolean:
			True if no Max
			False if Max 


		"""
		return len(pd.unique(row)) == 1

	def change_column_titles(self, df, base_order):
		"""
		This method changes the column titles of the DataFrame to bases in selected positions

		Parameters
		----------
		df: pd.DataFrame
			imported DataFrame 
		base_order: List
			list of bases that will replace the column titles in the DataFrame

		"""
		new_cols = base_order
		df.rename(columns=dict(zip(df.columns[[1,2,3,4,7,8,9,10]], new_cols)),inplace=True)

	def basecall_sequence(self, df, start_column, end_column):
		"""
		This method determines the correct base for each position from the highest intensity. 
		If there is no max for the given position then 'N' is appended to the basecall attribute list. 
		The max value in the row is found then the associated column title is appended to the basecall attribute list. 

		Parameters
		----------
		df: pd.DataFrame
			imported DataFrame
		start_column: int
			start column for intensity readings
		end_column: int
			end column of intensity readings + 1 

		Returns
		-------
		list:
			list of basecalls

		"""
		self.basecall = []
		for index, row in df.iterrows():
			if self.no_max(row[start_column:end_column]) == True:
				self.basecall.append(('N'))

			else:
				self.basecall.append(row[start_column:end_column].idxmax(axis=1))
		return self.basecall
		
	def reference_sequence(self, df, reference_column):
		"""
		This method appends the bases in the reference sequence column to the reference attribute list.

		Parameters
		----------
		df: pd.DataFrame
			imported Data Frame
		reference_column: int
			column for reference sequence

		Returns
		-------
		list:
			list of reference bases 

		"""
		self.reference = []
		for index, row in df.iterrows():
			self.reference.append(row[reference_column])
		return self.reference

	def calculate_error(self):
		"""
		This method calculates the error rate between the basecalls and the reference sequence.

		Returns
		-------
		int:
			%error of basecall sequence 

		"""
		count = 0
		sequence_length = len(self.reference)

		for index, data in enumerate(self.reference):
			if self.reference[index] == self.basecall[index]:
				count+=1
		return abs(((count-sequence_length)/sequence_length)) * 100

# The main function uses nested for loops to loop through each file and each run within the file. 
# Within the outerloop, a SequenceAnalyzer object is created, the csv is imported, and the column titles are changed.
# In the innerloop, the positions for the columns are updated and the methods to generate basecall and reference lists are called.
# Finally the error is calculated the ouputed to the console.
# There are also lines that are used to export the data. They are commented out. 

if __name__=="__main__":

	base_orders = [['A','C','G','T','A', 'C', 'G', 'T'], ['C', 'G', 'T', 'A', 'C', 'G', 'T', 'A']]

	# export_files = [
	# '/Users/rj/Downloads/analysis_exercise/biochem1_output.xlsx',
	# '/Users/rj/Downloads/analysis_exercise/biochem2_output.xlsx'
	# ]

	files = [
	"/Users/rj/Downloads/analysis_exercise/sequencing_data_biochem1.csv", 
	"/Users/rj/Downloads/analysis_exercise/sequencing_data_biochem2.csv"
	]


	RUN1 = {
		'start_column': 1, 
		'end_column': 5,
		'ref_column': 0, 
		'sheet_title' : 'Run_1'
	}

	RUN2 = {
		'start_column':7, 
		'end_column': 11, 
		'ref_column': 6, 
		'sheet_title' : 'Run_2'
	}

	runs = [RUN1, RUN2]

	for index, data in enumerate(files):
		excel = SequenceAnalyzer(files[index])
		data = excel.import_csv()
		order = base_orders[index]
		excel.change_column_titles(data, order)
		# writer = pd.ExcelWriter(export_files[index])

		for run in runs:
			basecall = excel.basecall_sequence(data, run['start_column'], run['end_column'])
			reference = excel.reference_sequence(data, run['ref_column'])

			# output = {
			# 	'basecall': basecall,
			# 	'reference': reference
			# }

			# export_df = pd.DataFrame(output)

			# export_df.to_excel(writer, sheet_name=run['sheet_title'])
			print(excel.calculate_error(),'%')
		# writer.close()
	