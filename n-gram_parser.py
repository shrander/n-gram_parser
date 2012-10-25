#!/usr/bin/python
# Nick Hnatiw
#  Home work assignment 1
#  Natural Language Processing
#  S. Nirenburg

import sys
import operator
import random

class parser:
    #def __init__(self, data):
        # not happy about this, but a more elegant solution will take too long to implement
        # appData instance
        #self.data = data
        
    def text_to_list(self, fHandle, n):
        """
        create tokenized word list - word list will consist of a list of n-grams
        fHandle - file handler for the text corpus to be tokenized
        n - n-gram depth
        """
        wordlist = fHandle.read().split()
        i=0
        nGramList = []
        while(i<len(wordlist)):
            tlist = []
            j=0
            while(i+j < len(wordlist) and j<n):
                tlist.append(wordlist[i+j])
                j+=1
            if len(tlist) == n:
                nGramList.append(tuple(tlist))
            i+=1
        return nGramList
                    
class appData:
    def __init__(self):
        #file handler for corpus
        self.f = None
        # depth of ngram
        self.n=1
        # list of ngrams
        self.nGramList = None
        # file handler for word list file
        self.fwl = None
        # word list to check for nGram
        self.wl = []
        
class app:
    def __init__(self):
        # size of the n-gram (default: unigram)
        self.n = 1
        # path to the corpus file
        self.corpus = ''
        # number of entries in the frequency distribution table
        self.freqLength = 50
        # file name of the word list
        self.list = ''
        # flag for Good Turing
        self.goodTuring = False
        # number of random words to generate
        self.rand = 0
        # histogram of bigrams
        self.hist = {}
        
        self.data = appData()
        self.parse = parser()
        

    def usage(self):
        print 'USAGE: hw1-hnatiw.py [options]'
        print '\nThis program takes in a flat txt file corpus and creates a'
        print '   frequency distribution table.'
        print '     -c corpus          File that contains corpus to be scanned'
        print '     -n n-gram size     Depth of the ngram (default: 1=unigram, 2=bigram, etc)'
        #print '     -f [number]        how large of frequency distribution to print out (default: 10)' 
        print '     -l [file]          word list for the frequency distribution. Not specifying a word list'
        print '                         will display the top ten most nGrams'
        print '     -r [number]        create random sentences. [number] is the number of words generated'
        print '                         use the \'-n\' option to modify what depth of ngram to use.'
        print '     -G                 Adds Good-Turing smoothing to the frequency distribution' 
        print '\n'
        sys.exit(0)
        
    def parseArgs(self, args):
        i=0
        try:
            while( i<=len(args)-1 ):
                if args[i] == '-c' or args[i] == '--corpus':
                    i+=1
                    self.corpus = args[i]
                elif args[i] == '-n' or args[i] == '--number':
                    i+=1
                    self.n = int(args[i])
                elif args[i] == '-f' or args[i] == '--freq':
                    i+=1
                    self.freqLength = int(args[i])
                elif args[i] == '-l' or args[i] == '--list':
                    i+=1
                    self.list = args[i]
                elif args[i] == '-G' or args[i] == '--Good':
                    self.goodTuring = True
                elif args[i] == '-r':
                    i+=1
                    self.rand = int(args[i])
                else:
                    print 'ERROR: '+' '.join(sys.argv) + '\n'
                    self.usage()
                i+=1
        except:
            self.usage()
        print '\nCorpus: ' + self.corpus
        print 'n-Gram depth: ' + str(self.n)
    
    def print_top_n_most_ngrams(self, hist):
        """
        creates a table of the most used ngrams in the corpus
        """
        sortedHist = sorted(hist.iteritems(), key=operator.itemgetter(1), reverse=True)
        for each in range(self.freqLength):
            for j in sortedHist[each][0]:
                print '%-10s' % j,
            print '%5d' % sortedHist[each][1]
    
    def get_total_ngram_count(self, hist):
        total = 0 # all ngrams in corpus
        for each in hist.iteritems():
            total += each[1]
        return total
        
    def print_ngram_hist(self, hist):
        """
        creates a histogram table with the data.wl as the labels for the histogram
        hist - dictionary with histogram information
        """
        # build header
        print '%10s' % '',
        for each in self.data.wl:
            print '%10s' % each,
        print ''
        
        #build left column labels and rows
        for i in self.data.wl:
            print '%-10s' % i,
            
            if not self.goodTuring:
                # print the counts for each word pair
                for j in self.data.wl:
                    if (i,j) in hist:
                        print '%10d' % hist[(i,j)],
                    else:
                        print '%10d' % 0,
                print ''
            else:
                 # print the Good Turing smoothed counts for each word pair
                for j in self.data.wl:
                    if (i,j) in hist:
                        print '%.8f' % (float(hist[(i,j)])/self.get_total_ngram_count(hist)),
                    else:
                        # Good Turing smoothing
                        ngram_sum = 0
                        for each in hist.iteritems():
                            if each[0][0] == i and each[1] == 1:
                                ngram_sum += each[1]
                        print '%.8f' % (float(ngram_sum)/self.get_total_ngram_count(hist)),
                print ''

    def printFreqDistTable(self):        
        """
        creates the frequency distribution table of nGrams
        if a word list is given the word list will be used to create the table
        otherwise the top 50 most used nGrams will displayed
        """
        for each in self.data.nGramList:
            self.hist[each] = self.data.nGramList.count(each)
            
        # if building random senteces do not print the histogram
        # TODO: this needs to be reworked.  it is sloppy
        if self.rand:
            return
        
        # Print the top most used ngrams unless a word list file is given.  If a word list file is given, priven the histogram with the words given.
        if self.data.n == 1 or self.data.fwl == None:
            self.print_top_n_most_ngrams(self.hist)
        else:
            self.print_ngram_hist(self.hist)
        print ''
            	
    def gen_random_sent(self):   
        """
        Creates random sentences from the nGrams denoted by the user
        """ 
        sentence = [] 
        self.data.f.seek(0)
        list = self.data.f.read().split()
        
        # unigram is just a random pool of self.rand samples
        if self.data.n == 1:
            sentence = random.sample(list, self.rand)
            
        # Bigrams are the only other nGrams handled by this generator
        else:
            sentence.append(random.choice(list)) # a random first word is chosen
            i=0
            while(i<self.rand): # choose self.rand number of words
                t_list = [] #  temperary list to generate all potential candidates with the given word being the previous word in the sentence
                for each in self.data.nGramList: # create a list of bigrams with the first word, in the bigram, being the last word chosen
                    if each[0] == sentence[-1]:
                        t_list.append(each)
                sentence.append(random.choice(t_list)[-1]) # choose a weighted random word from the generated list of possiblities
                i+=1
            
        print ' '.join(sentence)
        print ''
            
    def initData(self):
        """
        initialize some data structures and opens files given by the user
        """
        try:
            self.data.f = open(self.corpus,'r')
            self.data.n = self.n
            if self.list != '':
                self.data.fwl = open(self.list, 'r')
                self.data.wl = self.data.fwl.read().split()
        except IOError as e:
            print e
            sys.exit(1)

    def main(self, args):
        if len(args)==0 or (args[0] == 'python' and len(args) == 2):
            self.usage()
        self.parseArgs(args)
        self.initData()        
        self.data.nGramList = self.parse.text_to_list(self.data.f, self.data.n)
        print 'Building Frequency Distribution Tables\n'
        self.printFreqDistTable()
        if self.rand > 0:
            self.gen_random_sent()



if __name__ == '__main__':
    try:
        a = app()
        a.main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit(0)
