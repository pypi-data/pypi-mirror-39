import numpy as np
from itertools import combinations, chain
from tqdm import trange
from biterm.utility import get_B_d

class BTM:
    """ Biterm Topic Model

        Code and naming is based on this paper http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.402.4032&rep=rep1&type=pdf
        Thanks to jcapde for providing the code on https://github.com/jcapde/Biterm
    """

    def __init__(self, num_topics, V, alpha=1., beta=0.01, l=0.5):
        self.K = num_topics
        self.V = V
        self.alpha = np.full(self.K, alpha)
        self.beta = np.full((self.V, self.K), beta)
        self.l = l


    def _gibbs_sample(self, iterations):

        Z = np.zeros(len(self.B), dtype=np.int8)
        n_wz = np.zeros((self.V, self.K), dtype=int)
        n_z = np.zeros(self.K, dtype=int)

        for i, b_i in enumerate(self.B):
            topic = np.random.choice(self.K, 1)[0]
            n_wz[b_i[0], topic] += 1
            n_wz[b_i[1], topic] += 1
            n_z[topic] += 1
            Z[i] = topic

        for _ in trange(iterations):
            for i, b_i in enumerate(self.B):
                n_wz[b_i[0], Z[i]] -= 1
                n_wz[b_i[1], Z[i]] -= 1
                n_z[Z[i]] -= 1
                P_z = (n_z + self.alpha) * ((n_wz[b_i[0], :] + self.beta[b_i[0], :]) * (n_wz[b_i[1], :] + self.beta[b_i[1], :]) /
                      (n_wz + self.beta).sum(axis=0) ** 2)
                P_z = P_z / P_z.sum()
                Z[i] = np.random.choice(self.K, 1, p=P_z)
                n_wz[b_i[0], Z[i]] += 1
                n_wz[b_i[1], Z[i]] += 1
                n_z[Z[i]] += 1

        return n_z, n_wz

    def fit_transform(self, B_d, iterations):
        self.fit(B_d, iterations)
        return self.transform(B_d)

    def fit(self, B_d, iterations):
        self.B = list(chain(*B_d))
        n_z, n_wz = self._gibbs_sample(iterations)

        self.phi_wz = (n_wz + self.beta) / np.array([(n_wz + self.beta).sum(axis=1)] * self.K).T
        self.theta_z = (n_z + self.alpha) / (n_z + self.alpha).sum()

        self.alpha += self.l * n_z
        self.beta += self.l * n_wz


    def transform(self, B_d):

        P_zb = [[list(self.theta_z * self.phi_wz[b_i[0], :] * self.phi_wz[b_i[1], :] /
                      (self.theta_z * self.phi_wz[b_i[0], :] * self.phi_wz[b_i[1], :]).sum())
                 for b_i in set(doc)] for doc in B_d]

        P_zd = []
        for P_zbi in P_zb:
            P_zd.append(sum(P_zbi))

        return np.array(P_zd)
