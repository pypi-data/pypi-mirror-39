import numpy as np
import pyLDAvis
from biterm.btm import BTM
from sklearn.feature_extraction.text import CountVectorizer
import math
from biterm.utility import *

if __name__ == "__main__":

    # data from https://github.com/jacoxu/StackOverflow
    texts = open('./biterm/data/title_StackOverflow.txt').readlines()

    V = 500
    # vectorize texts
    vec = CountVectorizer(max_features=V, stop_words='english')
    X = vec.fit_transform(texts).toarray()
    B_d = get_B_d(X)

    num_topics = 20
    iterations = 2  # iterations for gibbs sampling

    btm = BTM(num_topics, V)
    topics = btm.fit(B_d, iterations)

    # evaluate topics
    n_top_words = 10
    #print_summuary(btm.phi_wz.T, X, V, n_top_words)

    # visualize topics with pyLDAvis
    # vis = pyLDAvis.prepare(btm.phi_wz.T, topics, np.count_nonzero(X, axis=1), V, np.sum(X, axis=0))
    # pyLDAvis.save_html(vis, './btm.html')
