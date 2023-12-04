from __future__ import annotations
import json
from typing import List

verbose = False

# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  key      : int,
                  value    : str,
                  toplevel : int,
                  pointers : List[Node] = None):
        self.key      = key
        self.value    = value
        self.toplevel = toplevel
        self.pointers = pointers

# DO NOT MODIFY!
class SkipList():
    def  __init__(self,
                  maxlevel : int,
                  headnode : Node = None,
                  tailnode : Node = None):
        self.headnode  = headnode
        self.tailnode  = tailnode
        self.maxlevel = maxlevel

    # DO NOT MODIFY!
    # Return a reasonable-looking json.dumps of the object with indent=2.
    # We create an list of nodes,
    # For each node we show the key, the value, and the list of pointers and the key each points to.
    def dump(self) -> str:
        currentNode = self.headnode
        nodeList = []
        while currentNode is not self.tailnode:
            pointerList = str([n.key for n in currentNode.pointers])
            nodeList.append({'key':currentNode.key,'value':currentNode.value,'pointers':pointerList})
            currentNode = currentNode.pointers[0]
        pointerList = str([None for n in currentNode.pointers])
        nodeList.append({'key':currentNode.key,'value':currentNode.value,'pointers':pointerList})
        return json.dumps(nodeList,indent = 2)

    # DO NOT MODIFY!
    # Creates a pretty rendition of a skip list.
    # It's vertical rather than horizontal in order to manage different lengths more gracefully.
    # This will never be part of a test but you can put "pretty" as a single line in your tracefile
    # to see what the result looks like.
    def pretty(self) -> str:
        currentNode = self.headnode
        longest = 0
        while currentNode != None:
            if len(str(currentNode.key)) > longest:
                longest = len(str(currentNode.key))
            currentNode = currentNode.pointers[0]
        longest = longest + 2
        pretty = ''
        currentNode = self.headnode
        while currentNode != None:
            lineT = 'Key = ' + str(currentNode.key) + ', Value = ' + str(currentNode.value)
            lineB = ''
            for p in currentNode.pointers:
                if p is not None:
                    lineB = lineB + ('('+str(p.key)+')').ljust(longest)
                else:
                    lineB = lineB + ''.ljust(longest)
            pretty = pretty + lineT
            if currentNode != self.tailnode:
                pretty = pretty + "\n"
                pretty = pretty + lineB + "\n"
                pretty = pretty + "\n"
            currentNode = currentNode.pointers[0]
        return(pretty)

    # DO NOT MODIFY!
    # Initialize a skip list.
    # This constructs the headnode and tailnode each with maximum level maxlevel.
    # Headnode has key -inf, and pointers point to tailnode.
    # Tailnode has key inf, and pointers point to None.
    # Both have value None.
    def initialize(self,maxlevel):
        pointers = [None] * (1+maxlevel)
        tailnode = Node(key = float('inf'),value = None,toplevel = maxlevel,pointers = pointers)
        pointers = [tailnode] * (maxlevel+1)
        headnode = Node(key = float('-inf'),value = None, toplevel = maxlevel,pointers = pointers)
        self.headnode = headnode
        self.tailnode = tailnode
        self.maxlevel = maxlevel

    # Create and insert a node with the given key, value, and toplevel.
    # The key is guaranteed to not be in the skiplist.
    def insert(self, key: int, value: str, toplevel: int):
        update = [None] * (self.maxlevel + 1)
        current = self.headnode

        # Start from the highest level of the skip list
        for i in range(self.maxlevel, -1, -1):
            while current.pointers[i] and current.pointers[i].key < key:
                current = current.pointers[i]
            update[i] = current

        # Reached level 0 and forward pointer to right, which is desired position to insert key.
        current = current.pointers[0]

        if current is None or current.key != key:
            new_node = Node(key, value, toplevel, [None]*(toplevel+1))
            for i in range(toplevel + 1):
                new_node.pointers[i] = update[i].pointers[i]
                update[i].pointers[i] = new_node
    

    # Delete node with the given key.
    # The key is guaranteed to be in the skiplist.
    def delete(self, key: int):
        update = [None] * (self.maxlevel + 1)
        current = self.headnode

        for i in range(self.maxlevel, -1, -1):
            while current.pointers[i] and current.pointers[i].key < key:
                current = current.pointers[i]
            update[i] = current

        current = current.pointers[0]
        if current and current.key == key:
            for i in range(current.toplevel + 1):
                if update[i].pointers[i] != current:
                    break
                update[i].pointers[i] = current.pointers[i]

    # Search for the given key.
    # Construct a list of all the keys in all the nodes visited during the search.
    # Append the value associated to the given key to this list.
    def search(self, key) -> str:
            current = self.header
            visited_keys = [-float('inf')]  # Starting with the header node represented by -Infinity

            # Traverse from the top level
            for level in range(self.max_level, -1, -1):
                # Traverse horizontally
                while current.forward[level] and current.forward[level].key < key:
                    # Record the key of each traversed node
                    if current.forward[level].key not in visited_keys:
                        visited_keys.append(current.forward[level].key)
                    current = current.forward[level]

                # Record the target node if found
                if current.forward[level] and current.forward[level].key == key:
                    visited_keys.append(key)
                    return json.dumps(visited_keys + [current.forward[level].value])

            # Return the list of traversed nodes with None if the target is not found
            return json.dumps(visited_keys + [None])