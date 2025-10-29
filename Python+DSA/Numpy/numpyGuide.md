# NumPy — Complete Guide

Short, practical, hands-on. Work through sections in order. Each section has: brief explanation, clear examples you can run, tasks with answers at the end.

---

# 1 Why NumPy

- NumPy provides fast arrays and vectorized math.
- You work with whole arrays, not Python loops.
- NumPy saves memory and runs faster for numeric code.

# 2 Import

```python
import numpy as np
```

# 3 Array creation

- Use np.array to convert Python lists.
- Use factory functions for common patterns.

Examples

```python
# from list
a = np.array([1,2,3])

# 2D
b = np.array([[1,2,3],[4,5,6]])

# zeros, ones, full
z = np.zeros((2,3))
one = np.ones(4)
f = np.full((2,2), 7)

# arange, linspace
r = np.arange(0,10,2)  # [0 2 4 6 8]
L = np.linspace(0,1,5)  # [0.   0.25 0.5  0.75 1.  ]

# identity, eye
I = np.eye(3)

# random
x = np.random.rand(3,2)   # uniform [0,1)

# empty (uninitialized, faster)
E = np.empty((2,3))
```

Tasks

- Create a 1D array with numbers 10 to 19.
- Create a 3x3 identity matrix.

# 4 Array attributes

- `ndim` number of dimensions
- `shape` tuple of axis lengths
- `size` number of elements
- `dtype` data type
- `itemsize` bytes per element

Examples

```python
a = np.array([[1,2,3],[4,5,6]])
print(a.ndim, a.shape, a.size, a.dtype, a.itemsize)
```

Task

- Print attributes for array of floats `np.array([1.,2.,3.])`.

# 5 Indexing and slicing

- Index like Python: a[0], a[1:4]
- For 2D use row, col: a[0,1]
- Slices return views, not copies.

Examples

```python
arr = np.arange(10)
sub = arr[2:7:2]   # start:stop:step

mat = np.arange(12).reshape(3,4)
row1 = mat[1]
cell = mat[2,3]
col2 = mat[:,2]
```

Note

- Changing `sub` also changes `arr` because `sub` is a view.
- Use `sub.copy()` to get a copy.

Tasks

- Given `a = np.arange(16).reshape(4,4)`, select the bottom-right 2x2 block.
- Extract every other column from `a`.

# 6 Data types and conversions

- NumPy types: int32, int64, float32, float64, bool, complex, object
- Convert with `astype`

Example

```python
x = np.array([1,2,3], dtype=np.int32)
xf = x.astype(np.float64)
```

Task

- Convert `np.array([0,1,1,0])` to boolean.

# 7 Vectorized arithmetic

- Apply operations elementwise. No loops.

Examples

```python
x = np.array([1,2,3])
y = np.array([10,20,30])
print(x + y)
print(x * 2)
print(np.sin(x))
```

Task

- Compute `(x - mean(x)) / std(x)` for `x = np.array([1,3,5,7])`.

# 8 Broadcasting

- Shapes must match or be compatible: trailing axes of length 1 can expand.
- Common case: add vector to each row of a matrix.

Examples

```python
M = np.ones((3,4))
v = np.array([1,2,3,4])
print(M + v)  # v broadcast across rows

w = np.array([10,20,30]).reshape(3,1)
print(w + v)  # shapes (3,1) and (4,) broadcast to (3,4)
```

Rules

- Two dimensions are compatible when equal or one of them is 1.

Task

- Given `A = np.arange(6).reshape(2,3)`, add `[0,10,20]` to each row using broadcasting.

# 9 Aggregations

- `sum, mean, std, min, max, argmin, argmax`
- Use `axis` to reduce across rows or columns.

Examples

```python
M = np.arange(12).reshape(3,4)
print(M.sum())        # total
print(M.sum(axis=0))  # sum of each column
print(M.mean(axis=1)) # mean by row
```

Task

- For `M = np.array([[1,2],[3,4],[5,6]])`, compute column-wise min and row-wise max.

# 10 Fancy indexing and boolean masks

- Use arrays of indices to select elements.
- Use boolean arrays to filter.

Examples

```python
x = np.array([10,20,30,40])
idx = np.array([3,1])
print(x[idx])  # [40 20]

mask = x > 15
print(x[mask]) # [20 30 40]
```

Task

- From `arr = np.arange(1,21)`, select numbers divisible by 3.

# 11 Reshape, ravel, flatten

- `reshape` returns view when possible.
- `ravel` returns view, `flatten` returns copy.

Examples

```python
A = np.arange(9)
B = A.reshape(3,3)
C = A.reshape(-1,1)  # infer dimension
flat = B.ravel()
copy_flat = B.flatten()
```

Task

- Turn a 2x6 array into 3x4 using reshape.

# 12 Concatenate, split

- Use `np.vstack`, `np.hstack`, `np.concatenate`
- Split with `np.split`, `np.vsplit`, `np.hsplit`

Examples

```python
a = np.arange(6).reshape(2,3)
b = np.arange(6,12).reshape(2,3)
print(np.concatenate([a,b], axis=0))  # stack rows
print(np.vstack([a,b]))
print(np.hstack([a,b]))
```

Task

- Given two arrays shape (3,2), (3,4), horizontally stack to get (3,6).

# 13 Linear algebra

- Use `np.dot`, `@`, `np.matmul`, `np.linalg.inv`, `np.linalg.solve`, `np.linalg.eig`

Examples

```python
A = np.array([[3,1],[2,4]])
b = np.array([1,2])
# solve Ax=b
x = np.linalg.solve(A,b)
# inverse
Ai = np.linalg.inv(A)
# eigen
vals, vecs = np.linalg.eig(A)
```

Task

- Solve system: 2x + 3y = 8, 5x - y = 7.

# 14 Random numbers

- `np.random.rand`, `randn`, `integers`, `choice`, `seed`

Examples

```python
np.random.seed(0)
print(np.random.rand(3,2))
print(np.random.randn(3))  # normal
print(np.random.randint(0,10, size=5))
```

Task

- Create reproducible 5x5 matrix of integers 0..9 with seed 42.

# 15 Performance notes

- Use vectorized ops. Avoid Python loops.
- Prefer in-place where possible: `a += b`.
- Use proper dtypes to save memory.

Mini benchmark example

```python
import time
N = 10_000_000
py = list(range(N))
start=time.time()
s = sum(py)
print('python loop', time.time()-start)

arr = np.arange(N)
start=time.time()
s2 = arr.sum()
print('numpy', time.time()-start)
```

# 16 IO: save and load

Examples

```python
np.save('arr.npy', a)
load = np.load('arr.npy')
np.savetxt('arr.csv', a, delimiter=',')
np.loadtxt('arr.csv', delimiter=',')
```

# 17 Tips and gotchas

- Slicing returns view. Use copy() when needed.
- Watch integer division in Python 2 only. In modern numpy, division yields float.
- Use `np.set_printoptions` to control print precision.

# 18 Exercises (project style)

1. Image flattening

- Load an image as array (use PIL or imageio). Convert to grayscale. Flatten to 1D. Compute mean and std. Reshape back.

2. Data cleaning

- Given 1D array with some NaNs, replace NaNs with column mean of corresponding reshaped matrix.

3. Simple PCA (using SVD)

- Given data matrix X (samples x features), center columns, compute SVD, project onto first 2 components.

4. Linear regression by normal equations

- Given X (with bias column) and y, solve for beta using `np.linalg.solve` or `pinv`.

# 19 Solutions (brief)

- Here are the solutions for all tasks:

**Array creation**

```python
np.arange(10,20)
np.eye(3)
```

**Array attributes**

```python
a = np.array([1.,2.,3.])
print(a.ndim, a.shape, a.size, a.dtype, a.itemsize)
```

**Indexing and slicing**

```python
a = np.arange(16).reshape(4,4)
print(a[2:,2:])   # bottom-right 2x2
print(a[:,::2])   # every other column
```

**Data types and conversions**

```python
arr = np.array([0,1,1,0])
print(arr.astype(bool))
```

**Vectorized arithmetic**

```python
x = np.array([1,3,5,7])
z = (x - x.mean()) / x.std()
print(z)
```

**Broadcasting**

```python
A = np.arange(6).reshape(2,3)
A = A + np.array([0,10,20])
print(A)
```

**Aggregations**

```python
M = np.array([[1,2],[3,4],[5,6]])
print(M.min(axis=0))
print(M.max(axis=1))
```

**Fancy indexing and boolean masks**

```python
arr = np.arange(1,21)
print(arr[arr % 3 == 0])
```

**Reshape**

```python
x = np.arange(12).reshape(2,6)
y = x.reshape(3,4)
print(y)
```

**Concatenate**

```python
a = np.ones((3,2))
b = np.zeros((3,4))
print(np.hstack([a,b]))
```

**Linear algebra**

```python
A = np.array([[2,3],[5,-1]])
b = np.array([8,7])
sol = np.linalg.solve(A,b)
print(sol)
```

**Random numbers**

```python
np.random.seed(42)
print(np.random.randint(0,10,(5,5)))
```

**Project hints**

- Use `np.nanmean` for NaN replacements.
- PCA: `U,S,Vt = np.linalg.svd(X_centered)` then project with `X_proj = X_centered @ Vt[:2].T`
- Linear regression: `beta = np.linalg.inv(X.T@X)@X.T@y`
