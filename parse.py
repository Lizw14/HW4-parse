import copy

R={}
P={}
RootEntries=[]
NonTerminal=set()

class Entry:
	def __init__(self, Rule, weight, start=0, dot=1, bkpointer1=None, bkpointer2=None):
		self.weight = weight
		self.start = start
		self.dot = dot
		self.Rule = Rule
		self.bkpointer1 = bkpointer1
		self.bkpointer2 = bkpointer2

	def print_entry(self):
		return str(self.Rule) +' '+ str(self.weight) +' '+ str(self.start) +' '+ str(self.dot)

class Chart:
	def __init__(self):
		# exist_rule: a set of entries that has been predicted in current column
		self.exist_rule = set()
		# exist_rule_next: a set of entries that has been predicted in next column
		self.exist_rule_next = set()
		self.chart = []
		# customer_index: [{X: [entries]},{},{},...] for each column, a list of entries with X after the dot
		self.customer_index = []
		self.S = {}


	def clear_set(self):
		self.exist_rule = self.exist_rule_next
		self.exist_rule_next = set()
		self.S = {}

	def create_column(self):
		self.chart.append([])
		self.customer_index.append({})

	def attach(self, column_idx, entry):
		print('attaching: '+ entry.print_entry())
		for idx, old_entry in enumerate(self.customer_index[entry.start][entry.Rule[0]]):
			new_entry = copy.copy(old_entry)
			new_entry.bkpointer1 = old_entry
			new_entry.bkpointer2 = entry
			new_entry.dot += 1
			new_entry.weight = entry.weight + old_entry.weight
			self.chart[column_idx].append(new_entry)
			print('attach add: '+ new_entry.print_entry())
			if new_entry.dot < len(new_entry.Rule):
				after_dot = new_entry.Rule[new_entry.dot]
				if after_dot not in self.customer_index[column_idx]:
					self.customer_index[column_idx][after_dot] = [new_entry]
				else:
					self.customer_index[column_idx][after_dot].append(new_entry)

	def predict(self, column_idx, entry):
		after_dot = entry.Rule[entry.dot]
		print('predicting: '+ entry.print_entry())
		if after_dot not in self.exist_rule:
			for non_terminal in self.S.get(after_dot, []):
				for rule in R.get((after_dot, non_terminal), []):
					new_entry = Entry(rule[1], rule[0], start=column_idx)
					self.chart[column_idx].append(new_entry)
					new_after_dot = new_entry.Rule[1]
					if new_after_dot not in self.customer_index[column_idx]:
						self.customer_index[column_idx][new_after_dot] = [new_entry]
					else:
						self.customer_index[column_idx][new_after_dot].append(new_entry)
					print('predict add: '+ new_entry.print_entry())
			self.exist_rule.add(after_dot)

	def scan(self, column_idx, entry, word):
		after_dot = entry.Rule[entry.dot]
		if after_dot == word:
			if column_idx+1 == len(self.chart):
				self.create_column()
			new_entry = copy.copy(entry)
			new_entry.dot += 1 
			new_entry.bkpointer1 = entry
			new_entry.bkpointer2 = None
			self.chart[column_idx+1].append(new_entry)
			#self.exist_rule_next.add(new_entry.Rule[entry.dot])
			if after_dot not in self.customer_index[column_idx+1]:
				self.customer_index[column_idx+1][after_dot] = [new_entry]
			else:
				self.customer_index[column_idx+1][after_dot].append(new_entry)
		print('scan: '+ new_entry.print_entry())


	def process_column(self, column_idx, word):
		print('processing column '+str(column_idx))
		self.S = get_S(word, [], {})
		count = 0
		while count < len(self.chart[column_idx]):
			print('current entry: '+str(count)+'/'+str(len(self.chart[column_idx])))
			entry = self.chart[column_idx][count]
			if entry.dot == len(entry.Rule):
				if entry.Rule[0] != 'ROOT':
					self.attach(column_idx, entry)
			elif entry.Rule[entry.dot] not in NonTerminal:
				self.scan(column_idx, entry, word)
			else:
				self.predict(column_idx, entry)
			count += 1

	def process_last_column(self, column_idx):
		count = 0
		root_list = []
		while count < len(self.chart[column_idx]):
			entry = self.chart[column_idx][count]
			if entry.dot == len(entry.Rule):
				if entry.Rule[0] == 'ROOT':
					root_list.append(entry)
				else:
					self.attach(column_idx, entry)
			count += 1
		return root_list


#<<<<<<< HEAD
def read_grammar(gr_file):

    grammar = open(gr_file, 'r')
    #grammar = grammar.readlines()

    for line in grammar:
        if line != "\n":
            line_tokens = line.split()

            if (line_tokens[1],line_tokens[2]) not in R:
                R[line_tokens[1],line_tokens[2]] = [[float(line_tokens[0]), line_tokens[1:]]]
                NonTerminal.add(line_tokens[1])
            else:
                R[line_tokens[1],line_tokens[2]].append([float(line_tokens[0]), line_tokens[1:]])

            if line_tokens[2] not in P:
                P[line_tokens[2]] = [line_tokens[1]]
            else:
                P[line_tokens[2]].append(line_tokens[1])

            if line_tokens[1] == 'ROOT':
            	RootEntries.append(Entry(line_tokens[1:], float(line_tokens[0])))

    grammar.close()
    return R, P, RootEntries, NonTerminal

def get_S(child, childlist, Sj):
    childlist.append(child)
    if child in P:
        left_parents = P[child]

        if len(left_parents) > 0:
            for parent in left_parents:
                if parent not in Sj:
                    Sj[parent] = childlist

                    Sj = get_S(parent,childlist,Sj)
                else:
                    pass
    return Sj



def print_entry(entry, out_string):

    if entry == None:
        return ''
    bkpoint1 = entry.bkpointer1
    bkpoint2 = entry.bkpointer2
    out_string += ("("+ entry.Rule[0])

    print (entry.print_entry())
    
    out_string += print_entry(bkpoint1.bkpointer2, out_string)
    out_string += print_entry(bkpoint2, out_string)
    out_string += ')'
    return out_string

def parse(sentence):
	earley = Chart()
	earley.create_column()
	earley.chart[0].extend(RootEntries)
	for entry in RootEntries:
		after_dot = entry.Rule[1]
		if after_dot not in earley.customer_index[0]:
			earley.customer_index[0][after_dot] = [entry]
		else:
			earley.customer_index[0][after_dot].append(entry)
	for i in xrange(len(sentence)):
		earley.process_column(i, sentence[i])
		earley.clear_set()
	root_list = earley.process_last_column(len(sentence))
	min_entry = root_list[0]
	for entry in root_list:
		if entry.weight < min_entry.weight:
			min_entry = entry
	out_string = print_entry(min_entry, '')
	print out_string

def main():
	R, P, RootEntries, NonTerminal = read_grammar('/Users/lizw/Downloads/hw-parse/papa.gr')
	print R
	print P
	print RootEntries
	print NonTerminal
	sentence = 'Papa ate the caviar with a spoon'.strip().split()
	parse(sentence)

if __name__=="__main__":
	main()



