from __future__ import division
import numpy as np
from scipy import sparse


def diffusion_map(G, t=1, n_components=2):
    # symmetric affinity matrix
    K = G.kernel
    # degrees
    diff_deg = np.array(np.sum(K, axis=1)).flatten()
    # negative sqrt
    diff_deg = np.power(diff_deg, -1 / 2)
    # put into square matrix
    diff_deg = sparse.spdiags([diff_deg], diags=0, m=K.shape[0], n=K.shape[0])
    # conjugate
    diff_aff = diff_deg.dot(K).dot(diff_deg)
    # symmetrize to remove numerical error
    diff_aff = (diff_aff + diff_aff.T) / 2
    # svd
    U, S, _ = sparse.linalg.svds(diff_aff, k=n_components + 1)
    # order in terms of smallest eigenvalue
    U, S = U[:, ::-1], S[::-1]
    # get first eigenvector
    u1 = U[:, 0][:, None]
    # ensure non-zero
    zero_idx = np.abs(u1) <= np.finfo(float).eps
    u1[zero_idx] = (np.sign(u1[zero_idx]) * np.finfo(float).eps).flatten()
    # normalize by first eigenvector
    U = U / u1
    # drop first eigenvector
    U, S = U[:, 1:], S[1:]
    # power eigenvalues
    S = np.power(S, t)
    # weight U by eigenvalues
    dm = U.dot(np.diagflat(S))
    return dm
