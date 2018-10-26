import copy
import sys
import math

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
	def __init__(self, len_sentence):
		# exist_rule: a set of entries that has been predicted in current column
		self.exist_rule = set()
		# exist_rule_next: a set of entries that has been predicted in next column
		self.exist_rule_next = set()
		self.chart = []
		# customer_index: [{X: [entries]},{},{},...] for each column, a list of entries with X after the dot
		self.customer_index = []
		self.S = {}
                self.length = len_sentence
                self.possible_entry = set()
                self.duplicate_dict = {}
                for i in xrange(self.length+1):
                    self.chart.append([])
                    self.customer_index.append({})


	def clear_set(self):
		self.exist_rule = self.exist_rule_next
		self.exist_rule_next = set()
		self.S = {}
                self.duplicate_dict = {}

	def create_column(self):
		self.chart.append([])
		self.customer_index.append({})

	def attach(self, column_idx, entry, current_count):
		#print(' attaching: '+ entry.print_entry())
		for idx, old_entry in enumerate(self.customer_index[entry.start][entry.Rule[0]]):
		    if column_idx != self.length and old_entry.dot < len(old_entry.Rule) - 1:
			after_dot = old_entry.Rule[old_entry.dot+1]
                        if after_dot not in self.possible_entry:
                            continue
                        #if len(P.get(after_dot, [])) > 0:
                        #    parent = P[after_dot][0]
                        #    if after_dot not in self.S.get(parent, []):
                        #        return
                    
    		    new_entry = copy.copy(old_entry)
		    new_entry.bkpointer1 = old_entry
	            new_entry.bkpointer2 = entry
                    new_entry.dot += 1
		    new_entry.weight = entry.weight + old_entry.weight
		    #print('# attaching new entry: '+ new_entry.print_entry())

                    flag = 1
                    for index in self.duplicate_dict.get((new_entry.start, new_entry.dot),[]):
                        if self.chart[column_idx][index].Rule == new_entry.Rule:
                            #print('# duplicate '+str(index) + ' '+str(current_count)+self.chart[column_idx][index].print_entry())
                            if self.chart[column_idx][index].weight <= new_entry.weight:
                                #print('# attaching duplicate with higher weight')
                                flag = 0
                            elif current_count <= index:
                                if column_idx != self.length and new_entry.dot < len(new_entry.Rule):
                                    after_dot = new_entry.Rule[new_entry.dot]
                                    self.customer_index[column_idx][after_dot].remove(self.chart[column_idx][index])
                                    self.customer_index[column_idx][after_dot].append(new_entry)
                                self.chart[column_idx][index] = new_entry
                                #print('# attaching duplicate not processed')
                                flag = 0
                            else:
                                if column_idx != self.length and new_entry.dot < len(new_entry.Rule):
                                    after_dot = new_entry.Rule[new_entry.dot]
                                    self.customer_index[column_idx][after_dot].remove(self.chart[column_idx][index])
                                self.chart[column_idx][index] = None
                                self.duplicate_dict[new_entry.start, new_entry.dot].remove(index)


                    #duplicate = self.check_duplicate(new_entry)
                    #if duplicate is not None:
                    #    continue
                    if flag == 1:
	    	        self.chart[column_idx].append(new_entry)
    		        #print('# attach add: '+ new_entry.print_entry())
		        if column_idx != self.length and old_entry.dot < len(old_entry.Rule) - 1:
                            after_dot = new_entry.Rule[new_entry.dot]
		            if after_dot not in self.customer_index[column_idx]:
	                        self.customer_index[column_idx][after_dot] = [new_entry]
	                    else:
	                        self.customer_index[column_idx][after_dot].append(new_entry)
                        if (new_entry.start, new_entry.dot) not in self.duplicate_dict:
                            self.duplicate_dict[new_entry.start, new_entry.dot] = [len(self.chart[column_idx])-1]
                        else:
                            self.duplicate_dict[new_entry.start, new_entry.dot].append(len(self.chart[column_idx])-1)
                    #else:
                    #    if column_idx < self.length:
                    #        return
    			#new_entry = copy.copy(old_entry)
		        #new_entry.bkpointer1 = old_entry
		        #new_entry.bkpointer2 = entry
    		        #new_entry.dot += 1
		        #new_entry.weight = entry.weight + old_entry.weight
	    	        #self.chart[column_idx].append(new_entry)
    		        #print('# attach add: '+ new_entry.print_entry())
                        

	def predict(self, column_idx, entry):
		after_dot = entry.Rule[entry.dot]
		#print('# predicting: '+ entry.print_entry())
                flag = 0
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
					#print('# predict add: '+ new_entry.print_entry())
                                        flag = 1
			self.exist_rule.add(after_dot)
                if flag == 0:
                    entry = None

	def scan(self, column_idx, entry, word):
		after_dot = entry.Rule[entry.dot]
		#print('# scaning: '+ entry.print_entry())
		if after_dot == word:
			#if column_idx+1 == len(self.chart):
			#	self.create_column()
			new_entry = copy.copy(entry)
			new_entry.dot += 1 
			new_entry.bkpointer1 = entry
			new_entry.bkpointer2 = word
			self.chart[column_idx+1].append(new_entry)
			#self.exist_rule_next.add(new_entry.Rule[entry.dot])
		        #print('# scaned: '+ new_entry.print_entry())
                        if new_entry.dot != len(new_entry.Rule):
                            new_after_dot = new_entry.Rule[new_entry.dot]
			    if new_after_dot not in self.customer_index[column_idx+1]:
				self.customer_index[column_idx+1][new_after_dot] = [new_entry]
			    else:
				self.customer_index[column_idx+1][new_after_dot].append(new_entry)


	def process_column(self, column_idx, word):
		#print('#processing column '+str(column_idx))
		self.S = get_S(word, [], {})
                self.possible_entry = set([item for sublist in self.S.viewvalues() for item in sublist])
                self.possible_entry.add(word)
                #print('# '+str(self.possible_entry))
		count = 0
		while count < len(self.chart[column_idx]):
			entry = self.chart[column_idx][count]
                        #if count % 1000 == 0:
                        #    print('#current entry in column '+str(column_idx)+': '+str(count)+'/'+str(len(self.chart[column_idx]))+entry.print_entry())
			if entry.dot == len(entry.Rule):
				if entry.Rule[0] != 'ROOT':
					self.attach(column_idx, entry, count)
			elif entry.Rule[entry.dot] not in NonTerminal:
				self.scan(column_idx, entry, word)
			else:
				self.predict(column_idx, entry)
			count += 1
                #print('# column '+str(column_idx))
                #for entry in self.chart[column_idx]:
                #    if entry is not None:
                #        print('# ' + entry.print_entry())
                #    else:
                #        print('# None')
                #for duplicate in self.duplicate_dict:
                #    print('# ' + str(duplicate))

	def process_last_column(self, column_idx):
		#print('#processing column '+str(column_idx))
		count = 0
		root_list = []
		while count < len(self.chart[column_idx]):
			entry = self.chart[column_idx][count]
			if entry.dot == len(entry.Rule):
				if entry.Rule[0] == 'ROOT':
					root_list.append(entry)
				else:
					self.attach(column_idx, entry, count)
			count += 1
                #for rule in root_list:
                    #print('# root_list: '+rule.print_entry())
		return root_list


#<<<<<<< HEAD
def read_grammar(gr_file):

    grammar = open(gr_file, 'r')
    #grammar = grammar.readlines()

    for line in grammar:
        if line != "\n":
            line_tokens = line.split()

            if (line_tokens[1],line_tokens[2]) not in R:
                R[line_tokens[1],line_tokens[2]] = [[-math.log(float(line_tokens[0]), 2), line_tokens[1:]]]
                NonTerminal.add(line_tokens[1])
            else:
                R[line_tokens[1],line_tokens[2]].append([-math.log(float(line_tokens[0]), 2), line_tokens[1:]])

            if line_tokens[2] not in P:
                P[line_tokens[2]] = [line_tokens[1]]
            else:
                P[line_tokens[2]].append(line_tokens[1])

            if line_tokens[1] == 'ROOT':
            	RootEntries.append(Entry(line_tokens[1:], -math.log(float(line_tokens[0]), 2)))

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
        pass
    elif isinstance(entry, basestring):
        out_string.append(entry)
    	#print ('# '+entry)
    else:
    	#print ('# '+entry.print_entry())
        bkpoint1 = entry.bkpointer1
        bkpoint2 = entry.bkpointer2
        out_string.append("("+ entry.Rule[0]+' ')

<<<<<<< HEAD
        print ('# '+entry.print_entry())
=======
>>>>>>> dcf7fe86aebe85aef3d02c16d242e8a7ae4335e2
    
        print_entry(bkpoint1.bkpointer2, out_string)
        print_entry(bkpoint2, out_string)
        out_string.append(")")
    return out_string

def parse(sentence,output):
	earley = Chart(len(sentence))
        #print('# len sentence:' +str(len(sentence)))
	#earley.create_column()
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
        if len(root_list) == 0:
            print('NONE')
        #    output.write('NONE\n')
        else:
	    min_entry = root_list[0]
	    for entry in root_list:
		    if entry.weight < min_entry.weight:
			    min_entry = entry
	    out_string = print_entry(min_entry, [])
            print ''.join(out_string)
            print min_entry.weight
	    #output.write("".join(out_string)+'\n')
            #output.write(str(min_entry.weight)+'\n')

def main(argv):
	R, P, RootEntries, NonTerminal = read_grammar(argv[1])
        #output = open("parse_result","w")
	output = None
        #print ('# '+str(len(R))+str(R))
	#print ('# '+str(len(P))+str(P))
	#print ('# '+str(RootEntries))
	#print ('# '+str(len(NonTerminal)))
        sentences = open(argv[2],"r")
        for sentence in sentences:
            tokens = sentence.strip().split()
            #print('# sentence: '+sentence)
            if len(tokens)>0:
	        parse(tokens,output)

        #output.close()

if __name__=="__main__":
	main(sys.argv)



