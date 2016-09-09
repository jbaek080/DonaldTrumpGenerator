import random
import sys
from flask import request
from flask import Flask
from flask import render_template
app = Flask(__name__)
f = "corpus.txt"

class Ngram:
    def __init__(self, words, next_ngrams=None):
        self.words = words
        #next_ngrams is a dictionary of {Ngram: occurrence} pairs
        if next_ngrams:
            self.add_next_ngrams(next_ngrams)
        else:
            self.next_ngrams = {}
    
    def __getitem__(self, i):
        return self.words[i]

    def add_next_ngram(self, next_ngram):
        self.next_ngrams[next_ngram] = self.next_ngrams.get(next_ngram, 0) + 1
        self.normalize(self.next_ngrams)

    def add_next_ngrams(self, next_ngrams):
        self.next_ngrams = ngrams
        self.normalize(self.next_ngrams)

    def normalize(self, ngrams):
        divisor = sum(ngrams.values())
        previous_value = 0
        for key in ngrams:
            ngrams[key] = (ngrams[key] / divisor) + previous_value 
            previous_value = ngrams[key]

    def get_next(self):
        r = random.random()
        for ngram in self.next_ngrams:
            if r < self.next_ngrams[ngram]:
                return ngram

class MarkovChain:
    def __init__(self, n, f):
        self.corpus = self.preprocess(f)[:3000]
        self.ngrams = self.make_ngrams(n, self.corpus)

    def preprocess(self, f):
        corpus = []
        with open(f, errors='ignore') as o:
            flag = 1
            for line in o:
                if "Share on Facebook" in line:
                    flag = 1 - flag
                    continue
                if flag:
                    continue
                else:
                    corpus += line.strip().split(" ")
        return corpus

    def make_ngrams(self, n, corpus):
        lst = []
        for i in range(len(corpus) - 2):
            ngram_words = [corpus[i], corpus[i+1], corpus[i+2]]
            ngram = Ngram(ngram_words)
            lst.append(ngram)
        self.add_next_ngrams(lst)
        return lst

    def add_next_ngrams(self, ngrams):
        i = 0
        for ngram in ngrams:
            last_word = ngram[len(ngram.words) - 1] 
            for other_ngram in ngrams:
                first_word = other_ngram[0]
                if last_word == first_word:
                    ngram.add_next_ngram(other_ngram)
            i += 1
            if i % 1000 == 0:
                print("progress: %f"%(100 * i/len(ngrams)))

    def generate(self, n):
        count = 0
        i = random.randint(0, len(self.ngrams))
        start = self.ngrams[i]
        string = ""
        for word in start.words:
            string += word + " "
        while count < n:
            next_ngram = start.get_next()
            for word in next_ngram.words[:len(next_ngram.words) - 1]:
                string += word + " "
                if "." in word:
                    string += "\r\n"
            count += 1
            start = next_ngram
        return string[string.index(". ") + 1:]
#        with open("out.txt", "w") as o:
#            o.write(string)

chain = MarkovChain(3, f)
string = chain.generate(1000)
@app.route("/")
@app.route("/<string>", methods=['GET'])
def f(string=string):
    if request.method == 'GET':
        string = chain.generate(1000)
        return render_template("donald.html", string=string)
