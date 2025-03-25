def strWithout3a3b(a: int, b: int) -> str:
    if a > b:
        bigger = [a, 'a']
        smaller = [b, 'b']
    else:
        bigger = [b, 'b']
        smaller = [a, 'a']

    result = []

    while bigger[0] > 0 or smaller[0] > 0:
        if len(result) >= 2 and result[-1] == result[-2]:
            if result[-1] == bigger[1]:
                result.append(smaller[1])
                smaller[0] -= 1
            else:
                result.append(bigger[1])
                bigger[0] -= 1

        if bigger[0] > smaller[0]:
            result.append(bigger[1])
            bigger[0] -= 1
        else:
            result.append(smaller[1])
            smaller[0] -= 1

    text = ''.join(result)
    return text



def isMonotonic(nums) -> bool:
    if nums[0] == nums[-1]:
        for i in range(0, len(nums) - 1):
            if nums[i] == nums[i + 1]:
                continue
            else:
                return False
        return True
    elif nums[0] > nums[-1]:
        for i in range(0, len(nums)-1):
            if nums[i] == nums[i+1]:
                continue
            if nums[i] > nums[i + 1]:
                continue
            else:
                return False
        return True
    elif nums[0] < nums[-1]:
        for i in range(0, len(nums)-1):
            if nums[i] == nums[i+1]:
                continue
            if nums[i] < nums[i + 1]:
                continue
            else:
                return False
        return True

# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


def isSameTree(p, q) -> bool:
    if not p and not q:
        print("Both trees are empty, returning True")
        return True
    if not p or not q:
        print("One tree is empty while the other is not, returning False")
        return False
    if p.val != q.val:
        print(f"Values at current nodes are different: {p.val} and {q.val}, returning False")
        return False
    left_result = isSameTree(p.left, q.left)
    right_result = isSameTree(p.right, q.right)
    print(f"Left subtree result: {left_result}, Right subtree result: {right_result}")
    return left_result and right_result



class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def findBottomLeftValue(root) -> int:
    if not root:
        return None

    # Initialize a list to act as a queue
    queue = [root]
    leftmost_node = None  # To store the value of the leftmost node in the last level

    # Traverse level by level
    while queue:
        level_size = len(queue)
        leftmost_node = queue[0].val  # Store the leftmost node value in this level

        # Process all nodes in the current level
        for _ in range(level_size):
            node = queue.pop(0)  # Dequeue the front node

            # Enqueue the children of the current node (if any)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    return leftmost_node

if __name__ == '__main__':
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.right.right = TreeNode(5)
    root.right.right.left = TreeNode(6)
    root.right.right.right = TreeNode(7)
    print(findBottomLeftValue(root))
    # print(strWithout3a3b(a = 1, b = 4))
    # print(isMonotonic(nums = [1,1,1]))
    # Create nodes
    # p_node1 = TreeNode(1)
    # p_node2 = TreeNode(2)
    # p_node3 = TreeNode(3)
    #
    # q_node1 = TreeNode(1)
    # q_node2 = TreeNode(2)
    # q_node3 = TreeNode(3)
    #
    # # Connect nodes to form trees
    # p_node1.left = p_node2
    # p_node1.right = p_node3
    #
    # q_node1.left = q_node2
    # q_node1.right = q_node3
    #
    # # Check if trees are the same
    # print(isSameTree(p_node1, q_node1))