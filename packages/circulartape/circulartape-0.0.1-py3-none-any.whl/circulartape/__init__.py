"""
Circular tape library.

This package implements a "circular tape" -- a doubly-linked list which wraps
around at the end.
"""


class Tape():
    def __init__(self, data, prev=None, next=None):
        self.data = data

        if prev is None and next is None:
            # First node in list.
            self.prev = self.next = self
        elif prev is not None and next is not None:
            self.prev = prev
            self.next = next
        else:
            raise ValueError("either don't specify prev/next, or specify both")

    def _fix_neighbors(self):
        self.next.prev = self
        self.prev.next = self

    def seek(self, n):
        """Seek n nodes clockwise. Negative values seek counterclockwise
        instead."""

        if n == 0:
            return self

        elif n > 0:
            return self.next.seek(n - 1)

        elif n < 0:
            return self.prev.seek(n + 1)

    def insert(self, data):
        """Insert a new node, caontaining the given data, after this node."""

        new = Tape(data, prev=self, next=self.next)
        new._fix_neighbors()

        return new

    def remove(self):
        """Remove this node from the tape."""

        if self.prev == self.next == self:
            raise ValueError("cannot remove last element")

        self.prev.next = self.next
        self.next.prev = self.prev

    def to_list(self):
        """Convert to a list, starting at this node."""
        current = self
        result = []
        while True:
            result.append(current.data)
            current = current.next
            if current is self:
                return result
