import numpy as np

a = np.random.rand(5,4)
print('Array a:\n', a)

a[:,:] = 2
print('Modified a:\n', a)

b = np.random.rand(5,4)
print('Array b:\n', b)

mean = b.mean()
print('Mean:\n', mean)

b[b < mean] = mean

print('Modified b:\n', b)
