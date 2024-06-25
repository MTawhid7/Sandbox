class AVLNode:
    def __init__(self, key):
        self.key = key
        self.height = 1
        self.left = None
        self.right = None


class AVLTree:
    def __init__(self):
        self.root = None

    def height(self, node):
        if node is None:
            return 0
        return node.height

    def balance_factor(self, node):
        return self.height(node.left) - self.height(node.right)

    def update_height(self, node):
        node.height = 1 + max(self.height(node.left), self.height(node.right))

    def rotate_right(self, y):
        # Step 1: Set x as the left child of y and T2 as the right child of x.
        x = y.left
        T2 = x.right

        # Step 2: Update the right child of x to be y.
        x.right = y
        # Step 3: Update the left child of y to be T2.
        y.left = T2

        # Step 4: Update the height of y.
        self.update_height(y)
        # Step 5: Update the height of x.
        self.update_height(x)

        # Step 6: Return the new root of the rotated subtree (x).
        return x

    def rotate_left(self, x):
        # Step 1: Set y as the right child of x and T2 as the left child of y.
        y = x.right
        T2 = y.left

        # Step 2: Update the left child of y to be x.
        y.left = x

        # Step 3: Update the right child of x to be T2.
        x.right = T2

        # Step 4: Update the height of x.
        self.update_height(x)

        # Step 5: Update the height of y.
        self.update_height(y)

        # Step 6: Return the new root of the rotated subtree (y).
        return y

    def insert(self, root, key):
        if root is None:
            return AVLNode(key)

        # Perform standard BST insert
        if key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        # Update height of the current node
        self.update_height(root)

        # Get the balance factor to check if the node became unbalanced
        balance = self.balance_factor(root)

        # Left Heavy
        if balance > 1:
            # Left-Left Case
            if key < root.left.key:
                return self.rotate_right(root)
            # Left-Right Case
            else:
                root.left = self.rotate_left(root.left)
                return self.rotate_right(root)

        # Right Heavy
        if balance < -1:
            # Right-Right Case
            if key > root.right.key:
                return self.rotate_left(root)
            # Right-Left Case
            else:
                root.right = self.rotate_right(root.right)
                return self.rotate_left(root)

        return root

    def insert_list(self, elements):
        for element in elements:
            self.root = self.insert(self.root, element)

    def inorder_traversal(self, node):
        if node:
            self.inorder_traversal(node.left)
            print(node.key, end=" ")
            self.inorder_traversal(node.right)

    def update_key(self, key_to_update, new_key):
        self.delete_key(key_to_update)
        self.root = self.insert(self.root, new_key)

    def delete_key(self, key_to_delete):
        self.root = self._delete_key(self.root, key_to_delete)

    def _delete_key(self, root, key):
        if root is None:
            return root

        if key < root.key:
            root.left = self._delete_key(root.left, key)
        elif key > root.key:
            root.right = self._delete_key(root.right, key)
        else:
            # Node with only one child or no child
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left

            # Node with two children, find the inorder successor
            root.key = self._min_value_node(root.right).key
            root.right = self._delete_key(root.right, root.key)

        # Update height of the current node
        self.update_height(root)

        # Get the balance factor to check if the node became unbalanced
        balance = self.balance_factor(root)

        # Left Heavy
        if balance > 1:
            if self.balance_factor(root.left) >= 0:
                return self.rotate_right(root)
            else:
                root.left = self.rotate_left(root.left)
                return self.rotate_right(root)

        # Right Heavy
        if balance < -1:
            if self.balance_factor(root.right) <= 0:
                return self.rotate_left(root)
            else:
                root.right = self.rotate_right(root.right)
                return self.rotate_left(root)

        return root

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current


# Example usage:
avl_tree = AVLTree()

# Take user input for the list
user_input = input("Enter the list of keys separated by spaces: ")
user_elements = list(map(int, user_input.split()))

# Insert the list into the AVL tree
avl_tree.insert_list(user_elements)

while True:
    print("\nOptions:")
    print("1. Inorder Traversal")
    print("2. Insert Key")
    print("3. Delete Key")
    print("4. Update Key")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        print("Inorder Traversal of AVL Tree:")
        avl_tree.inorder_traversal(avl_tree.root)
    elif choice == "2":
        new_key = int(input("Enter the key to insert: "))
        avl_tree.root = avl_tree.insert(avl_tree.root, new_key)
        print(f"Key {new_key} inserted.")
    elif choice == "3":
        key_to_delete = int(input("Enter the key to delete: "))
        avl_tree.delete_key(key_to_delete)
        print(f"Key {key_to_delete} deleted.")
    elif choice == "4":
        key_to_update = int(input("Enter the key to update: "))
        new_key = int(input("Enter the new key: "))
        avl_tree.update_key(key_to_update, new_key)
        print(f"Key {key_to_update} updated to {new_key}.")
    elif choice == "5":
        print("Exiting the program.")
        break
    else:
        print("Invalid choice. Please enter a valid option.")
