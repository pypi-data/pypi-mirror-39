from itertools import combinations, chain
import numpy as np
import math

def get_B_d(X):
    B_d = []
    for x in X:
        b_i = [b for b in combinations(np.nonzero(x)[0], 2)]
        B_d.append(b_i)
    return B_d


def topic_summuary(P_wz, X, V, M, verbose=True):
    for z, P_wzi in enumerate(P_wz):
        V_z = np.argsort(P_wzi)[:-(M + 1):-1]
        W_z = V[V_z]

        # calculate topic coherence score -> http://dirichlet.net/pdf/mimno11optimizing.pdf
        C_z = 0
        for m in range(1, M):
            for l in range(m):
                D_vmvl = np.sum(np.in1d(np.nonzero(X[:,V_z[l]]), np.nonzero(X[:,V_z[m]]))) + 1
                D_vl = np.count_nonzero(X[:,V_z[l]])
                C_z += math.log(D_vmvl / D_vl)

        if verbose: print('Topic {} | Coherence={:0.2f} | Top words= {}'.format(z, C_z, ' '.join(W_z)))
        return z, C_z, W_z

