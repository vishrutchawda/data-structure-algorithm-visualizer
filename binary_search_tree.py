import tkinter as tk
from tkinter import simpledialog, messagebox, ttk


class Node:
    """A node in the binary search tree."""

    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BinarySearchTree:
    """A binary search tree implementation with methods for insertion, deletion, and traversals."""

    def __init__(self):
        self.root = None
        self.node_map = {}  # Map for quick node lookup by value

    def insert(self, value):
        """Insert a value into the binary search tree. Raises ValueError if value already exists."""
        if self.root is None:
            self.root = Node(value)
            self.node_map[value] = self.root
        else:
            self._insert(self.root, value)

    def _insert(self, node, value):
        """Helper method to insert a new node according to BST rules."""
        if value < node.data:
            if node.left is None:
                node.left = Node(value)
                self.node_map[value] = node.left
            else:
                self._insert(node.left, value)
        elif value > node.data:
            if node.right is None:
                node.right = Node(value)
                self.node_map[value] = node.right
            else:
                self._insert(node.right, value)
        else:
            raise ValueError(f"Node with value {value} already exists in the tree.")

    def delete(self, value):
        """Delete a value from the binary search tree. Returns (deleted_node, replacement_node)."""
        self.root, removed_values, replacements, deleted_node, replacement_node = self._delete(self.root, value)
        # Update node_map: remove deleted values and update replacements
        for val in removed_values:
            if val in self.node_map:
                del self.node_map[val]
        for node, new_value in replacements:
            self.node_map[new_value] = node
        return deleted_node, replacement_node

    def _delete(self, node, value):
        """Helper method to delete a node and update the tree structure.

        Returns:
            tuple: (updated_node, removed_values, replacements, deleted_node, replacement_node)
            - updated_node: The updated subtree after deletion.
            - removed_values: List of values whose nodes were removed.
            - replacements: List of (node, new_value) tuples for nodes with updated values.
            - deleted_node: The node targeted for deletion.
            - replacement_node: The node used for replacement, if any.
        """
        if node is None:
            return None, [], [], None, None

        if value < node.data:
            updated_left, removed_values, replacements, del_node, rep_node = self._delete(node.left, value)
            node.left = updated_left
            return node, removed_values, replacements, del_node, rep_node
        elif value > node.data:
            updated_right, removed_values, replacements, del_node, rep_node = self._delete(node.right, value)
            node.right = updated_right
            return node, removed_values, replacements, del_node, rep_node
        else:
            # Node to be deleted is found
            deleted_node = node
            if node.left is None:
                temp = node.right
                removed_values = [node.data]
                replacements = []
                replacement_node = None
                return temp, removed_values, replacements, deleted_node, replacement_node
            elif node.right is None:
                temp = node.left
                removed_values = [node.data]
                replacements = []
                replacement_node = None
                return temp, removed_values, replacements, deleted_node, replacement_node
            else:
                # Node with two children
                if self._subtree_size(node.left) > self._subtree_size(node.right):
                    predecessor = self._max_value_node(node.left)
                    new_value = predecessor.data
                    old_data = node.data
                    node.data = new_value
                    updated_left, sub_removed_values, sub_replacements, _, _ = self._delete(node.left, new_value)
                    node.left = updated_left
                    removed_values = sub_removed_values + [old_data]
                    replacements = sub_replacements + [(node, new_value)]
                    replacement_node = predecessor
                    return node, removed_values, replacements, deleted_node, replacement_node
                else:
                    successor = self._min_value_node(node.right)
                    new_value = successor.data
                    old_data = node.data
                    node.data = new_value
                    updated_right, sub_removed_values, sub_replacements, _, _ = self._delete(node.right, new_value)
                    node.right = updated_right
                    removed_values = sub_removed_values + [old_data]
                    replacements = sub_replacements + [(node, new_value)]
                    replacement_node = successor
                    return node, removed_values, replacements, deleted_node, replacement_node

    def _subtree_size(self, node):
        """Calculate the size of a subtree."""
        if node is None:
            return 0
        return 1 + self._subtree_size(node.left) + self._subtree_size(node.right)

    def _min_value_node(self, node):
        """Find the node with the smallest value in the subtree."""
        current = node
        while current.left:
            current = current.left
        return current

    def _max_value_node(self, node):
        """Find the node with the largest value in the subtree."""
        current = node
        while current.right:
            current = current.right
        return current

    def inorder(self):
        """Perform inorder traversal (left-root-right)."""
        return self._inorder(self.root)

    def _inorder(self, node):
        if node is None:
            return []
        return self._inorder(node.left) + [node.data] + self._inorder(node.right)

    def preorder(self):
        """Perform preorder traversal (root-left-right)."""
        return self._preorder(self.root)

    def _preorder(self, node):
        if node is None:
            return []
        return [node.data] + self._preorder(node.left) + self._preorder(node.right)

    def postorder(self):
        """Perform postorder traversal (left-right-root)."""
        return self._postorder(self.root)

    def _postorder(self, node):
        if node is None:
            return []
        return self._postorder(node.left) + self._postorder(node.right) + [node.data]

    def get_size(self):
        """Return the number of nodes in the tree."""
        return self._get_size(self.root)

    def _get_size(self, node):
        if node is None:
            return 0
        return 1 + self._get_size(node.left) + self._get_size(node.right)

    def get_height(self):
        """Return the height of the tree."""
        return self._get_height(self.root)

    def _get_height(self, node):
        if node is None:
            return -1  # Height of empty tree is -1
        left_height = self._get_height(node.left)
        right_height = self._get_height(node.right)
        return 1 + max(left_height, right_height)


class BinarySearchTreeGUI:
    """A Tkinter-based GUI for visualizing and interacting with a binary search tree."""

    def __init__(self, root):
        self.bst = BinarySearchTree()

        # Main window styling
        self.root = root
        self.root.title("Binary Search Tree Visualization")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f8ff")

        # Frame for user input
        self.frame = tk.Frame(root, bg="#e6f7ff", bd=5)
        self.frame.pack(pady=20)

        # Entry field for value input
        self.label = tk.Label(self.frame, text="Enter value:", bg="#e6f7ff", font=("Arial", 12))
        self.label.grid(row=0, column=0)

        self.entry = tk.Entry(self.frame, font=("Arial", 12))
        self.entry.grid(row=0, column=1)

        # Dropdown menu for operation selection
        self.options = [
            "Insert",
            "Inorder Traversal",
            "Preorder Traversal",
            "Postorder Traversal",
            "Delete Node",
            "Reconstruct from Preorder"
        ]
        self.operation = tk.StringVar(self.root)
        self.operation.set(self.options[0])

        self.dropdown = ttk.Combobox(self.frame, textvariable=self.operation, values=self.options, font=("Arial", 12))
        self.dropdown.grid(row=0, column=2)
        self.dropdown['state'] = 'readonly'

        # Button to trigger action
        self.btn = tk.Button(self.frame, text="Submit", command=self.perform_operation, bg="#4CAF50", fg="white",
                             font=("Arial", 12), activebackground="#45a049")
        self.btn.grid(row=0, column=3)

        # Bind the Enter key to the submit button action
        self.entry.bind('<Return>', lambda event: self.perform_operation())

        # Canvas for tree visualization
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white", highlightbackground="#b0c4de")
        self.canvas.pack()

        # Label to display the traversal result
        self.result_label = tk.Label(root, text="", font=("Arial", 12, "bold"), fg="#4CAF50", bg="#f0f8ff")
        self.result_label.pack(pady=10)

        # Labels for tree properties
        self.size_label = tk.Label(root, text="Number of nodes: 0", font=("Arial", 12), bg="#f0f8ff")
        self.size_label.pack()
        self.height_label = tk.Label(root, text="Height: -1", font=("Arial", 12), bg="#f0f8ff")
        self.height_label.pack()

    def perform_operation(self):
        """Perform the selected operation based on user input."""
        operation = self.operation.get()
        input_value = self.entry.get()

        if operation == "Insert":
            try:
                value = int(input_value)
                self.bst.insert(value)
                self.draw_tree()
                self.update_tree_properties()
            except ValueError as e:
                messagebox.showerror("Error", str(e) if str(e) else "Please enter a valid integer.")
        elif operation == "Delete Node":
            try:
                value = int(input_value)
                deleted_node, replacement_node = self.bst.delete(value)
                if deleted_node:
                    # Visualize the deletion process
                    self.highlight_node(deleted_node.data if replacement_node else value, highlight_color="red",
                                        text="Deleting")
                    if replacement_node:
                        self.highlight_node(replacement_node.data, highlight_color="yellow", text="Replacing")
                        self.animate_move(replacement_node.data, deleted_node.data)
                    self.draw_tree()
                    self.update_tree_properties()
                    self.result_label.config(text=f"Node {value} deleted.")
                else:
                    messagebox.showerror("Error", f"Node with value {value} not found.")
            except ValueError as e:
                messagebox.showerror("Error", str(e) if str(e) else "Please enter a valid integer.")
        elif operation in ["Inorder Traversal", "Preorder Traversal", "Postorder Traversal"]:
            if operation == "Inorder Traversal":
                traversal = self.bst.inorder()
                self.highlight_nodes(traversal, "Inorder Traversal")
                self.result_label.config(text="Inorder Traversal: " + ', '.join(map(str, traversal)))
            elif operation == "Preorder Traversal":
                traversal = self.bst.preorder()
                self.highlight_nodes(traversal, "Preorder Traversal")
                self.result_label.config(text="Preorder Traversal: " + ', '.join(map(str, traversal)))
            elif operation == "Postorder Traversal":
                traversal = self.bst.postorder()
                self.highlight_nodes(traversal, "Postorder Traversal")
                self.result_label.config(text="Postorder Traversal: " + ', '.join(map(str, traversal)))
        elif operation == "Reconstruct from Preorder":
            try:
                preorder_list = [int(x.strip()) for x in input_value.split(',')]
                self.bst.root = None
                self.bst.node_map = {}
                self._insert_with_visual(preorder_list)
                self.update_tree_properties()
                self.result_label.config(text="Tree reconstructed.")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid comma-separated list of integers.")

        self.entry.delete(0, tk.END)

    def update_tree_properties(self):
        """Update the displayed tree properties: size and height."""
        size = self.bst.get_size()
        height = self.bst.get_height()
        self.size_label.config(text=f"Number of nodes: {size}")
        self.height_label.config(text=f"Height: {height}")

    def draw_tree(self):
        """Draw the binary search tree on the canvas."""
        self.canvas.delete("all")
        if self.bst.root:
            self._draw_node(self.bst.root, 400, 50, 150)

    def _draw_node(self, node, x, y, offset):
        """Recursively draw the tree nodes."""
        if node:
            # Draw the node as a circle
            self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="lightblue", outline="black", width=2)
            self.canvas.create_text(x, y, text=str(node.data), font=("Arial", 12))

            # Draw the left child
            if node.left:
                self.canvas.create_line(x - 20, y + 20, x - offset + 20, y + 80 - 20, fill="black")
                self._draw_node(node.left, x - offset, y + 80, offset // 2)

            # Draw the right child
            if node.right:
                self.canvas.create_line(x + 20, y + 20, x + offset - 20, y + 80 - 20, fill="black")
                self._draw_node(node.right, x + offset, y + 80, offset // 2)

    def highlight_node(self, value, highlight_color="yellow", text=""):
        """Highlight a specific node."""
        self.canvas.delete("all")
        self.draw_tree()
        self._highlight_node(self.bst.root, value, 400, 50, 150, highlight_color, text)

    def _highlight_node(self, node, value, x, y, offset, highlight_color, text):
        """Helper method to highlight a specific node."""
        if node:
            if node.data == value:
                self.canvas.after(500)
                self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=highlight_color, outline="black", width=2)
                self.canvas.create_text(x, y, text=str(node.data), font=("Arial", 12))

            # Traverse left or right
            if node.left:
                self._highlight_node(node.left, value, x - offset, y + 80, offset // 2, highlight_color, text)
            if node.right:
                self._highlight_node(node.right, value, x + offset, y + 80, offset // 2, highlight_color, text)

    def animate_move(self, from_value, to_value):
        """Animate the movement of a node from one position to another."""
        self.highlight_node(from_value, highlight_color="yellow", text="Moving")
        self.canvas.after(1000)
        self.highlight_node(to_value, highlight_color="green", text="Arrived")
        self.canvas.after(1000)

    def highlight_nodes(self, traversal, title):
        """Highlight nodes during traversal."""
        self.canvas.delete("all")
        self.draw_tree()

        # Highlight nodes one by one
        for i, value in enumerate(traversal):
            self.canvas.update()
            self.canvas.after(500)
            self._highlight_node(self.bst.root, value, 400, 50, 150, highlight_color="yellow", text=title)

    def _insert_with_visual(self, preorder):
        """Insert nodes one by one with visualization."""

        def insert_next_node(index):
            if index < len(preorder):
                value = preorder[index]
                self.bst.insert(value)
                self.draw_tree()
                self.canvas.after(500, insert_next_node, index + 1)
            else:
                self.update_tree_properties()

        insert_next_node(0)


if __name__ == "__main__":
    root = tk.Tk()
    gui = BinarySearchTreeGUI(root)
    root.mainloop()