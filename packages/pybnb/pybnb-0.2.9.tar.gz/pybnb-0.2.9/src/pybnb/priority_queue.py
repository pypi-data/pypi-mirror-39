"""
A collection of priority queue implementations that can be
used by the dispatcher.

Copyright by Gabriel A. Hackebeil (gabe.hackebeil@gmail.com).
"""

import collections
import heapq

from pybnb.common import (minimize,
                          maximize)
from pybnb.node import Node

from sortedcontainers import SortedList

class _NoThreadingMaxPriorityFirstQueue(object):
    """A simple priority queue implementation that is not
    thread safe. When the queue is not empty, the item with
    the highest priority is next.

    This queue implementation is not allowed to store None.
    """
    requires_priority = True

    def __init__(self):
        self._count = 0
        self._heap = []

    def size(self):
        """Returns the size of the queue."""
        return len(self._heap)

    def put(self, item, priority, _push_=heapq.heappush):
        """Puts an item into the queue with the given
        priority. Items placed in the queue may not be
        None. This method returns a unique counter associated
        with each put."""
        assert item is not None
        cnt = self._count
        self._count += 1
        _push_(self._heap, (-priority, cnt, item))
        return cnt

    def get(self, _pop_=heapq.heappop):
        """Removes and returns the highest priority item in
        the queue, where ties are broken by the order items
        were placed in the queue. If the queue is empty,
        returns None."""
        if len(self._heap) > 0:
            return _pop_(self._heap)[2]
        else:
            return None

    def next(self):
        """Returns, without modifying the queue, a tuple of
        the form (cnt, item), where item is highest priority
        entry in the queue and cnt is the unique counter
        assigned to it when it was added to the queue.

        Raises
        ------
        IndexError
            If the queue is empty.
        """
        try:
            return self._heap[0][1:]
        except IndexError:
            raise IndexError("The queue is empty")

    def filter(self, func, include_counters=False):
        """Removes items from the queue for which
        `func(item)` returns False. The list of items
        removed is returned. If `include_counters` is set to
        True, values in the returned list will have the form
        (cnt, item), where cnt is a unique counter that was
        created for the item when it was added to the
        queue."""
        heap_new = []
        removed = []
        for priority, cnt, item in self._heap:
            if func(item):
                heap_new.append((priority, cnt, item))
            elif not include_counters:
                removed.append(item)
            else:
                removed.append((cnt,item))
        heapq.heapify(heap_new)
        self._heap = heap_new
        return removed

    def items(self):
        """Iterates over the queued items in arbitrary order
        without modifying the queue."""
        for _,_,item in self._heap:
            yield item

class _NoThreadingFIFOQueue(object):
    """A simple first-in, first-out queue implementation
    that is not thread safe.

    This queue implementation is not allowed to store None.
    """
    requires_priority = False

    def __init__(self):
        self._count = 0
        self._deque = collections.deque()

    def size(self):
        """Returns the size of the queue."""
        return len(self._deque)

    def put(self, item):
        """Puts item at the end of the queue. Items placed
        in the queue may not be None. This method returns a
        unique counter associated with each put."""
        assert item is not None
        cnt = self._count
        self._count += 1
        self._deque.append((cnt, item))
        return cnt

    def get(self):
        """Removes and returns the highest priority item in
        the queue, where ties are broken by the order items
        were placed in the queue. If the queue is empty,
        returns None."""
        if len(self._deque) > 0:
            return self._deque.popleft()[1]
        else:
            return None

    def next(self):
        """Returns, without modifying the queue, a tuple of
        the form (cnt, item), where item is highest priority
        entry in the queue and cnt is the unique counter
        assigned to it when it was added to the queue.

        Raises
        ------
        IndexError
            If the queue is empty.
        """
        try:
            return self._deque[0]
        except IndexError:
            raise IndexError("The queue is empty")

    def filter(self, func, include_counters=False):
        """Removes items from the queue for which
        `func(item)` returns False. The list of items
        removed is returned. If `include_counters` is set to
        True, values in the returned list will have the form
        (cnt, item), where cnt is a unique counter that was
        created for the item when it was added to the
        queue."""
        deque_new = collections.deque()
        removed = []
        for cnt, item in self._deque:
            if func(item):
                deque_new.append((cnt, item))
            elif not include_counters:
                removed.append(item)
            else:
                removed.append((cnt,item))
        self._deque = deque_new
        return removed

    def items(self):
        """Iterates over the queued items in arbitrary order
        without modifying the queue."""
        for _,item in self._deque:
            yield item

class IPriorityQueue(object):
    """The abstract interface for priority queues that store
    node data for the dispatcher."""

    def size(self):                               #pragma:nocover
        """Returns the size of the queue."""
        raise NotImplementedError

    def put(self, data):                          #pragma:nocover
        """Puts a node data item in the queue, possibly
        updating the value of :attr:`queue_priority
        <pybnb.node.Node.queue_priority>`, depending on the
        queue implementation. This method returns a unique
        counter associated with each put."""
        raise NotImplementedError()

    def get(self):                                #pragma:nocover
        """Returns the next data item in the queue. If the
        queue is empty, returns None."""
        raise NotImplementedError()

    def bound(self):                              #pragma:nocover
        """Returns the weakest bound of all data items in the
        queue. If the queue is empty, returns None."""
        raise NotImplementedError()

    def filter(self, func):                       #pragma:nocover
        """Removes items from the queue for which
        `func(item)` returns False. The list of items
        removed is returned. If the queue is empty or no
        items are removed, the returned list will be
        empty."""
        raise NotImplementedError()

    def items(self):                              #pragma:nocover
        """Iterates over the queued items in arbitrary order
        without modifying the queue."""
        raise NotImplementedError()

class WorstBoundFirstPriorityQueue(IPriorityQueue):
    """A priority queue implementation that serves nodes
    with the worst bound first.

    Parameters
    ----------
    sense : {:obj:`minimize <pybnb.common.minimize>`, :obj:`maximize <pybnb.common.maximize>`}
        The objective sense for the problem.
    """

    def __init__(self, sense):
        assert sense in (minimize, maximize)
        self._sense = sense
        self._queue = _NoThreadingMaxPriorityFirstQueue()

    def size(self):
        return self._queue.size()

    def put(self, data):
        bound = Node._extract_bound(data)
        if self._sense == minimize:
            priority = -bound
        else:
            priority = bound
        Node._insert_queue_priority(data, priority)
        return self._queue.put(data, priority)

    def get(self):
        return self._queue.get()

    def bound(self):
        try:
            _,data = self._queue.next()
            bound = Node._extract_bound(data)
            priority = Node._extract_queue_priority(data)
            if self._sense == minimize:
                assert bound == -priority
            else:
                assert bound == priority
            return bound
        except IndexError:
            return None

    def filter(self, func):
        return self._queue.filter(func)

    def items(self):
        return self._queue.items()

class CustomPriorityQueue(IPriorityQueue):
    """A priority queue implementation that can handle
    custom node priorities. It uses an additional data
    structure to reduce the amount of time it takes to
    compute a queue bound.

    Parameters
    ----------
    sense : {:obj:`minimize <pybnb.common.minimize>`, :obj:`maximize <pybnb.common.maximize>`}
        The objective sense for the problem.
    """

    def __init__(self,
                 sense,
                 _queue_type_=_NoThreadingMaxPriorityFirstQueue):
        assert sense in (minimize, maximize)
        self._sense = sense
        self._queue = _queue_type_()
        self._sorted_by_bound = SortedList()

    def size(self):
        return self._queue.size()

    def put(self, data):
        bound = Node._extract_bound(data)
        if self._queue.requires_priority:
            if not Node._has_queue_priority(data):
                raise ValueError("A node queue priority is required")
            priority = Node._extract_queue_priority(data)
            cnt = self._queue.put(data, priority)
        else:
            cnt = self._queue.put(data)
        if self._sense == maximize:
            self._sorted_by_bound.add((-bound, cnt, data))
        else:
            self._sorted_by_bound.add((bound, cnt, data))
        return cnt

    def get(self):
        if self._queue.size() > 0:
            cnt,data_ = self._queue.next()
            assert type(cnt) is int
            data = self._queue.get()
            assert data_ is data
            bound = Node._extract_bound(data)
            if self._sense == maximize:
                self._sorted_by_bound.remove((-bound, cnt, data))
            else:
                self._sorted_by_bound.remove((bound, cnt, data))
            return data
        else:
            return None

    def bound(self):
        try:
            return Node._extract_bound(self._sorted_by_bound[0][2])
        except IndexError:
            return None

    def filter(self, func):
        removed = []
        for cnt, data in self._queue.filter(func,
                                            include_counters=True):
            removed.append(data)
            bound = Node._extract_bound(data)
            if self._sense == maximize:
                self._sorted_by_bound.remove((-bound, cnt, data))
            else:
                self._sorted_by_bound.remove((bound, cnt, data))
        return removed

    def items(self):
        return self._queue.items()

class BestObjectiveFirstPriorityQueue(CustomPriorityQueue):
    """A priority queue implementation that serves nodes
    with the best objective first.

    sense : {:obj:`minimize <pybnb.common.minimize>`, :obj:`maximize <pybnb.common.maximize>`}
        The objective sense for the problem.
    """

    def put(self, data):
        objective = Node._extract_objective(data)
        if self._sense == minimize:
            priority = -objective
        else:
            priority = objective
        Node._insert_queue_priority(data, priority)
        return super(BestObjectiveFirstPriorityQueue, self).put(data)

class BreadthFirstPriorityQueue(CustomPriorityQueue):
    """A priority queue implementation that serves nodes in
    breadth-first order.

    sense : {:obj:`minimize <pybnb.common.minimize>`, :obj:`maximize <pybnb.common.maximize>`}
        The objective sense for the problem.
    """

    def put(self, data):
        depth = Node._extract_tree_depth(data)
        assert depth >= 0
        Node._insert_queue_priority(data, -depth)
        return super(BreadthFirstPriorityQueue, self).put(data)

class DepthFirstPriorityQueue(CustomPriorityQueue):
    """A priority queue implementation that serves nodes in
    depth-first order.

    sense : {:obj:`minimize <pybnb.common.minimize>`, :obj:`maximize <pybnb.common.maximize>`}
        The objective sense for the problem.
    """

    def put(self, data):
        depth = Node._extract_tree_depth(data)
        assert depth >= 0
        Node._insert_queue_priority(data, depth)
        return super(DepthFirstPriorityQueue, self).put(data)

class FIFOQueue(CustomPriorityQueue):
    """A priority queue implementation that serves nodes in
    first-in, first-out order.

    sense : {:obj:`minimize <pybnb.common.minimize>`, :obj:`maximize <pybnb.common.maximize>`}
        The objective sense for the problem.
    """

    def __init__(self, sense):
        super(FIFOQueue, self).__init__(
            sense,
            _queue_type_=_NoThreadingFIFOQueue)

    def put(self, data):
        cnt = super(FIFOQueue, self).put(data)
        Node._insert_queue_priority(data, -cnt)
        return cnt
