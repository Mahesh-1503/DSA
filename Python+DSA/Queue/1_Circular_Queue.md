# Circular Queue – A Comprehensive Textbook Chapter

---

## 1. Introduction: The Problem with Linear Queues

Before we meet the circular queue, let’s revisit the humble **linear queue** that we already know.

### Recap: The Linear Queue

A linear queue is a FIFO (First-In, First-Out) data structure. We use two pointers:

- **Front** – points to the first element (to be removed).
- **Rear** – points to the last element (where new elements are added).

In an array-based implementation, we have a fixed capacity. Elements are added at the rear and removed from the front.

#### ASCII Memory Representation

```text
Capacity = 5

Initial empty queue:
front = -1, rear = -1
[   ] [   ] [   ] [   ] [   ]

After enqueue(10), enqueue(20), enqueue(30):
front = 0, rear = 2
[10] [20] [30] [   ] [   ]
  ↑              ↑
front           rear
```

### The Limitation: False Overflow

Now, let’s perform some dequeue operations.

```text
After dequeue() twice:
front = 2, rear = 2
[ x ] [ x ] [30] [   ] [   ]
              ↑
            front/rear
```

We have removed 10 and 20. The indices 0 and 1 are now empty, but `rear` is still at 2. If we try to enqueue another element, we check `rear == capacity-1` – which is **false** because rear is 2, not 4. So we can still add more. But if we continue enqueuing until rear reaches 4:

```text
After enqueue(40), enqueue(50):
front = 2, rear = 4
[ x ] [ x ] [30] [40] [50]
              ↑         ↑
            front      rear
```

Now `rear == 4`, so the queue is considered **full**. But we have two empty slots at the front! This is called **false overflow** or **memory wastage**. We cannot reuse those slots because the linear queue only moves forward – we never wrap around.

### Why Not Shift Elements?

We could shift all remaining elements to the left after each dequeue, but that would cost O(n) time, making dequeue inefficient.

### The Intuition: We Need a “Circle”

What if we could reuse the empty slots at the beginning when the rear reaches the end? Imagine the array is not a straight line but a **circle**. When we reach the last index, we simply go back to index 0. That’s the idea behind the **circular queue**.

---

## 2. Real‑Life Analogies

Let’s build intuition with everyday examples.

### Analogy 1: A Circular Road

Imagine a circular track with parking spots numbered 0 to 4. Cars arrive and park in order. When spot 4 is occupied, the next car parks at spot 0 (if empty). The front car (the one that has been waiting longest) leaves from its spot. The rear moves around the circle.

- **Front** – the spot with the oldest car.
- **Rear** – the spot where the next car will park.
- **Wrapping** – when rear reaches spot 4, the next spot is 0.

### Analogy 2: A Clock

A clock has numbers 1 to 12. After 12 comes 1. That’s a perfect circle. If we treat the clock as a queue, the hour hand (rear) moves forward, and when it passes 12, it wraps to 1.

### Analogy 3: A Round Table with Chairs

People sit around a round table. New guests always sit in the next empty chair clockwise. When the last chair is taken, the next guest sits in the first chair if it is free (i.e., the person who was sitting there has left). The oldest person (front) leaves, freeing a chair.

### Analogy 4: Ferris Wheel

Cabins move around a wheel. New passengers board at the bottom (rear), and after a full revolution, they get off at the bottom (front). But if a cabin is already occupied, it skips boarding. The wheel keeps rotating, reusing cabins.

### Analogy 5: Conveyor Belt

Items are placed on a conveyor belt at one end and taken off at the other. The belt is a loop; items keep moving around until removed. If the belt is full, new items cannot be placed until an item is removed.

**In all analogies, the key is reuse of space – the circle allows us to go around.**

---

## 3. What is a Circular Queue?

A **circular queue** (also known as a **ring buffer**) is a linear data structure that uses a fixed-size array, but treats it as if the ends are connected to form a circle. When the rear pointer reaches the last index, it wraps around to index 0. Similarly, front wraps around after dequeue.

This overcomes the false overflow problem of a linear queue.

### How the Circle Works

We use the **modulo operator (`%`)** to compute the next index:

```
rear = (rear + 1) % capacity
front = (front + 1) % capacity
```

The `%` ensures that the index always stays within the range `[0, capacity-1]`.

### Key Differences from Linear Queue

| Feature | Linear Queue | Circular Queue |
|---------|--------------|----------------|
| **Wrap-around** | No | Yes |
| **Memory reuse** | No | Yes |
| **False overflow** | Yes | No |
| **Full condition** | `rear == capacity-1` | `(rear+1) % capacity == front` |
| **Empty condition** | `front == -1` | `front == -1` (or `front == rear` if we use a different strategy) |

---

## 4. Core Concepts in Depth

### 4.1 The Modulo Operator Masterclass

Let’s understand `%` from scratch.

`a % b` gives the remainder when `a` is divided by `b`.

Examples:
- `7 % 5 = 2` (because 7 = 5×1 + 2)
- `11 % 5 = 1`
- `18 % 5 = 3`

Now, for a circular queue of size 5, indices are 0,1,2,3,4. After index 4, the next index should be 0. How do we compute that?

```
next_index = (current_index + 1) % 5
```

If `current_index = 4`, then `(4+1) % 5 = 0`. Perfect.

If `current_index = 2`, then `(2+1) % 5 = 3`.

So `rear = (rear + 1) % capacity` always gives the next position in the circle.

**Why does this prevent overflow?** Because we never go beyond `capacity-1`; the index wraps around.

### 4.2 Front and Rear Pointers in Circular Queue

We maintain two integer pointers:

- `front` – index of the first element.
- `rear` – index of the last element.

**Initial state (empty queue):** we set both `front` and `rear` to `-1`.

**Enqueue:** if empty, set `front = rear = 0`; otherwise `rear = (rear + 1) % capacity` and place element at that index.

**Dequeue:** if empty, error; otherwise store `arr[front]`; if `front == rear` (only one element left), reset both to `-1`; else `front = (front + 1) % capacity`.

### 4.3 Empty and Full Conditions

There are two common ways to manage emptiness/fullness:

#### Method 1: Keep a `count` variable
- Maintain a separate `size` counter.
- Empty if `size == 0`.
- Full if `size == capacity`.

This is simple and avoids the ambiguity of circular pointers.

#### Method 2: Use only `front` and `rear` (no count)
- **Empty:** `front == -1` (or `front == rear` and both indicate empty, but need a sentinel).
- **Full:** `(rear + 1) % capacity == front`.

However, if we use `front == rear` to indicate empty, we lose one slot because full condition would also be `front == rear` (if we allow full when rear is one behind front). So we usually leave one slot unused to distinguish full from empty.

**In this chapter, we will use Method 1 (with `count`)** because it is more beginner-friendly and avoids confusion.

---

## 5. Operations on Circular Queue

We will cover each operation in detail, with all required pedagogical components.

### 5.1 Create Circular Queue

**Problem:** Initialize an empty circular queue with a given capacity.

**Intuition:** Allocate an array, set `front = rear = -1`, and `count = 0`.

**ASCII Memory Diagram:**
```text
capacity = 5
front = -1, rear = -1, count = 0
[   ] [   ] [   ] [   ] [   ]
```

**Algorithm:**
1. Allocate array of size `capacity`.
2. Set `front = rear = -1`, `count = 0`.

**Python Implementation:**
```python
class CircularQueue:
    """Circular Queue using an array with a count variable."""

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity
        self.arr = [None] * capacity
        self.front = -1
        self.rear = -1
        self.count = 0
```

**Complexity:** O(1) time, O(capacity) space.

---

### 5.2 isEmpty()

**Problem:** Check if the queue has no elements.

**Intuition:** If `count == 0`, it's empty.

**Pseudo Code:**
```
isEmpty():
    return count == 0
```

**Python:**
```python
def is_empty(self) -> bool:
    """Return True if the queue is empty."""
    return self.count == 0
```

**Complexity:** O(1).

---

### 5.3 isFull()

**Problem:** Check if the queue has reached its capacity.

**Intuition:** If `count == capacity`, it's full.

**Pseudo Code:**
```
isFull():
    return count == capacity
```

**Python:**
```python
def is_full(self) -> bool:
    """Return True if the queue is full."""
    return self.count == self.capacity
```

**Complexity:** O(1).

---

### 5.4 Enqueue (Add Element)

**Problem:** Add an element to the rear of the circular queue.

**Intuition:**
- If full, raise overflow.
- If empty, set `front = rear = 0`.
- Else, move `rear` forward: `rear = (rear + 1) % capacity`.
- Place the element at `rear`.
- Increment `count`.

**Prediction Question:** What happens if we enqueue when the queue is empty? Where will the first element be placed? (Answer: at index 0, with both front and rear pointing to 0.)

**Visualization (ASCII):**

Before enqueue (empty):
```text
front = -1, rear = -1, count = 0
[   ] [   ] [   ] [   ] [   ]
```

After enqueue(10):
```text
front = 0, rear = 0, count = 1
[10] [   ] [   ] [   ] [   ]
  ↑
front/rear
```

After enqueue(20) and enqueue(30):
```text
front = 0, rear = 2, count = 3
[10] [20] [30] [   ] [   ]
  ↑         ↑
front      rear
```

Now suppose we dequeue twice (removing 10 and 20):
```text
front = 2, rear = 2, count = 1
[ x ] [ x ] [30] [   ] [   ]
              ↑
            front/rear
```

Now enqueue(40):
```text
front = 2, rear = 3, count = 2
[ x ] [ x ] [30] [40] [   ]
              ↑    ↑
            front rear
```

Enqueue(50):
```text
front = 2, rear = 4, count = 3
[ x ] [ x ] [30] [40] [50]
              ↑         ↑
            front      rear
```

Enqueue(60): `rear = (4+1)%5 = 0`. Place at index 0:
```text
front = 2, rear = 0, count = 4
[60] [ x ] [30] [40] [50]
  ↑              ↑
 rear           front
```

Notice how rear wrapped to 0!

**Algorithm:**
1. If `is_full()`: raise OverflowError.
2. If `is_empty()`: set `front = rear = 0`.
3. Else: `rear = (rear + 1) % capacity`.
4. `arr[rear] = item`.
5. `count += 1`.

**Python Implementation:**
```python
def enqueue(self, item: int) -> None:
    """Add an item to the rear of the circular queue."""
    if self.is_full():
        raise OverflowError("Queue is full")
    if self.is_empty():
        self.front = self.rear = 0
    else:
        self.rear = (self.rear + 1) % self.capacity
    self.arr[self.rear] = item
    self.count += 1
```

**Driver Code:**
```python
cq = CircularQueue(5)
cq.enqueue(10)
cq.enqueue(20)
cq.enqueue(30)
cq.enqueue(40)
cq.enqueue(50)
print(cq.arr)  # [10,20,30,40,50]
try:
    cq.enqueue(60)
except OverflowError as e:
    print(e)  # Queue is full
```

**Expected Output:**
```
[10, 20, 30, 40, 50]
Queue is full
```

**Output Explanation:**
The first five enqueues fill the queue. The sixth raises an overflow.

**Memory State Before/After:**
- Before: empty or partially filled.
- After: element added, rear and count updated.

**Dry Run (Trace Table):**
| Step | Operation | front | rear | count | arr |
|------|-----------|-------|------|-------|-----|
| 0 | init | -1 | -1 | 0 | [ , , , , ] |
| 1 | enqueue(10) | 0 | 0 | 1 | [10, , , , ] |
| 2 | enqueue(20) | 0 | 1 | 2 | [10,20, , , ] |
| 3 | enqueue(30) | 0 | 2 | 3 | [10,20,30, , ] |
| 4 | enqueue(40) | 0 | 3 | 4 | [10,20,30,40, ] |
| 5 | enqueue(50) | 0 | 4 | 5 | [10,20,30,40,50] |
| 6 | enqueue(60) | – | – | – | Overflow |

**Complexity:** O(1) time, O(1) space.

**Edge Cases:**
- Enqueue on empty queue.
- Enqueue when `front` is not 0 (wrap-around).
- Enqueue when queue is full.

**Common Mistakes:**
- Forgetting to wrap the rear index.
- Not updating `front` on first enqueue.
- Not checking `is_full()` before enqueue.
- Using `front == rear` to detect fullness without considering the `count` variable.

**Debugging Tips:**
- Print `front`, `rear`, `count`, and the array after each enqueue.
- For wrap-around, verify that `rear` becomes 0 after 4.

**Interview Discussion:**
- Why do we use a `count` variable instead of relying only on pointers? It simplifies the full/empty checks and eliminates the need to waste one slot.
- How would you handle dynamic resizing? (We'll discuss later.)

---

### 5.5 Dequeue (Remove Element)

**Problem:** Remove and return the front element.

**Intuition:**
- If empty, raise underflow.
- Store the element at `front`.
- If this is the last element (`count == 1`), reset `front = rear = -1`.
- Else, move `front` forward: `front = (front + 1) % capacity`.
- Decrement `count`.
- Return the stored element.

**Prediction Question:** What happens to the element after dequeue? Is it removed from memory? (Answer: It remains in the array, but we will overwrite it later. Logically, it is removed.)

**Visualization (ASCII):**

Assume we have the following queue after some operations:
```text
front = 2, rear = 0, count = 4
[60] [ x ] [30] [40] [50]
  ↑              ↑
 rear           front
```

Before dequeue:
```text
[60] [ x ] [30] [40] [50]
  ↑              ↑
 rear           front
```

After dequeue():
- `item = arr[front] = 30`.
- `front = (2+1)%5 = 3`.
- `count = 3`.

```text
[60] [ x ] [ x ] [40] [50]
  ↑              ↑
 rear           front
```
Now `front` points to 40.

**Algorithm:**
1. If `is_empty()`: raise IndexError.
2. `item = arr[front]`.
3. If `count == 1`: `front = rear = -1`.
4. Else: `front = (front + 1) % capacity`.
5. `count -= 1`.
6. Return `item`.

**Python Implementation:**
```python
def dequeue(self) -> int:
    """Remove and return the front element."""
    if self.is_empty():
        raise IndexError("Queue is empty")
    item = self.arr[self.front]
    if self.count == 1:
        self.front = self.rear = -1
    else:
        self.front = (self.front + 1) % self.capacity
    self.count -= 1
    return item
```

**Driver Code:**
```python
cq = CircularQueue(5)
cq.enqueue(10)
cq.enqueue(20)
cq.enqueue(30)
print(cq.dequeue())  # 10
print(cq.dequeue())  # 20
print(cq.dequeue())  # 30
try:
    cq.dequeue()
except IndexError as e:
    print(e)  # Queue is empty
```

**Expected Output:**
```
10
20
30
Queue is empty
```

**Output Explanation:** Each dequeue returns the front element and moves front forward. After the last dequeue, queue becomes empty.

**Memory State Before/During/After:**
- Before: non-empty.
- During: front advances.
- After: if last element, reset pointers.

**Dry Run (Trace Table):**
Assume we have already enqueued 10,20,30 with front=0, rear=2, count=3.

| Step | Operation | front | rear | count | arr (logical) |
|------|-----------|-------|------|-------|---------------|
| 0 | init | 0 | 2 | 3 | [10,20,30, , ] |
| 1 | dequeue() | 1 | 2 | 2 | [ x ,20,30, , ] (return 10) |
| 2 | dequeue() | 2 | 2 | 1 | [ x , x ,30, , ] (return 20) |
| 3 | dequeue() | -1 | -1 | 0 | [ x , x , x , , ] (return 30) |
| 4 | dequeue() | – | – | – | Underflow |

**Complexity:** O(1) time, O(1) space.

**Edge Cases:**
- Dequeue when only one element remains.
- Dequeue when front wraps around.
- Dequeue on empty queue.

**Common Mistakes:**
- Forgetting to reset both `front` and `rear` when the last element is removed.
- Not checking `is_empty()` before dequeue.
- Using `front == rear` to detect last element incorrectly when `count` is used.
- Not handling wrap-around of front after dequeue.

**Debugging Tips:**
- After dequeue, verify that `front` and `rear` are consistent with `count`.
- If `count == 0`, ensure both pointers are -1.

**Interview Discussion:**
- How would you implement a circular queue without a `count` variable? (You need to use one slot to distinguish full/empty.)
- What if you need to dynamically resize the queue? You would need to copy elements to a new array, handling the wrap-around properly.

---

### 5.6 Peek (Front Element)

**Problem:** Return the front element without removing it.

**Intuition:** Return `arr[front]` if queue is not empty.

**Python:**
```python
def peek(self) -> int:
    """Return the front element without removing it."""
    if self.is_empty():
        raise IndexError("Queue is empty")
    return self.arr[self.front]
```

**Complexity:** O(1).

---

### 5.7 Rear (Back Element)

**Problem:** Return the rear element without removing it.

**Python:**
```python
def rear(self) -> int:
    """Return the rear element without removing it."""
    if self.is_empty():
        raise IndexError("Queue is empty")
    return self.arr[self.rear]
```

**Complexity:** O(1).

---

### 5.8 Display

**Problem:** Print all elements from front to rear.

**Intuition:** Iterate through the queue starting at `front`, moving forward modulo `capacity`, until we have printed `count` elements.

**Python Implementation:**
```python
def display(self) -> None:
    """Print the queue elements from front to rear."""
    if self.is_empty():
        print("Queue is empty")
        return
    print("Front -> ", end="")
    idx = self.front
    for _ in range(self.count):
        print(self.arr[idx], end=" ")
        idx = (idx + 1) % self.capacity
    print("<- Rear")
```

**Driver Code:**
```python
cq = CircularQueue(5)
cq.enqueue(10)
cq.enqueue(20)
cq.enqueue(30)
cq.enqueue(40)
cq.enqueue(50)
cq.display()
# After dequeue twice and enqueue 60,70:
cq.dequeue()
cq.dequeue()
cq.enqueue(60)
cq.enqueue(70)
cq.display()
```

**Expected Output:**
```
Front -> 10 20 30 40 50 <- Rear
Front -> 30 40 50 60 70 <- Rear
```

**Explanation:** The second display shows that the queue now wraps around; the order is maintained.

**Complexity:** O(n) time, O(1) space.

---

## 6. Complete Implementation with Driver

Here is the full, production-quality Python class.

```python
from typing import Optional, List

class CircularQueue:
    """Circular Queue using an array with a count variable."""

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity
        self.arr: List[Optional[int]] = [None] * capacity
        self.front: int = -1
        self.rear: int = -1
        self.count: int = 0

    def is_empty(self) -> bool:
        return self.count == 0

    def is_full(self) -> bool:
        return self.count == self.capacity

    def enqueue(self, item: int) -> None:
        if self.is_full():
            raise OverflowError("Queue is full")
        if self.is_empty():
            self.front = self.rear = 0
        else:
            self.rear = (self.rear + 1) % self.capacity
        self.arr[self.rear] = item
        self.count += 1

    def dequeue(self) -> int:
        if self.is_empty():
            raise IndexError("Queue is empty")
        item = self.arr[self.front]
        if self.count == 1:
            self.front = self.rear = -1
        else:
            self.front = (self.front + 1) % self.capacity
        self.count -= 1
        return item

    def peek(self) -> int:
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.arr[self.front]

    def rear(self) -> int:
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.arr[self.rear]

    def size(self) -> int:
        return self.count

    def display(self) -> None:
        if self.is_empty():
            print("Queue is empty")
            return
        print("Front -> ", end="")
        idx = self.front
        for _ in range(self.count):
            print(self.arr[idx], end=" ")
            idx = (idx + 1) % self.capacity
        print("<- Rear")
```

**Driver Code:**
```python
if __name__ == "__main__":
    cq = CircularQueue(5)
    print("Enqueue: 10,20,30,40,50")
    cq.enqueue(10)
    cq.enqueue(20)
    cq.enqueue(30)
    cq.enqueue(40)
    cq.enqueue(50)
    cq.display()

    print("Dequeue two elements")
    print("Dequeued:", cq.dequeue())
    print("Dequeued:", cq.dequeue())
    cq.display()

    print("Enqueue 60,70")
    cq.enqueue(60)
    cq.enqueue(70)
    cq.display()

    print("Current size:", cq.size())
    print("Peek front:", cq.peek())
    print("Peek rear:", cq.rear())
```

**Expected Console Output:**
```
Enqueue: 10,20,30,40,50
Front -> 10 20 30 40 50 <- Rear
Dequeue two elements
Dequeued: 10
Dequeued: 20
Front -> 30 40 50 <- Rear
Enqueue 60,70
Front -> 30 40 50 60 70 <- Rear
Current size: 5
Peek front: 30
Peek rear: 70
```

**Output Explanation:** The queue wraps around after dequeueing, allowing new elements to occupy the freed slots at the beginning.

---

## 7. Internal Working – Execution Trace

Let's trace a full sequence to see how pointers move.

**Sequence:** `enqueue(10)`, `enqueue(20)`, `enqueue(30)`, `dequeue()`, `dequeue()`, `enqueue(40)`, `enqueue(50)`, `enqueue(60)`.

**Capacity = 5.**

| Step | Operation | front | rear | count | arr (with indices) |
|------|-----------|-------|------|-------|---------------------|
| 0 | init | -1 | -1 | 0 | [0: ,1: ,2: ,3: ,4: ] |
| 1 | enqueue(10) | 0 | 0 | 1 | [0:10,1: ,2: ,3: ,4: ] |
| 2 | enqueue(20) | 0 | 1 | 2 | [0:10,1:20,2: ,3: ,4: ] |
| 3 | enqueue(30) | 0 | 2 | 3 | [0:10,1:20,2:30,3: ,4: ] |
| 4 | dequeue() | 1 | 2 | 2 | [0:10,1:20,2:30,3: ,4: ] (10 removed) |
| 5 | dequeue() | 2 | 2 | 1 | [0:10,1:20,2:30,3: ,4: ] (20 removed) |
| 6 | enqueue(40) | 2 | 3 | 2 | [0:10,1:20,2:30,3:40,4: ] |
| 7 | enqueue(50) | 2 | 4 | 3 | [0:10,1:20,2:30,3:40,4:50] |
| 8 | enqueue(60) | 2 | 0 | 4 | [0:60,1:20,2:30,3:40,4:50] (rear wraps) |

Notice at step 8: `rear = (4+1)%5 = 0`, and we overwrite index 0 (which was previously 10, already logically removed). This demonstrates memory reuse.

**Full condition:** At step 7, count = 3, not full. At step 8, count = 4, still not full. If we enqueue one more, count becomes 5, and `is_full()` returns true.

---

## 8. Comparison with Other Queues

| Feature | Linear Queue (Array) | Circular Queue | Deque | Priority Queue |
|---------|----------------------|----------------|-------|----------------|
| **Memory reuse** | No | Yes | Yes (both ends) | No (if array) |
| **False overflow** | Yes | No | No | Yes (if array) |
| **Fixed capacity** | Yes | Yes | Yes | Yes (often) |
| **Enqueue time** | O(1) | O(1) | O(1) (push) | O(log n) |
| **Dequeue time** | O(1) | O(1) | O(1) (pop) | O(log n) |
| **Peek time** | O(1) | O(1) | O(1) | O(1) |
| **Ordering** | FIFO | FIFO | Both | Priority |
| **Complexity** | Simple | Moderate | Moderate | High |
| **Use cases** | Basic buffering | Circular buffers, streaming | Sliding window, palindrome | Task scheduling, Dijkstra |

**Advantages of Circular Queue over Linear Queue:**
- No memory wastage.
- Efficient use of fixed array.
- Operations remain O(1).

**Disadvantages:**
- Fixed capacity (like linear array).
- Slightly more complex pointer arithmetic.
- Need to handle wrap-around carefully.

---

## 9. Real‑World Applications

### 9.1 Streaming Media Buffers

Audio and video players use circular buffers to store incoming data while processing. When the buffer is full, new data overwrites the oldest (if the player is lagging), or the player waits. The circular queue ensures continuous data flow without shifting.

### 9.2 Keyboard Buffer

Key presses are stored in a circular buffer. The keyboard driver enqueues keystrokes, and the operating system dequeues them for processing. This prevents loss of keystrokes when the system is busy.

### 9.3 Network Routers (Packet Buffers)

Routers use circular queues to buffer incoming packets when the output link is congested. The wrap-around allows efficient use of memory.

### 9.4 Producer‑Consumer Systems

A circular buffer is a classic solution to the producer‑consumer problem. Producers write to the buffer, consumers read from it. The circular nature allows reuse of space without locking.

### 9.5 Operating System Task Schedulers

Some schedulers use circular queues to manage ready processes (round‑robin). The scheduler dequeues a process, runs it for a time slice, and if not finished, enqueues it again at the rear.

### 9.6 Embedded Systems and Sensor Data

In embedded systems, sensor readings are often stored in a circular buffer to maintain a rolling window of recent data. This allows efficient analysis without storing unlimited data.

### 9.7 Circular Logging

Log files can be stored in a circular buffer to keep only the most recent logs, discarding old ones when space runs out.

**In all these applications, the circular queue is chosen because it provides O(1) operations, reuses memory, and avoids the overhead of shifting or dynamic resizing.**

---

## 10. Debugging Masterclass

### Common Mistakes and How to Fix Them

#### Mistake 1: Wrong Modulo Calculation

**Bug:** Using `rear = rear + 1` without modulo, leading to index out of bounds.

**Fix:** Always use `% capacity`.

#### Mistake 2: Incorrect Full Condition (when using count)

**Bug:** Checking `rear == capacity-1` as in linear queue.

**Fix:** Use `count == capacity`.

#### Mistake 3: Incorrect Empty Condition

**Bug:** Checking `front == rear` for emptiness.

**Fix:** Use `count == 0` or `front == -1` (if you don't use count).

#### Mistake 4: Forgetting Wrap‑Around for Front

**Bug:** Front index not wrapped after dequeue.

**Fix:** Use `front = (front + 1) % capacity`.

#### Mistake 5: Not Resetting Pointers After Last Element

**Bug:** After dequeueing the last element, `front` and `rear` still point to that index, causing confusion.

**Fix:** Set `front = rear = -1` when `count == 1` before decrementing.

#### Mistake 6: Off‑by‑One in Display Loop

**Bug:** Displaying `count+1` elements or using wrong starting index.

**Fix:** Iterate exactly `count` times, starting at `front`.

#### Mistake 7: Enqueue After Full

**Bug:** Not checking `is_full()`, leading to overwriting existing data.

**Fix:** Always raise an exception or handle appropriately.

### Debugging Strategy

1. **Print state after each operation:** Show `front`, `rear`, `count`, and the array.
2. **Use a small test case** with wrap‑around.
3. **Check invariants:**
   - If `count == 0`, `front == rear == -1`.
   - If `count > 0`, `front` and `rear` are valid indices.
   - `0 <= front < capacity`, `0 <= rear < capacity`.
4. **Trace with a table** like we did in this chapter.

---

## 11. Interview Preparation

### Beginner Questions

1. What is a circular queue? How does it differ from a linear queue?
2. Why do we need a circular queue? What problem does it solve?
3. How do you check if a circular queue is empty or full?
4. Explain the modulo operation in the context of a circular queue.
5. What are the time complexities of enqueue and dequeue in a circular queue?

### Intermediate Questions

1. Implement a circular queue using an array in your favorite language.
2. How would you handle dynamic resizing of a circular queue?
3. What are the trade-offs between using a count variable versus using only two pointers?
4. Write a function to reverse a circular queue.
5. How can you implement a circular queue using a linked list? (That would be a circular linked list.)

### Advanced Questions

1. Design a thread‑safe circular queue for a multi‑producer, multi‑consumer scenario.
2. How would you implement a circular queue that supports both enqueue and dequeue in O(1) with a dynamically growing capacity?
3. Explain how the circular queue is used in the Linux kernel's `kfifo` implementation.
4. Given a circular queue, how would you compute the number of free slots without using a count variable?
5. How to handle overflow in a real‑time system where you cannot drop data? (Possible solutions: blocking, overwriting oldest, or using a larger buffer.)

### FAANG‑Style Conceptual Questions

- **Amazon:** Design a system for a real‑time stock ticker that uses a circular buffer to store the last N prices.
- **Google:** Implement a circular buffer that can be used for audio streaming; handle underflow and overflow gracefully.
- **Microsoft:** How would you use a circular queue to manage a pool of worker threads?

### Coding Questions

1. Implement a circular queue class with all operations.
2. Write a function that prints all elements of a circular queue in order, starting from the front.
3. Given a circular queue, find the maximum element without using extra space.
4. Implement a `k`‑buffer: a circular queue that keeps only the last `k` elements.

### Dry‑Run Questions

Trace the following sequence on a circular queue of capacity 4:
`enqueue(1)`, `enqueue(2)`, `enqueue(3)`, `dequeue()`, `enqueue(4)`, `enqueue(5)`, `dequeue()`, `enqueue(6)`.
Show front, rear, count, and array after each step.

---

## 12. Practice Section

### Concept Questions (MCQs)

1. In a circular queue, the rear pointer moves:
   a) forward only
   b) backward only
   c) in a circular fashion
   d) not at all

2. Which condition indicates that a circular queue is full (using a count variable)?
   a) `rear == capacity - 1`
   b) `front == rear`
   c) `count == capacity`
   d) `front == -1`

3. The primary advantage of a circular queue over a linear queue is:
   a) Faster operations
   b) Dynamic resizing
   c) Reuse of memory
   d) Simpler implementation

### Fill in the Blanks

- The index after `capacity-1` in a circular queue is `_______`.
- If a circular queue has `count = 0`, then `front` and `rear` are both `_______`.
- To move the rear pointer, we use `rear = (rear + 1) % _______`.

### Predict the Output

Given a circular queue of capacity 5, initially empty. Perform the operations:
`enqueue(5)`, `enqueue(10)`, `dequeue()`, `enqueue(15)`, `enqueue(20)`, `dequeue()`, `enqueue(25)`, `enqueue(30)`.
What is the content of the queue (front to rear)?

### Dry‑Run Exercises

- Perform the sequence from the interview section and draw the array at each step.
- Write a trace table for a sequence that includes wrap‑around.

### Debugging Exercises

Given the following buggy code, find the errors:
```python
class CircularQueue:
    def __init__(self, cap):
        self.arr = [0]*cap
        self.front = 0
        self.rear = 0
        self.count = 0
    def enqueue(self, item):
        if self.count == len(self.arr):
            print("Full")
            return
        self.arr[self.rear] = item
        self.rear += 1
        self.count += 1
```
What is wrong? How would you fix it?

### Coding Exercises

1. Implement a circular queue that dynamically doubles its capacity when full.
2. Write a function `is_palindrome(s)` using a circular queue and a stack.
3. Implement a `CircularQueue` class that supports `__len__` and `__iter__` methods.

### Challenge Problems

1. **Circular Buffer with Overwrite:** Implement a circular queue that, when full, overwrites the oldest element (i.e., it always keeps the most recent N items).
2. **Thread‑Safe Circular Queue:** Implement a circular queue using Python's `threading` and `queue` modules (or use locks) for concurrent access.
3. **Circular Queue Using Two Pointers Only:** Implement a circular queue without a `count` variable (use one empty slot to distinguish full/empty).

### Mini Projects

1. **Music Playlist:** Use a circular queue to store a playlist of songs. Allow adding and removing songs, and skipping to the next song (wrap around).
2. **CPU Task Scheduler:** Simulate a round‑robin scheduler. Each task has a burst time. Use a circular queue to manage ready tasks.
3. **Circular Log Buffer:** Implement a logger that stores the last N log messages in a circular buffer. Provide methods to add and retrieve logs.

---

## 13. Revision

### Chapter Summary

- The linear queue suffers from false overflow: it cannot reuse empty slots at the front.
- The circular queue treats the array as a circle, using modulo arithmetic to wrap pointers.
- We use a `count` variable to easily check empty/full conditions.
- Enqueue: `rear = (rear + 1) % capacity` (or set to 0 if empty).
- Dequeue: `front = (front + 1) % capacity` (or reset if last element).
- All operations are O(1).
- Circular queues are widely used in buffering, streaming, and scheduling.

### One‑Page Cheat Sheet

```python
class CircularQueue:
    def __init__(self, cap):
        self.cap = cap
        self.arr = [None]*cap
        self.front = self.rear = -1
        self.count = 0

    def is_empty(self): return self.count == 0
    def is_full(self): return self.count == self.cap

    def enqueue(self, item):
        if self.is_full(): raise OverflowError
        if self.is_empty(): self.front = self.rear = 0
        else: self.rear = (self.rear + 1) % self.cap
        self.arr[self.rear] = item
        self.count += 1

    def dequeue(self):
        if self.is_empty(): raise IndexError
        item = self.arr[self.front]
        if self.count == 1: self.front = self.rear = -1
        else: self.front = (self.front + 1) % self.cap
        self.count -= 1
        return item
```

### Important Formulas

- Next index: `(current + 1) % capacity`
- Empty: `count == 0`
- Full: `count == capacity`

### Mind Map (ASCII)

```
                Circular Queue
                /             \
        FIFO Principle    Wrap-around
        /        \          /        \
    Enqueue     Dequeue    Modulo   Memory reuse
    (rear)      (front)    (%)     no wastage
```

### Common Mistakes Checklist

- [ ] Forgetting to wrap rear on enqueue.
- [ ] Forgetting to wrap front on dequeue.
- [ ] Not updating `count` correctly.
- [ ] Not resetting `front` and `rear` when queue becomes empty.
- [ ] Using `front == rear` to check full/empty without `count`.
- [ ] Off‑by‑one in display loop.
- [ ] Not handling overflow/underflow exceptions.

---

## Final Words

Congratulations! You have now mastered the circular queue – a brilliant solution to a fundamental problem in data structures. You understand why it exists, how it works, and how to implement it. Remember, the circular queue is not just an academic exercise; it is a workhorse in countless systems, from your keyboard to streaming video.

As you continue your journey, keep in mind the importance of efficient memory management and the elegance of using simple arithmetic to solve complex problems.

Happy coding!

---

*End of Chapter*