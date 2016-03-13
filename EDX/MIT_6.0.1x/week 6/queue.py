  """
  Queue class
  """

  class Queue:
      """
      A simple implementation of a FIFO queue.
      """

      def __init__(self):
          """
          Initialize the queue.
          """
          self._items = []

      def __len__(self):
          """
          Return the number of items in the queue.
          """
          return len(self._items)

      def __iter__(self):
          """
          Create an iterator for the queue.
          """
          for item in self._items:
              yield item

      def __str__(self):
          """
          Return a string representation of the queue.
          """
          return str(self._items)

      def insert(self, item):
          """
          Add item to the queue.
          """
          self._items.append(item)

      def remove(self):
          """
          Remove and return the least recently inserted item.
          """
          try:
            return self._items.pop(0)
          except ValueError:
            print "It did raise 'ValueError'!"

      def clear(self):
          """
          Remove all items from the queue.
          """
          self._items = []

