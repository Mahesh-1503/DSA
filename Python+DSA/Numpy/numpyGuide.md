# NumPy — Complete Guide with Explanations

Work through sections in order. Each part has a brief explanation, runnable examples with comments, and small tasks.

---

## 1. Why NumPy

- NumPy gives fast, memory-efficient arrays.
- It replaces slow Python loops with vectorized operations.
- You use array math directly on data.

---

## 2. Import

```python
import numpy as np  # standard import
```

---

## 3. Array creation

Use `np.array()` or built-in generators.

```python
# From Python list
a = np.array([1,2,3])  # 1D array

# 2D array
b = np.array([[1,2,3],[4,5,6]])

# Predefined arrays
z = np.zeros((2,3))    # all zeros
one = np.ones(4)       # all ones
f = np.full((2,2), 7)  # filled with constant 7

# Number sequences
r = np.arange(0,10,2)     # step of 2
L = np.linspace(0,1,5)    # 5 evenly spaced values between 0–1

# Identity matrix
I = np.eye(3)

# Random arrays
x = np.random.rand(3,2)   # random floats in [0,1)
E = np.empty((2,3))       # uninitialized values (faster)
```

**Tasks**

- Create `[10,11,...,19]`
- Create a 3×3 identity matrix.

---

## 4. Array attributes

Check key properties.

```python
a = np.array([[1,2,3],[4,5,6]])
print(a.ndim)    # number of dimensions
print(a.shape)   # rows, columns
print(a.size)    # total elements
print(a.dtype)   # data type
print(a.itemsize)# bytes per element
```

**Task**

- Print same attributes for `np.array([1.,2.,3.])`.

---

## 5. Indexing and slicing

Use standard syntax.

```python
arr = np.arange(10)
sub = arr[2:7:2]        # start:stop:step
print(sub)

mat = np.arange(12).reshape(3,4)
print(mat[1])           # 2nd row
print(mat[2,3])         # specific cell
print(mat[:,2])         # full column
```

- Slices are **views**, not copies.
- Use `.copy()` to avoid linked changes.

**Tasks**

- Extract bottom-right 2×2 of a 4×4 array.
- Extract every other column.

---

## 6. Data types and conversions

```python
x = np.array([1,2,3], dtype=np.int32)
xf = x.astype(np.float64)   # convert to float
print(xf)
```

**Task**

- Convert `[0,1,1,0]` to boolean.

---

## 7. Vectorized arithmetic

```python
x = np.array([1,2,3])
y = np.array([10,20,30])

print(x + y)         # elementwise add
print(x * 2)         # scalar multiply
print(np.sin(x))     # elementwise sine
```

**Task**

- Standardize `[1,3,5,7]` using `(x - mean) / std`.

---

## 8. Broadcasting

- Smaller shapes automatically expand.
- Works when trailing dimensions are equal or 1.

```python
M = np.ones((3,4))
v = np.array([1,2,3,4])
print(M + v)  # vector added to each row

w = np.array([10,20,30]).reshape(3,1)
print(w + v)  # expands both ways
```

**Task**

- Add `[0,10,20]` to each row of `np.arange(6).reshape(2,3)`.

---

## 9. Aggregations

```python
M = np.arange(12).reshape(3,4)
print(M.sum())         # total
print(M.sum(axis=0))   # by column
print(M.mean(axis=1))  # by row
```

**Task**

- Compute column min and row max for
  `np.array([[1,2],[3,4],[5,6]])`.

---

## 10. Logical operations

Work elementwise for comparisons and logical tests.

```python
a = np.array([1,2,3,4,5])
b = np.array([3,2,1,4,6])

print(a > 2)                            # boolean array
print(a == b)                           # compare arrays
print(np.logical_and(a>1, a<5))         # AND
print(np.logical_or(a==2, b==6))        # OR
print(np.all(a<6), np.any(a==3))        # reduce to single bool
```

**Task**

- Check even numbers in `[10,20,30,40]`.
- Test if all > 5.

---

## 11. Statistical operations

Used for quick analysis.

```python
data = np.array([[1,2,3],[4,5,6],[7,8,9]])

print(np.mean(data))             # mean of all
print(np.mean(data, axis=0))     # column means
print(np.std(data))              # std deviation
print(np.var(data))              # variance
print(np.median(data))           # median
print(np.percentile(data, 50))   # 50th percentile = median
print(np.corrcoef(data[0], data[1]))  # correlation
```

**Task**

- Find variance and std for `[5,10,15,20]`.
- Get 25th, 50th, 75th percentiles for `[1,3,5,7,9]`.

---

## 12. Fancy indexing and boolean masks

Select using index arrays or boolean filters.

```python
x = np.array([10,20,30,40])
print(x[[3,1]])     # specific indices
print(x[x>15])      # filter by condition
```

**Task**

- Select all numbers divisible by 3 from 1–20.

---

## 13. Reshape, concatenate, and split

```python
a = np.arange(6).reshape(2,3)
b = np.arange(6,12).reshape(2,3)

print(np.concatenate([a,b], axis=0))  # vertical join
print(np.vstack([a,b]))               # same
print(np.hstack([a,b]))               # horizontal join
```

**Task**

- Stack arrays of shapes (3,2) and (3,4) into (3,6).

---

## 14. Linear algebra

```python
A = np.array([[3,1],[2,4]])
b = np.array([1,2])

x = np.linalg.solve(A,b)     # solve Ax=b
Ai = np.linalg.inv(A)        # inverse
vals, vecs = np.linalg.eig(A)# eigenvalues/vectors

print(x, Ai, vals)
```

**Task**

- Solve 2x + 3y = 8, 5x – y = 7.

---

## 15. Random numbers

```python
np.random.seed(0)
print(np.random.rand(3,2))             # uniform
print(np.random.randn(3))              # normal
print(np.random.randint(0,10,5))       # integers
```

**Task**

- Generate reproducible 5×5 integers 0–9 with seed 42.

---

## 16. Performance

```python
import time

N = 10_000_000
py = list(range(N))
start=time.time()
sum(py)
print('Python loop:', time.time()-start)

arr = np.arange(N)
start=time.time()
arr.sum()
print('NumPy:', time.time()-start)
```

- NumPy is much faster due to vectorized C code.
- Use in-place ops (`a += b`) when possible.

---

## 17. I/O operations

```python
np.save('arr.npy', a)
np.load('arr.npy')

np.savetxt('arr.csv', a, delimiter=',')
np.loadtxt('arr.csv', delimiter=',')
```

---

## 18. Tips and gotchas

- Slicing gives a **view**, not a copy.
- Use `.copy()` to avoid side effects.
- Set print precision: `np.set_printoptions(precision=3)`.

---

## 19. Exercises

1. **Image flattening**
   Convert image to grayscale, flatten, find mean/std, reshape back.

2. **Data cleaning**
   Replace NaN with column mean.

3. **PCA (SVD method)**
   Center data, use `np.linalg.svd`, project on 2 components.

4. **Linear regression**
   Use normal equation:
   `beta = np.linalg.inv(X.T@X) @ X.T @ y`.

---

## 20. Task Solutions

```python
# 3 Array creation
np.arange(10,20)
np.eye(3)

# 4 Attributes
a = np.array([1.,2.,3.])
print(a.ndim, a.shape, a.size, a.dtype, a.itemsize)

# 5 Indexing
a = np.arange(16).reshape(4,4)
print(a[2:,2:])
print(a[:,::2])

# 6 Conversion
arr = np.array([0,1,1,0]).astype(bool)
print(arr)

# 7 Arithmetic
x = np.array([1,3,5,7])
z = (x - x.mean()) / x.std()
print(z)

# 8 Broadcasting
A = np.arange(6).reshape(2,3)
print(A + np.array([0,10,20]))

# 9 Aggregation
M = np.array([[1,2],[3,4],[5,6]])
print(M.min(axis=0))
print(M.max(axis=1))

# 10 Logical
vals = np.array([10,20,30,40])
print(vals % 2 == 0)
print(np.all(vals > 5))

# 11 Statistical
arr = np.array([5,10,15,20])
print(np.var(arr), np.std(arr))
nums = np.array([1,3,5,7,9])
print(np.percentile(nums, [25,50,75]))

# 12 Boolean mask
arr = np.arange(1,21)
print(arr[arr % 3 == 0])

# 13 Concatenate
a = np.ones((3,2))
b = np.zeros((3,4))
print(np.hstack([a,b]))

# 14 Linear algebra
A = np.array([[2,3],[5,-1]])
b = np.array([8,7])
print(np.linalg.solve(A,b))

# 15 Random
np.random.seed(42)
print(np.random.randint(0,10,(5,5)))
```