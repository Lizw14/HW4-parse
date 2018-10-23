check_duplicate()

R: (NP, Det, N)

class Entry:
	def __init__(weight, start, dot, R, bkpointer1=None, bkpointer2=None):
		self.weight = weight
		self.start = start
		self.dot = dot
		self.R = R
		self.bkpointer1 = bkpointer1
		self.bkpointer2 = bkpointer2

class Chart:
	def __init__:
		self.exist_rule = set()
		self.exist_rule_next = set()
		self.chart = []
		self.customer_index = []

	def clear_set():
		self.exist_rule = self.exist_rule_next
		self.exist_rule_next = set()

	def create_column():
		self.chart.append([])
		self.customer_index.append([])

	def attach(column_idx, entry):
		self.chart[column_idx].append(shutil.copy(self.customer_index[entry.start][R[0]]))
		self.chart[column_idx][-1].bkpointer1 = self.customer_index[entry.start][R[0]]
		self.chart[column_idx][-1].bkpointer2 = entry
		self.weight = entry.weight + self.customer_index[entry.start][R[0]].weight

	def predict(column_idx, entry):
		after_dot = R[dot]
		if after_dot not in self.exist_rule:
			for non_terminal in S[column_idx][after_dot]:
				for rule in R[after_dot][non_terminal]:
					self.chart[column_idx].append(rule)
			self.exist_rule.add(after_dot)

	def scan(column_idx, entry, word):
		after_dot = R[dot]
		if after_dot == word:
			self.create_column()
			new_entry = shutil.copy(entry)
			new_entry.dot +=1 
			new_entry.bkpointer1 = entry
			new_entry.bkpointer2 = None
			self.chart[column_idx+1].append(new_entry)


def read_grammar(gr_file):
    R = {}
    P = {}

    grammar = open(gr_file)
    grammar = grammar.readlines()

    for line in grammar:
        if line != "\n":
            line_tokens = line.split()

            if (line_tokens[1],line_tokens[2]) not in R:
                R[line_tokens[1],line_tokens[2]] = [line_tokens]
            else:
                R[line_tokens[1],line_tokens[2]].append(line_tokens)

            if line_tokens[2] not in P:
                p[line_tokens[2]] = [line_tokens[1]]
            else:
                p[line_tokens[2]].append(line_tokens[1])
    return R,P

def get_S(child,childlist,Sj):
    childlist.append(child)
    left_parents = P[child]
    
    for parent in left_parents:
        Sj[parent] = childlist
        Sj = get_S(parent,childlist,Sj)
    return Sj

def print_entry(entry):
    bkpoint1 = entry.bkpointer1
    bkpoint2 = entry.bkpointer2

    if entry == None:
        pass
    print("("+ entry.R[0])
    
    print_entry(bkpoinit1.bkpointer2)
    print_entry(bkpoint2)
    print(")")

def parse():
	chart = [[],[],[],[], ...]
	for i in xrange(len(sentence)):
		S = get_S(sentence[i])
		count = 0
		while 1
			count = count+1
			if count < len(chart[i]):
				rule = chart[i][count]
				if dot is at last postion:
					attach(rule)
				elif rule contains terminal:
					scan(rule)
				else predict(rule)
			else count = len(chart[i])
				break
	i = i+1
	count = 0
	count = count+1
	while 1
		if count < len(chart[i]):
			rule = chart[i][count]
			if dot is at last postion:
				attach(rule)
			elif rule contains terminal:
				scan(rule)
			else predict(rule)
		else count = len(chart[i])
			break
	final_rule = find(ROOT)
	print_entry(final_rule)



