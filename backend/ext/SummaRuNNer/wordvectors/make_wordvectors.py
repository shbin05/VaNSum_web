# coding: utf-8
import nltk
import codecs
import argparse
import numpy as np
import gensim
from itertools import chain

# arguments setting
parser = argparse.ArgumentParser()
parser.add_argument('--vector_size', type=int, default=100,
                    help='the size of a word vector')
parser.add_argument('--window_size', type=int, default=5,
                    help='the maximum distance between the current and predicted word within a sentence.')
parser.add_argument('--vocab_size', type=int, default=10000,
                    help='the maximum vocabulary size')
parser.add_argument('--num_negative', type=int, default=5,
                    help='the int for negative specifies how many “noise words” should be drawn')
args = parser.parse_args()

vector_size = args.vector_size
window_size = args.window_size
vocab_size = args.vocab_size
num_negative = args.num_negative


def get_min_count(sents):
    '''
    Args:
      sents: A list of lists. E.g., [["I", "am", "a", "boy", "."], ["You", "are", "a", "girl", "."]]

    Returns:
      min_count: A uint. Should be set as the parameter value of word2vec `min_count`.   
    '''
    global vocab_size

    fdist = nltk.FreqDist(chain.from_iterable(sents))
    # the count of the the top-kth word
    min_count = fdist.most_common(vocab_size)[-1][1]

    return min_count


def make_wordvectors():
    # In case you have difficulties installing gensim, you need to consider installing conda.
    
    # import cPickle as pickle

    print("Making sentences as list...")
    sents = []
    with codecs.open(f'data/ko.txt', 'r', 'utf-8') as fin:
        while 1:
            line = fin.readline()
            if not line:
                break

            words = line.split()
            sents.append(words)

    print("Making word vectors...")
    min_count = get_min_count(sents)
    model = gensim.models.Word2Vec(sents, vector_size=vector_size, min_count=min_count,
                                   negative=num_negative,
                                   window=window_size)

    model.save(f'data/ko.bin')

    # Save to file
    with codecs.open(f'data/ko.tsv', 'w', 'utf-8') as fout:
        for i, word in enumerate(model.wv.index_to_key):
            fout.write(u"{}\t{}\t{}\n".format(str(i), word.encode('utf8').decode('utf8'),
                                              np.array_str(model.wv[word])
                                              ))


if __name__ == "__main__":
    make_wordvectors()

    print("Done")
