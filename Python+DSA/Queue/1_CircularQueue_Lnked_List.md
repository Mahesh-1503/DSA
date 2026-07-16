# Circular Queue Using Linked List – A Comprehensive Textbook Chapter

---

## 1. Introduction: Why Another Implementation?

We have already mastered the **array-based circular queue**. It solved the false overflow problem by wrapping the `front` and `rear` pointers around using modular arithmetic.

**But wait** – there was a catch. The array-based circular queue has a **fixed capacity**. What if we don't know how many elements we need to store? What if the queue needs to grow and shrink dynamically?

Imagine a bustling airport security checkpoint. Sometimes it’s empty, sometimes it’s packed with hundreds of passengers. If we allocated an array for 500 passengers, we waste memory during off-peak hours. If we allocated for only 100, the queue overflows during peak hours.

This is where the **Circular Queue using a Linked List** shines. It offers the same FIFO ordering and circular reuse of pointers, but it is **dynamically sized** – it grows and shrinks as needed, never wasting memory and never suffering from a hard capacity limit.

In this chapter, we will build a circular queue from scratch using a **circular singly linked list**. We will keep the `front` and `rear` pointers, but instead of indices, we use node references. The “circle” is formed by connecting the `next` pointer of the last node back to the first node.

---

## 2. Why a Linked List? (The WHY)

Let’s compare the two implementations side-by-side in our minds.

| Feature | Array-Based Circular Queue | Linked-List-Based Circular Queue |
| :--- | :--- | :--- |
| **Capacity** | Fixed (must be declared upfront) | Dynamic (grows as needed) |
| **Memory Usage** | Always occupies `capacity` blocks | Occupies exactly `n` nodes (where `n` is current size) |
| **Overflow** | Occurs when `count == capacity` | **Never** occurs (except system memory exhaustion) |
| **False Overflow** | Solved by wrap-around | Inherently solved (no fixed array) |
| **Pointer Arithmetic** | Uses modulo `%` | Uses `next` references |
| **Cache Locality** | Excellent (contiguous memory) | Poor (nodes are scattered in heap) |
| **Memory Overhead** | Very low (just array and two integers) | Higher (each node stores a `next` pointer) |

### The Core Motivation
The linked-list implementation gives us the **freedom** to handle unpredictable data flows. It is the go-to choice in embedded systems, event loops, and real-time applications where the number of items cannot be predetermined.

---

## 3. Building Intuition with Analogies

### Analogy 1: The Round Table with Movable Chairs
Imagine a round table where guests sit in chairs. New guests bring their own chair and sit down. The waiter (the `front`) always serves the person whose chair is at a specific spot. When a guest leaves, they take their chair with them. The table itself has no fixed number of chairs – it grows and shrinks dynamically. The circle is maintained because the last guest’s chair is always placed right next to the first guest’s chair.

- **Front** = the first guest to be served.
- **Rear** = the last guest who arrived.
- **Wrapping** = the circular link between the last and first guest.

### Analogy 2: A Conveyor Belt with Modular Cartridges
Instead of a fixed belt with slots, imagine a conveyor belt where you can attach new cartridges onto the end. The belt is a loop – the last cartridge always connects to the first. To remove an item, you detach the first cartridge and the belt automatically reconnects the last cartridge to the new first one.

> **Think before reading further:** In a linked-list circular queue, what does the “circular” connection actually look like when we have only **one** element? Can it still be circular?

**Answer:** Yes! A single node is considered circular because its `next` pointer points back to itself. This is the base case that makes all operations consistent.

---

## 4. The Core Structure (The WHAT)

A circular queue using a linked list is built with two components:

### 4.1 The Node
Each node stores:
- `data` – the actual value
- `next` – a reference to the next node in the list

```text
+-------+--------+
| data  |  next  |
+-------+--------+
```

### 4.2 The Queue Class
We maintain three variables:
- `front` – pointer to the first node (the one to be dequeued).
- `rear` – pointer to the last node (where new nodes are added).
- `count` – number of elements currently in the queue.

### 4.3 The Circular Invariant
In a **circular** linked list, the **tail’s `next` pointer always points to the head**.
- When the queue is empty: `front == rear == None`.
- When the queue has 1 node: `front == rear` and `rear.next == front` (self-circular).
- When the queue has multiple nodes: `front != rear` and `rear.next == front`.

---

## 5. Memory Representation (ASCII Visualizations)

### 5.1 Empty Queue
```text
front = None
rear  = None
count = 0
```

### 5.2 Queue with One Element (10)
```text
front --> [ 10 | next ]  <-- rear
              ↑_________|
rear.next == front (the node points to itself)
```

### 5.3 Queue with Three Elements (10, 20, 30)
```text
front --> [ 10 | next ] --> [ 20 | next ] --> [ 30 | next ] --,
              ↑                                                     |
              |___________________________________________________|
rear points to the last node, and rear.next == front.
```

### 5.4 After Dequeue (removing 10)
```text
front --> [ 20 | next ] --> [ 30 | next ] --,
              ↑                                |
              |________________________________|
rear still points to 30, and rear.next == front (which is now 20).
```

Notice how the circular link is seamlessly updated by just changing the `next` pointer of the rear node.

---

## 6. Operations – Step by Step

We will now teach every operation using the proven pedagogical framework: **Problem → Intuition → Visualization → Pseudo → Python → Dry Run → Complexity**.

---

### 6.1 Create an Empty Circular Queue

**Problem:** Initialize a queue with no elements, ready for operations.

**Intuition:** We simply set `front = rear = None` and `count = 0`. No memory is allocated upfront.

**ASCII:**
```text
+------------+
| front: None|
| rear : None|
| count: 0   |
+------------+
```

**Python Implementation:**
```python
from typing import Optional

class Node:
    """A single node in the circular linked list."""
    def __init__(self, data: int):
        self.data = data
        self.next: Optional['Node'] = None

class CircularQueueLinkedList:
    """Circular queue implemented using a circular singly linked list."""
    
    def __init__(self):
        self.front: Optional[Node] = None  # points to the first node
        self.rear: Optional[Node] = None   # points to the last node
        self.count: int = 0                # current number of elements
```

**Complexity:** O(1) time, O(1) space.

---

### 6.2 isEmpty()

**Problem:** Check if the queue has no elements.

**Intuition:** If `front == None` (or `count == 0`), it’s empty.

**Pseudo:**
```
isEmpty():
    return front == None
```

**Python:**
```python
def is_empty(self) -> bool:
    """Return True if the queue is empty."""
    return self.front is None
```

**Complexity:** O(1).

---

### 6.3 isFull() – The Special Case

**Problem:** Check if the queue is full.

**Intuition:** In a linked-list implementation, the queue is **never full** (assuming infinite heap memory). So we return `False` always. This is a fundamental advantage over the array version.

**Python:**
```python
def is_full(self) -> bool:
    """Linked-list queue never gets full (except memory exhaustion)."""
    return False  # Always false
```

---

### 6.4 Enqueue (Add Element)

**Problem:** Add an element to the rear of the circular queue.

**Intuition:** 
- Create a new node with the given data.
- If the queue is **empty**, the new node is both `front` and `rear`. Its `next` must point to itself (to form the circle).
- If the queue is **non-empty**, link the current `rear` to the new node, make the new node the new `rear`, and set its `next` to `front` to maintain the circle.
- Increment `count`.

**Prediction Question:** What happens to `rear.next` when we enqueue into an empty queue? Think before reading...

**Answer:** `rear.next` is set to `rear` itself (i.e., `new_node.next = new_node`). This makes the circle complete even with a single node.

**Visualization (ASCII):**

**Before (empty):**
```text
front = None, rear = None
```

**After enqueue(10):**
```text
front --> [ 10 | next ]  <-- rear
              ↑_________|
rear.next == front (self-loop)
```

**After enqueue(20):**
```text
front --> [ 10 | next ] --> [ 20 | next ] --,
                                      ↑       |
                                      |_______|
rear.next == front
```

**Algorithm:**
1. Create `new_node = Node(item)`.
2. If `is_empty()`:
   - Set `front = rear = new_node`.
   - Set `rear.next = front` (self-circular).
3. Else:
   - Set `rear.next = new_node`.
   - Set `rear = new_node`.
   - Set `rear.next = front` (maintain circle).
4. Increment `count`.

**Python Implementation:**
```python
def enqueue(self, item: int) -> None:
    """Add an item to the rear of the queue."""
    new_node = Node(item)
    if self.is_empty():
        self.front = self.rear = new_node
        self.rear.next = self.front  # circular link for single node
    else:
        # Link the current rear to the new node
        self.rear.next = new_node
        # Move rear to the new node
        self.rear = new_node
        # Maintain the circle: rear points to front
        self.rear.next = self.front
    self.count += 1
```

**Driver Code:**
```python
cq = CircularQueueLinkedList()
cq.enqueue(10)
cq.enqueue(20)
cq.enqueue(30)
print(cq.front.data)  # Should be 10
print(cq.rear.data)   # Should be 30
```

**Expected Output:**
```
10
30
```

**Output Explanation:** `front` points to the first node (10), `rear` points to the last node (30). The circle is intact.

**Memory State (After 3 enqueues):**
```text
front --> [10|next] --> [20|next] --> [30|next] --,
                                      ↑             |
                                      |_____________|
```

**Dry Run (Trace Table):**
| Step | Operation | front | rear | count | Circular Link Check |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 0 | init | None | None | 0 | - |
| 1 | enqueue(10) | Node(10) | Node(10) | 1 | rear.next == front (self) |
| 2 | enqueue(20) | Node(10) | Node(20) | 2 | rear.next == front (Node(10)) |
| 3 | enqueue(30) | Node(10) | Node(30) | 3 | rear.next == front (Node(10)) |

**Complexity:** Time O(1), Space O(1) per node.

**Edge Cases:**
- Enqueue on an empty queue (must handle self-loop).
- Enqueue on a queue of any size (just updates `rear` and `rear.next`).

**Common Mistakes:**
- Forgetting to set `rear.next = front` when the queue is non-empty. If you forget, the list becomes a normal linked list (broken circle).
- Using `rear.next = new_node` but forgetting to update `rear = new_node`.
- Not handling the self-loop for the first element.

**Debugging Tips:**
- After every enqueue, verify `rear.next is front`. If `rear.next != front`, the circular invariant is broken.
- Print `front.data` and `rear.data` to confirm correct links.

---

### 6.5 Dequeue (Remove Element)

**Problem:** Remove and return the element at the front of the queue.

**Intuition:**
- If empty, raise `IndexError`.
- Store the data from the `front` node.
- If this is the **only node** (`front == rear`):
  - Set `front = rear = None`.
- Else:
  - Move `front` forward: `front = front.next`.
  - Maintain the circular link: set `rear.next = front`.
- Decrement `count`.
- Return the stored data.

**Prediction Question:** When we remove the last element, what happens to the circular link? Do we need to worry about `rear.next` pointing to a deleted node?

**Answer:** When we remove the last element, we set both `front` and `rear` to `None`. The orphaned node is garbage-collected. The circle is dissolved because there are no nodes left.

**Visualization (ASCII):**

**Before dequeue (queue = [10, 20, 30]):**
```text
front --> [10|next] --> [20|next] --> [30|next] --,
                                      ↑             |
                                      |_____________|
```

**After dequeue() (removing 10):**
```text
front --> [20|next] --> [30|next] --,
                  ↑                    |
                  |____________________|
rear.next == front (now points to 20)
```

**After dequeue() again (removing 20):**
```text
front --> [30|next] --,
              ↑          |
              |__________|
rear == front (single node)
```

**After dequeue() again (removing 30):**
```text
front = None, rear = None
```

**Algorithm:**
1. If `is_empty()`: raise `IndexError`.
2. Save `item = front.data`.
3. If `front == rear` (only one node):
   - `front = rear = None`.
4. Else:
   - `front = front.next`.
   - `rear.next = front` (maintain circle).
5. `count -= 1`.
6. Return `item`.

**Python Implementation:**
```python
def dequeue(self) -> int:
    """Remove and return the front element."""
    if self.is_empty():
        raise IndexError("Queue is empty")
    
    item = self.front.data
    
    if self.front == self.rear:
        # Only one node left
        self.front = None
        self.rear = None
    else:
        # Move front forward
        self.front = self.front.next
        # Maintain the circular link
        self.rear.next = self.front
    
    self.count -= 1
    return item
```

**Driver Code:**
```python
cq = CircularQueueLinkedList()
cq.enqueue(10)
cq.enqueue(20)
cq.enqueue(30)
print(cq.dequeue())  # 10
print(cq.dequeue())  # 20
print(cq.dequeue())  # 30
try:
    cq.dequeue()
except IndexError as e:
    print(e)  # "Queue is empty"
```

**Expected Output:**
```
10
20
30
Queue is empty
```

**Output Explanation:** Each dequeue retrieves the front element and updates the `front` pointer. After the third dequeue, the queue becomes empty, and any further dequeue triggers an exception.

**Dry Run (Trace Table):**
| Step | Operation | front | rear | count | Circular Link Check |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 0 | init | None | None | 0 | - |
| 1 | enqueue(10,20,30) | Node(10) | Node(30) | 3 | rear.next == Node(10) |
| 2 | dequeue() | Node(20) | Node(30) | 2 | rear.next == Node(20) |
| 3 | dequeue() | Node(30) | Node(30) | 1 | rear.next == Node(30) |
| 4 | dequeue() | None | None | 0 | - |
| 5 | dequeue() | None | None | 0 | Raises IndexError |

**Complexity:** Time O(1), Space O(1).

**Edge Cases:**
- Dequeue on an empty queue (must raise).
- Dequeue the only element (must reset to `None`).
- Dequeue when `front` moves around the circle (the `rear.next` update ensures the circle is never broken).

**Common Mistakes:**
- Forgetting to update `rear.next` after moving `front`. If you forget, `rear.next` still points to the old `front`, which is no longer in the queue. This breaks the circle and leads to stale references.
- Not checking `front == rear` before moving `front`. If you move `front` when there is only one node, `front` becomes `None` and `rear` still points to the deleted node.
- Not resetting both `front` and `rear` to `None` when removing the last element.

**Debugging Tips:**
- After every dequeue, assert `rear.next == front` (if the queue is not empty).
- Check `count` and `front`/`rear` values on paper to ensure the circle is preserved.

---

### 6.6 Peek (Front Element)

**Problem:** Return the front element without removing it.

**Intuition:** Return `front.data` if queue is not empty.

**Python:**
```python
def peek(self) -> int:
    """Return the front element without removing it."""
    if self.is_empty():
        raise IndexError("Queue is empty")
    return self.front.data
```

**Complexity:** O(1).

---

### 6.7 Rear (Back Element)

**Problem:** Return the rear element without removing it.

**Intuition:** Return `rear.data` if queue is not empty.

**Python:**
```python
def rear(self) -> int:
    """Return the rear element without removing it."""
    if self.is_empty():
        raise IndexError("Queue is empty")
    return self.rear.data
```

**Complexity:** O(1).

---

### 6.8 Size (Count)

**Problem:** Return the number of elements.

**Intuition:** Return `count`.

**Python:**
```python
def size(self) -> int:
    """Return the current number of elements."""
    return self.count
```

**Complexity:** O(1).

---

### 6.9 Display (Traverse the Queue)

**Problem:** Print all elements from front to rear in order.

**Intuition:** We need to traverse exactly `count` nodes. Starting from `front`, we follow `next` pointers, print each data, and stop after `count` steps.

**Caution:** If we simply loop while `current != self.front`, we might get an infinite loop or miss elements. The safest approach is to loop exactly `count` times.

**Python:**
```python
def display(self) -> None:
    """Print the queue elements from front to rear."""
    if self.is_empty():
        print("Queue is empty")
        return
    
    print("Front -> ", end="")
    current = self.front
    for _ in range(self.count):
        print(current.data, end=" ")
        current = current.next
    print("<- Rear")
```

**Driver Code:**
```python
cq = CircularQueueLinkedList()
cq.enqueue(10)
cq.enqueue(20)
cq.enqueue(30)
cq.display()
```

**Expected Output:**
```
Front -> 10 20 30 <- Rear
```

**Explanation:** The loop iterates `count` times, printing each element and moving to the next. Because the list is circular, `current` will eventually reach the `front` again, but we stop after `count` steps.

**Complexity:** Time O(n), Space O(1).

---

## 7. Complete Production-Quality Code

Here is the entire, fully documented, PEP 8 compliant implementation.

```python
from typing import Optional

class Node:
    """A node in a circular singly linked list."""
    def __init__(self, data: int):
        self.data = data
        self.next: Optional['Node'] = None


class CircularQueueLinkedList:
    """
    A dynamic circular queue implemented using a circular linked list.
    
    Features:
    - FIFO ordering.
    - No fixed capacity (grows dynamically).
    - O(1) enqueue and dequeue operations.
    - Maintains a circular invariant: rear.next == front (when not empty).
    """
    
    def __init__(self):
        self.front: Optional[Node] = None
        self.rear: Optional[Node] = None
        self.count: int = 0

    def is_empty(self) -> bool:
        """Return True if the queue has no elements."""
        return self.front is None

    def is_full(self) -> bool:
        """Return False because linked-list queue never has a fixed capacity."""
        return False

    def enqueue(self, item: int) -> None:
        """Add an element to the rear of the queue."""
        new_node = Node(item)
        if self.is_empty():
            self.front = self.rear = new_node
            self.rear.next = self.front  # self-circular
        else:
            self.rear.next = new_node
            self.rear = new_node
            self.rear.next = self.front  # maintain circularity
        self.count += 1

    def dequeue(self) -> int:
        """Remove and return the front element."""
        if self.is_empty():
            raise IndexError("Queue is empty")
        
        item = self.front.data
        if self.front == self.rear:
            # Only one node left
            self.front = None
            self.rear = None
        else:
            self.front = self.front.next
            self.rear.next = self.front  # update circular link
        
        self.count -= 1
        return item

    def peek(self) -> int:
        """Return the front element without removing it."""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.front.data

    def rear(self) -> int:
        """Return the rear element without removing it."""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.rear.data

    def size(self) -> int:
        """Return the current number of elements."""
        return self.count

    def display(self) -> None:
        """Print all elements from front to rear."""
        if self.is_empty():
            print("Queue is empty")
            return
        
        print("Front -> ", end="")
        current = self.front
        for _ in range(self.count):
            print(current.data, end=" ")
            current = current.next
        print("<- Rear")
```

---

## 8. Internal Working: Pointer Movement Trace

Let’s trace a full sequence on a deeper level to see the pointers in action.

**Sequence:** `enqueue(5)`, `enqueue(15)`, `dequeue()`, `enqueue(25)`, `dequeue()`, `enqueue(35)`, `enqueue(45)`.

**Step-by-Step:**

| Step | Operation | `front` points to | `rear` points to | `rear.next` points to | `count` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 0 | init | None | None | - | 0 |
| 1 | enqueue(5) | Node(5) | Node(5) | Node(5) (self) | 1 |
| 2 | enqueue(15) | Node(5) | Node(15) | Node(5) | 2 |
| 3 | dequeue() | Node(15) | Node(15) | Node(15) (self) | 1 |
| 4 | enqueue(25) | Node(15) | Node(25) | Node(15) | 2 |
| 5 | dequeue() | Node(25) | Node(25) | Node(25) (self) | 1 |
| 6 | enqueue(35) | Node(25) | Node(35) | Node(25) | 2 |
| 7 | enqueue(45) | Node(25) | Node(45) | Node(25) | 3 |

**Key Observation:** In steps 3 and 5, after dequeueing the only element, the queue returns to a single-node self-circular state. In steps 4 and 6, when we enqueue a new element, the circle is expanded: `rear.next` is updated to point back to the `front`.

---

## 9. Comparison: Circular Array vs Circular Linked List

Now that we have mastered both, let’s make a definitive comparison table.

| **Aspect** | **Array-Based Circular Queue** | **Linked-List-Based Circular Queue** |
| :--- | :--- | :--- |
| **Capacity** | Fixed (must know max size beforehand) | Dynamic (grows as needed) |
| **Memory Wastage** | Allocates full capacity even if empty | Allocates only for existing elements |
| **Overflow** | Possible when `count == capacity` | **Impossible** (except heap exhaustion) |
| **False Overflow** | Solved by modulo | Naturally solved (no fixed array) |
| **Enqueue Complexity** | O(1) | O(1) |
| **Dequeue Complexity** | O(1) | O(1) |
| **Cache Locality** | High (contiguous memory) | Low (nodes scattered in heap) |
| **Memory Overhead** | Minimal (just array + 2 ints) | High (each node stores a `next` pointer) |
| **Modulo Arithmetic** | Required (`%`) | Not required (just pointer updates) |
| **Implementation Complexity** | Moderate | Moderate (but pointer management is tricky) |
| **Best Use Case** | High-performance, predictable max size | Variable workload, unknown max size |

---

## 10. Real-World Applications

### 10.1 Embedded Systems (Dynamic Sensor Buffers)
In IoT devices, sensor readings arrive at variable rates. Using a linked-list circular queue allows the device to buffer data without pre-allocating a large array, saving precious memory.

### 10.2 Event Loops in GUI Frameworks
Event-driven applications (e.g., `tkinter`, `Qt`) maintain an event queue. Events are enqueued as they occur (mouse clicks, key presses) and processed in order. Because the number of events is unpredictable, a dynamic circular queue is a perfect fit.

### 10.3 Task Schedulers in Operating Systems
Some OS schedulers use circular linked lists for the ready queue. Processes are enqueued dynamically, and the scheduler uses the circular nature to implement round-robin without fixed size constraints.

### 10.4 Network Packet Buffers (Variable Load)
In routers, traffic can spike unpredictably. A linked-list circular queue can absorb bursts of packets without dropping them due to capacity limits, unlike fixed-size array buffers.

### 10.5 Producer-Consumer (Queue of Jobs)
In a web server, incoming requests are placed in a job queue. The number of requests can vary from zero to millions. A dynamic queue handles this gracefully.

---

## 11. Debugging Masterclass

### Common Bugs and Fixes

#### Bug 1: Broken Circular Invariant (Enqueue)
**Symptom:** After enqueuing multiple items, `rear.next` still points to the old `front` (or `None`), so the list is no longer circular.
**Fix:** Always set `rear.next = front` after updating the `rear` pointer.

#### Bug 2: Dequeueing the Last Element Incorrectly
**Symptom:** After dequeueing the last element, `front` becomes `None` but `rear` still points to the deleted node. The queue is logically empty but pointers are stale.
**Fix:** In the `if self.front == self.rear` block, set **both** `self.front` and `self.rear` to `None`.

#### Bug 3: Infinite Loop in `display()`
**Symptom:** The `display()` method runs forever because we didn't stop after `count` steps.
**Fix:** Always use a `for` loop with `range(self.count)` instead of a `while` loop based on `current != self.front`.

#### Bug 4: Dequeueing on Empty Queue
**Symptom:** `front` is `None`, but the code tries to access `front.data`, leading to `AttributeError`.
**Fix:** Always call `is_empty()` at the start of `dequeue()`.

#### Bug 5: Not Maintaining Circularity after Dequeue
**Symptom:** After dequeueing, `rear.next` still points to the old `front` (which is now gone).
**Fix:** Update `rear.next = self.front` after moving `front` forward.

### Debugging Strategy
1. **Invariant Check:** Insert an assertion at the end of every enqueue and dequeue:
   ```python
   if not self.is_empty():
       assert self.rear.next == self.front
   ```
   This catches broken circles immediately.

2. **Visualize:** Draw the nodes on paper or use a debugger to inspect `front`, `rear`, and `rear.next` step-by-step.

3. **Small Tests:** Test edge cases:
   - Enqueue into empty.
   - Dequeue last element.
   - Enqueue after dequeuing last element.
   - Multiple enqueue/dequeue cycles.

---

## 12. Interview Preparation

### Beginner Questions
1. What is a circular queue implemented with a linked list?
2. How does it differ from an array-based circular queue?
3. How do you check if a linked-list circular queue is empty?
4. What is the time complexity of enqueue and dequeue?
5. Why doesn't a linked-list circular queue have a "full" condition?

### Intermediate Questions
1. Implement a circular queue using a singly linked list in your preferred language.
2. Write a function to reverse the elements of a circular linked queue.
3. How would you find the middle node of a circular queue without using a counter?
4. Explain how the `rear.next` pointer changes when performing multiple enqueue and dequeue operations.

### Advanced Questions
1. **Design a Circular Queue with O(1) size**: Write the code without using a `count` variable. (Hint: Use a sentinel node or rely on `front == rear` with a sentinel to distinguish empty vs full). 
2. **Thread-Safe Implementation**: How would you make this linked-list circular queue thread-safe for a producer-consumer system?
3. **Memory Management**: In languages like C/C++, how would you handle the memory of nodes after dequeue to avoid leaks?
4. **Analytical Question**: What is the worst-case memory fragmentation impact of using a linked-list queue versus an array queue?

### FAANG-Style Scenario
- **Uber/Lyft Ride Queue**: You are designing a ride-matching system. Drivers are enqueued when they become available, and riders request drivers in FIFO order. The number of drivers fluctuates wildly. Which implementation do you choose? Why?
  - **Answer:** The linked-list circular queue is chosen because driver availability is dynamic and unpredictable. Fixed array would either waste memory or overflow.

---

## 13. Practice Section

### Concept Questions (MCQs)
1. In a linked-list circular queue, the `rear.next` pointer always points to:
   a) `None`
   b) The `front` node
   c) The second node
   d) The `rear` node itself (when empty)

2. Which of the following is NOT a benefit of the linked-list circular queue?
   a) Dynamic size
   b) No false overflow
   c) Better cache locality than array
   d) No fixed capacity

3. When dequeuing the only element, we must:
   a) Set `front = rear = None`
   b) Set `front = front.next`
   c) Keep `rear` pointing to the old node
   d) Set `rear.next = None`

### Fill in the Blanks
- The `display` method must iterate exactly `_______` times to avoid infinite loops.
- The base case for a circular linked list is when `front == rear` and `rear.next == _______`.
- To maintain circularity after enqueue, we set `rear.next = _______`.

### Predict the Output
Given the code:
```python
cq = CircularQueueLinkedList()
cq.enqueue(1)
cq.enqueue(2)
cq.dequeue()
cq.enqueue(3)
cq.display()
```
What will be printed?

### Dry-Run Exercise
Trace the following operations on a linked-list circular queue, showing `front`, `rear`, `rear.next`, and `count` after each step:
`enqueue(5)`, `enqueue(10)`, `dequeue()`, `dequeue()`, `enqueue(15)`, `enqueue(20)`.

### Debugging Exercises
Here is a buggy `enqueue` method. Identify and fix the bugs.
```python
def enqueue(self, item):
    new_node = Node(item)
    if self.is_empty():
        self.front = new_node
        self.rear = new_node
    else:
        self.rear.next = new_node
        self.rear = new_node
    self.count += 1
```

### Coding Exercises
1. Implement a method `rotate(k)` that moves the `front` pointer forward by `k` positions without changing the element order.
2. Implement a method `get(index)` that returns the element at the `index`-th position from the front (0-based).
3. Write a function `is_circular(queue)` that verifies the circular invariant (`rear.next == front`) for a given queue.

### Challenge Problem
**Merge Two Circular Queues**: Given two circular linked-list queues `q1` and `q2`, merge them into a single circular queue where all elements of `q1` come before all elements of `q2`. The merged queue must maintain FIFO and circularity. Solve in O(1) time (without iterating through elements) by adjusting pointers.

---

## 14. Revision Section

### Chapter Summary
- The linked-list circular queue solves the fixed-capacity limitation of the array-based circular queue.
- It uses a circular singly linked list where `rear.next == front`.
- Operations are O(1) because we only update pointers.
- The queue is never "full" (unless memory runs out), making it ideal for unpredictable data loads.
- We maintain a `count` variable for O(1) size and easy empty checking.

### One-Page Cheat Sheet
```python
class CircularQueueLinkedList:
    def __init__(self):
        self.front = self.rear = None
        self.count = 0

    def enqueue(self, item):
        new = Node(item)
        if self.is_empty():
            self.front = self.rear = new
            self.rear.next = self.front
        else:
            self.rear.next = new
            self.rear = new
            self.rear.next = self.front
        self.count += 1

    def dequeue(self):
        if self.is_empty(): raise IndexError
        item = self.front.data
        if self.front == self.rear:
            self.front = self.rear = None
        else:
            self.front = self.front.next
            self.rear.next = self.front
        self.count -= 1
        return item
```

### Important Formulas / Invariants
- Empty: `front == None` (or `count == 0`)
- Non-empty: `rear.next == front` (MUST always hold)
- Single node: `front == rear` and `rear.next == front`

### Mind Map (ASCII)

```
           Circular Queue (Linked List)
            /                           \
     FIFO Ordering                 Dynamic Capacity
         |                                |
   front (oldest)                   No fixed limit
   rear  (newest)                   Uses heap memory
         |                                |
   `rear.next == front`             Node with data + next
   (circular invariant)             (pointer overhead)
```

### Common Mistakes Checklist
- [ ] Forgetting to set `rear.next = front` after enqueue (non-empty).
- [ ] Not resetting `front` to `None` when dequeueing the last element.
- [ ] Using `while` loop in `display()` without `count` (infinite loop).
- [ ] Not handling `self.front == self.rear` properly in dequeue.
- [ ] Accessing `front.data` before checking `is_empty()`.
- [ ] `rear.next` still pointing to deleted node after dequeue.

---

## Final Words

You have now conquered the **Circular Queue using a Linked List**. You understand when to use it (dynamic, unpredictable workloads) and how to implement it with pristine pointer logic. This is a powerful tool in the arsenal of any systems programmer, backend engineer, or embedded developer.

Remember: the array version gives you speed and locality; the linked version gives you freedom and flexibility. Choose wisely based on your problem constraints.

As you move forward, try implementing this in a multi-threaded environment or combining it with a priority queue. Keep the circular invariant close to your heart – `rear.next` must always point to `front`!

Happy coding!

---

*End of Chapter*