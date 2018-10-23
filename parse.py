import copy

class Entry:
	def __init__(Rule, weight, start=0, dot=1, bkpointer1=None, bkpointer2=None):
		self.weight = weight
		self.start = start
		self.dot = dot
		self.Rule = Rule
		self.bkpointer1 = bkpointer1
		self.bkpointer2 = bkpointer2

class Chart:
	def __init__:
		# exist_rule: a set of entries that has been predicted in current column
		self.exist_rule = set()
		# exist_rule_next: a set of entries that has been predicted in next column
		self.exist_rule_next = set()
		self.chart = []
		# customer_index: [{X: entries},{},{},...] for each column, a list of entries with X after the dot
		self.customer_index = []
		self.S = {}

	def clear_set():
		self.exist_rule = self.exist_rule_next
		self.exist_rule_next = set()
		self.S = {}

	def create_column():
		self.chart.append([])
		self.customer_index.append([])

	def attach(column_idx, entry):
		self.chart[column_idx].append(copy.copy(self.customer_index[entry.start][entry.Rule[0]]))
		self.chart[column_idx][-1].bkpointer1 = self.customer_index[entry.start][entry.Rule[0]]
		self.chart[column_idx][-1].bkpointer2 = entry
		self.chart[column_idx][-1].dot += 1
		self.weight = entry.weight + self.customer_index[entry.start][entry.Rule[0]].weight
		self.exist_rule.add(self.chart[column_idx][-1].Rule[dot])

	def predict(column_idx, entry):
		after_dot = entry.Rule[dot]
		if after_dot not in self.exist_rule:
			for non_terminal in self.S[after_dot]:
				for rule in R[after_dot, non_terminal]:
					new_entry = Entry(rule[1], rule[0], start=column_idx)
					self.chart[column_idx].append(new_entry)
			self.exist_rule.add(after_dot)

	def scan(column_idx, entry, word):
		after_dot = entry.Rule[dot]
		if after_dot == word:
			self.create_column()
			new_entry = copy.copy(entry)
			new_entry.dot += 1 
			new_entry.bkpointer1 = entry
			new_entry.bkpointer2 = None
			self.chart[column_idx+1].append(new_entry)
			self.exist_rule.add(new_entry.Rule[dot])

	def process_column(column_idx, word):
		self.S = get_S(word)
		count = 0
		while count < len(self.chart[colunm_idx]):
			entry = self.chart[i][count]
			if entry.dot == len(entry.Rule)-1:
				self.attach(column_idx, entry)
			elif entry.Rule[dot] not in R.viewkeys():
				self.scan(column_idx, entry, word)
			else:
				self.predict(column_idx, entry)
			count += 1

	def process_last_column(column_idx):
		count = 0
		root_list = []
		while count < len(self.chart[colunm_idx]):
			entry = self.chart[i][count]
			if entry.dot == len(entry.Rule):
				if entry.Rule[0] == 'ROOT':
					root_list.append(entry)
				else:
					self.attach(column_idx, entry)
			count += 1
		return root_list


def read_grammar(file):
	return R, P

def get_S(word):

def print_entry(rule):
	recursive print_entry
	print

def parse(sentence):
	chart = Chart()
	for i in xrange(len(sentence)):
		chart.process_column(i, sentence[i])
		chart.clear_set()
	root_list = chart.process_last_column(len(sentence))
	min_entry = root_list[0]
	for entry in root_list:
		if entry.weight < min_entry.weight:
			min_entry = entry
	print_entry(min_entry)



