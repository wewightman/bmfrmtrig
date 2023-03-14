import numpy as np
refs = np.arange(12).reshape((-1,3))
trefs = np.zeros(4)
alphas = np.ones(4)
print([tee for tee in zip((*refs, *trefs, *alphas))])
a = [print(tee) for tee in zip(refs, trefs, alphas)]
print(a[0])
