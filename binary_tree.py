import tkinter as tk
from tkinter import simpledialog, messagebox, ttk

class Node:
    """A node in the binary tree."""
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class BinaryTree:
    """A binary tree implementation with methods for insertion, traversal"""
    def __init__(self):
        self.root = None
        self.node_map = {}  # Map for quick node lookup by value

    def insert(self, value, parent_value=None, direction=None):
        """Insert a value into the binary tree based on parent and direction.

        Args:
            value: The value to insert.
            parent_value: The value of the parent node (None for root).
            direction: The direction to insert ('left' or 'right', None for root).

        Raises:
            ValueError: If parent node is not found or the specified child already exists.
        """
        if self.root is None:
            self.root = Node(value)
            self.node_map[value] = self.root
        else:
            parent_node = self.node_map.get(parent_value)
            if not parent_node:
                raise ValueError(f"Parent node {parent_value} not found.")
            if direction == "left":
                if parent_node.left is None:
                    parent_node.left = Node(value)
                    self.node_map[value] = parent_node.left
                else:
                    raise ValueError(f"Node {parent_value} already has a left child.")
            elif direction == "right":
                if parent_node.right is None:
                    parent_node.right = Node(value)
                    self.node_map[value] = parent_node.right
                else:
                    raise ValueError(f"Node {parent_value} already has a right child.")


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

class BinaryTreeGUI:
    """A Tkinter-based GUI for visualizing and interacting with a binary tree."""
    def __init__(self, root):
        self.bt = BinaryTree()

        # Main window styling
        self.root = root
        self.root.title("Binary Tree Visualization")
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
            "Postorder Traversal"
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
                if self.bt.root:
                    parent_value = simpledialog.askinteger("Parent Node", "Insert after which node?", parent=self.root)
                    if parent_value is None or parent_value not in self.bt.node_map:
                        messagebox.showerror("Error", "Parent node not found or invalid.")
                        return
                    self.ask_for_direction_and_insert(value, parent_value)
                else:
                    self.bt.insert(value)  # Insert as root
                    self.draw_tree()
                    self.update_tree_properties()
            except ValueError as e:
                messagebox.showerror("Error", str(e) if str(e) else "Please enter a valid integer.")
        elif operation == "Inorder Traversal":
            traversal = self.bt.inorder()
            self.highlight_nodes(traversal, "Inorder Traversal")
            self.result_label.config(text="Inorder Traversal: " + ', '.join(map(str, traversal)))
        elif operation == "Preorder Traversal":
            traversal = self.bt.preorder()
            self.highlight_nodes(traversal, "Preorder Traversal")
            self.result_label.config(text="Preorder Traversal: " + ', '.join(map(str, traversal)))
        elif operation == "Postorder Traversal":
            traversal = self.bt.postorder()
            self.highlight_nodes(traversal, "Postorder Traversal")
            self.result_label.config(text="Postorder Traversal: " + ', '.join(map(str, traversal)))

        self.entry.delete(0, tk.END)

    def ask_for_direction_and_insert(self, value, parent_value):
        """Prompt user to choose the direction (left or right) for insertion."""
        direction_window = tk.Toplevel(self.root)
        direction_window.title("Choose Direction")

        label = ttk.Label(direction_window, text=f"Where do you want to insert {value} under {parent_value}?")
        label.pack(pady=10)

        left_button = ttk.Button(direction_window, text="Left",
                                 command=lambda: self.insert_node_with_direction(value, parent_value, "left",
                                                                                 direction_window))
        left_button.pack(side="left", padx=10)

        right_button = ttk.Button(direction_window, text="Right",
                                  command=lambda: self.insert_node_with_direction(value, parent_value, "right",
                                                                                  direction_window))
        right_button.pack(side="right", padx=10)

    def insert_node_with_direction(self, value, parent_value, direction, window):
        """Insert a node with the specified value, parent, and direction."""
        try:
            self.bt.insert(value, parent_value, direction)
            window.destroy()
            self.draw_tree()
            self.update_tree_properties()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def update_tree_properties(self):
        """Update the displayed tree properties: size and height."""
        size = self.bt.get_size()
        height = self.bt.get_height()
        self.size_label.config(text=f"Number of nodes: {size}")
        self.height_label.config(text=f"Height: {height}")

    def draw_tree(self):
        """Draw the binary tree on the canvas."""
        self.canvas.delete("all")
        if self.bt.root:
            self._draw_node(self.bt.root, 400, 50, 150)

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

    def highlight_nodes(self, traversal, title):
        """Highlight nodes during traversal."""
        self.canvas.delete("all")
        self.draw_tree()

        # Highlight nodes one by one
        for value in traversal:
            self.canvas.update()
            self.canvas.after(500)
            self._highlight_node(self.bt.root, value, 400, 50, 150, title)

    def _highlight_node(self, node, value, x, y, offset, title):
        """Highlight a specific node with a given value."""
        if node:
            if node.data == value:
                self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="yellow", outline="black", width=2)
                self.canvas.create_text(x, y, text=str(node.data), font=("Arial", 12))

            if node.left:
                self._highlight_node(node.left, value, x - offset, y + 80, offset // 2, title)
            if node.right:
                self._highlight_node(node.right, value, x + offset, y + 80, offset // 2, title)

if __name__ == "__main__":
    root = tk.Tk()
    gui = BinaryTreeGUI(root)
    root.mainloop()