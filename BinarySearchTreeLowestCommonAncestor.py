# Took a binary search tree from https://www.programiz.com/dsa/binary-search-tree
# Added bits to find the lowest common ancestor for 2 given values.   Parts be me signed #rf
# Binary Search Tree operations in Python


# Create a node
class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


# Inorder traversal
def inorder(root):
    if root is not None:
        # Traverse left
        inorder(root.left)

        # Traverse root
        print(str(root.key) + "->", end=' ')

        # Traverse right
        inorder(root.right)


def findNextNode(node, key):  # rf
    current = node

    if (key < current.key):
        if (current.left is not None):
            current = current.left
    elif (key > current.key):
        if (current.right is not None):
            current = current.right

    return current


def findNode(node, value):  # rf
    outarray = []
    current = node
    while (current.key != value):
        nextnode = findNextNode(current, value)
        print("current key : " + str(current.key) +
              "next : " + str(findNextNode(current, value).key))
        outarray.append(current.key)
        current = nextnode
    outarray.append(current.key)
    return (outarray)


# Insert a node
def insert(node, key):

    # Return a new node if the tree is empty
    if node is None:
        return Node(key)

    # Traverse to the right place and insert the node
    if key < node.key:
        node.left = insert(node.left, key)
    else:
        node.right = insert(node.right, key)

    return node


# Find the inorder successor
def minValueNode(node):
    current = node

    # Find the leftmost leaf
    while (current.left is not None):
        current = current.left

    return current


# Deleting a node
def deleteNode(root, key):

    # Return if the tree is empty
    if root is None:
        return root

    # Find the node to be deleted
    if key < root.key:
        root.left = deleteNode(root.left, key)
    elif (key > root.key):
        root.right = deleteNode(root.right, key)
    else:
        # If the node is with only one child or no child
        if root.left is None:
            temp = root.right
            root = None
            return temp

        elif root.right is None:
            temp = root.left
            root = None
            return temp

        # If the node has two children,
        # place the inorder successor in position of the node to be deleted
        temp = minValueNode(root.right)

        root.key = temp.key

        # Delete the inorder successor
        root.right = deleteNode(root.right, temp.key)

    return root


root = None
root = insert(root, 8)
root = insert(root, 3)
root = insert(root, 1)
root = insert(root, 6)
root = insert(root, 7)
root = insert(root, 10)
root = insert(root, 14)
root = insert(root, 4)

print("Inorder traversal: ", end=' ')
inorder(root)

# print("\nDelete 10")
# root = deleteNode(root, 10)
# print("Inorder traversal: ", end=' ')
# inorder(root)

first = 0
second = 0

print("Finding the lowest common ancestors of 2 given values")  # rf
print("input first number")
first = input()
first = int(first)
firstarray = findNode(root, first)
print(firstarray)
second = input()
second = int(second)
secondarray = findNode(root, second)
print(secondarray)
arraylen = len(firstarray)
if (len(secondarray) < arraylen):
    arraylen = len(secondarray)
nodeval = 0

for i in range(0, arraylen):
    if (secondarray[i] == firstarray[i]):
        nodeval = firstarray[i]


print("the node is : " + str(nodeval))
