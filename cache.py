#from node import Node
#from handler import Handler


class CacheStruct:

    def __init__(self, node, handler):
        self.node = node
        self.handler = handler   ###### the copy of handler when it proccessed the node



class QNode:

    def __init__(self, key, value: CacheStruct):
        self.key = key
        self.value: CacheStruct = value
        self.prev = None
        self.next = None

    def __str__(self):
        return "(%s, %s)" % (self.key, self.value)

class LRUCache:

    def __init__(self, capacity: int=128):

        self.mapping = {}

        # No explicit doubly linked queue here (you may create one yourself)
        self.head = None
        self.end = None

        self.capacity = capacity
        self.current_size = 0

    def get(self, key: int) -> QNode:
        node = self.mapping.get(key)
        if not node:
            return None
        if self.head == node:
            return node
        self._remove(node)
        self._set_head(node)
        return node

    # TODO wrapper for value getter
    def get_value(self, key) -> CacheStruct:
        node = self.get(key)
        return node.value if node else None

    def set(self, key, value: CacheStruct):
        if key in self.mapping:
            node = self.mapping[key]
            node.value = value
            if self.head != node:
                self._remove(node)
                self._set_head(node)
        else:
            new_node = QNode(key, value)
            if self.current_size == self.capacity:
                del self.mapping[self.end.key]
                self._remove(self.end)
            self._set_head(new_node)
            self.mapping[key] = new_node

    def _set_head(self, node):
        if not self.head:
            self.head = node
            self.end = node
        else:
            node.prev = self.head
            self.head.next = node
            self.head = node
        self.current_size += 1


    def _remove(self, node):
        if not self.head:
            return

        # removing the node from somewhere in the middle; update pointers
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev

        # head = end = node
        if not node.next and not node.prev:
            self.head = None
            self.end = None

        # if the node we are removing is the one at the end, update the new end
        # also not completely necessary but set the new end's previous to be NULL
        if self.end == node:
            self.end = node.next
            self.end.prev = None
        self.current_size -= 1
        return node


    #def print_elements(self):
        #n = self.head
        #print("[head = %s, end = %s]" % (self.head, self.end), end=" ")
        #while n:
            #print("%s -> " % (n), end = "")
            #n = n.prev

if __name__ == "__main__":
    cache = LRUCache()