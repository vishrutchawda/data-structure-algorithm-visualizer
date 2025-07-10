import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import random

class TreeNode:
    def __init__(self, value, start, end, node_id, parents=None):
        self.value = value
        self.start = start
        self.end = end
        self.node_id = node_id
        self.children = []
        self.parents = parents if parents is not None else []
        for parent in self.parents:
            if self not in parent.children:
                parent.children.append(self)

class MergeSortVisualizer:
    def __init__(self, root):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.root = root
        self.root.title("Merge Sort Tree Visualizer")
        self.root.geometry("1540x810")

        # Styling variables (unchanged)
        self.primary_color = "#1E90FF"
        self.secondary_color = "#FF4500"
        self.node_color = "lightblue"
        self.merge_node_color = "lightgreen"
        self.bg_color = "#F5F5F5"
        self.text_color = "#333333"
        self.arrow_color = "black"

        # Input frame
        self.input_frame = ctk.CTkFrame(self.root, fg_color=self.bg_color)
        self.input_frame.pack(pady=20, padx=20, fill="x")

        self.label = ctk.CTkLabel(
            self.input_frame,
            text="Enter numbers (comma-separated):",
            font=("Arial", 16, "bold"),
            text_color=self.text_color
        )
        self.label.pack(side="left", padx=10)

        self.entry = ctk.CTkEntry(
            self.input_frame,
            width=400,
            font=("Arial", 14),
            placeholder_text="e.g., 5, 3, 8, 1, 9",
            corner_radius=10
        )
        self.entry.pack(side="left", padx=10)
        self.entry.bind("<Return>", lambda event: self.start_sorting())  # Bind Enter key

        self.generate_button = ctk.CTkButton(
            self.input_frame,
            text="Generate Random Array",
            command=self.generate_random_array,
            font=("Arial", 14, "bold"),
            fg_color=self.primary_color,
            hover_color="#4682B4",
            corner_radius=10
        )
        self.generate_button.pack(side="left", padx=10)

        self.reset_button = ctk.CTkButton(
            self.input_frame,
            text="Reset",
            command=self.reset_visualization,
            font=("Arial", 14, "bold"),
            fg_color=self.secondary_color,
            hover_color="#FF6347",
            corner_radius=10
        )
        self.reset_button.pack(side="left", padx=10)

        # Control frame (unchanged)
        self.control_frame = ctk.CTkFrame(self.root, fg_color=self.bg_color)
        self.control_frame.pack(pady=10, padx=20, fill="x")

        self.prev_button = ctk.CTkButton(
            self.control_frame,
            text="Previous Step",
            command=self.previous_step,
            font=("Arial", 14, "bold"),
            fg_color=self.secondary_color,
            hover_color="#FF6347",
            corner_radius=10
        )
        self.prev_button.pack(side="left", padx=10)

        self.next_button = ctk.CTkButton(
            self.control_frame,
            text="Next Step",
            command=self.next_step,
            font=("Arial", 14, "bold"),
            fg_color=self.secondary_color,
            hover_color="#FF6347",
            corner_radius=10
        )
        self.next_button.pack(side="left", padx=10)

        self.play_pause_button = ctk.CTkButton(
            self.control_frame,
            text="Play",
            command=self.toggle_play_pause,
            font=("Arial", 14, "bold"),
            fg_color=self.primary_color,
            hover_color="#4682B4",
            corner_radius=10
        )
        self.play_pause_button.pack(side="left", padx=10)

        # Canvas setup (unchanged)
        self.canvas_frame = ctk.CTkFrame(self.root, fg_color=self.bg_color)
        self.canvas_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.tree_canvas = tk.Canvas(
            self.canvas_frame,
            width=1200,
            height=600,
            bg=self.bg_color,
            highlightthickness=0
        )
        self.scrollbar = ctk.CTkScrollbar(
            self.canvas_frame,
            orientation="vertical",
            command=self.tree_canvas.yview
        )
        self.tree_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.tree_canvas.pack(side="left", fill="both", expand=True)
        self.tree_canvas.configure(scrollregion=(0, 0, 2000, 4000))

        self.root.bind("<MouseWheel>", self.scroll_canvas)

        # Initialize variables (unchanged)
        self.array = []
        self.delay = 350
        self.node_positions = {}
        self.drawn_edges = set()
        self.is_sorting = False
        self.max_depth = 0
        self.nodes_at_depth = {}
        self.single_value_depth = 0
        self.sorting_steps = []
        self.current_step = -1
        self.node_id_counter = 0
        self.all_nodes = []
        self.is_playing = False

    def scroll_canvas(self, event):
        if event.num == 4 or event.delta > 0:  # Scroll up
            self.tree_canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:  # Scroll down
            self.tree_canvas.yview_scroll(1, "units")

    def get_node_id(self):
        self.node_id_counter += 1
        return f"N{self.node_id_counter}"

    def reset_visualization(self):
        """Reset the visualization to its initial state."""
        self.is_sorting = False
        self.is_playing = False
        self.play_pause_button.configure(text="Play")
        self.tree_canvas.delete("all")
        self.node_positions.clear()
        self.drawn_edges.clear()
        self.max_depth = 0
        self.nodes_at_depth = {}
        self.single_value_depth = 0
        self.sorting_steps = []
        self.current_step = -1
        self.node_id_counter = 0
        self.all_nodes = []
        self.array = []

    def generate_random_array(self):
        """Generate a random array and start sorting."""
        # Reset visualization state before generating a new array
        self.reset_visualization()
        random_array = [random.randint(0, 99) for _ in range(10)]
        self.entry.delete(0, tk.END)
        self.entry.insert(0, ",".join(map(str, random_array)))
        self.start_sorting()

    def start_sorting(self):
        """Start the merge sort visualization process."""
        # Check if sorting is already in progress
        if self.is_sorting:
            messagebox.showerror("Warning", "Visualization is already in progress!")
            return

        # Reset visualization state
        self.reset_visualization()

        try:
            # Set is_sorting to True
            self.is_sorting = True

            # Capture input
            input_str = self.entry.get().strip()
            if not input_str:
                messagebox.showerror("Error", "Input field is empty. Please enter comma-separated numbers.")
                return

            # Split input and filter out empty or invalid entries
            input_values = [x.strip() for x in input_str.split(",") if x.strip()]
            if not input_values:
                messagebox.showerror("Error", "No valid numbers found. Please enter comma-separated integers.")
                return

            if len(input_values) > 10:
                messagebox.showerror("Error","Input exceeds 10 numbers. Please enter up to 10 comma-separated integers.")
                return


            # Convert to integers and validate
            self.array = []
            for val in input_values:
                try:
                    num = int(val)
                    if num < 0:
                        messagebox.showerror("Error",
                                             "Negative numbers are not allowed. Please enter non-negative integers.")
                        return
                    self.array.append(num)
                except ValueError:
                    messagebox.showerror("Error",
                                         f"Invalid input '{val}'. Please enter valid comma-separated integers.")
                    return

            if len(self.array) > 20:
                messagebox.showerror("Error", "Array size exceeds 20 numbers. Please enter fewer numbers.")
                return

            if not self.array:
                messagebox.showerror("Error", "No valid numbers found. Please enter comma-separated integers.")
                return

            # Proceed with visualization
            root_node = self.merge_sort_with_viz(self.array, 0, len(self.array), 0)

            for depth in sorted(self.nodes_at_depth.keys()):
                all_single = all(len(node.value) == 1 for node in self.nodes_at_depth[depth])
                if all_single:
                    self.single_value_depth = depth
                    break

            self.propagate_single_valued_nodes()
            self.build_merge_tree(root_node)
            self.show_step()

            # Ensure Play and Next Step buttons are ready
            self.current_step = -1
            self.is_playing = False
            self.play_pause_button.configure(text="Play")

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
        finally:
            # Always reset is_sorting to False when done or if an error occurs
            self.is_sorting = False

    def show_step(self):
        self.tree_canvas.delete("all")
        self.node_positions.clear()
        self.drawn_edges.clear()

        for i in range(self.current_step + 1):
            if i < len(self.sorting_steps):
                func, *args = self.sorting_steps[i]
                func(*args)

        self.tree_canvas.configure(scrollregion=self.tree_canvas.bbox("all"))

        if self.is_playing and self.current_step < len(self.sorting_steps) - 1:
            self.current_step += 1
            self.root.after(self.delay, self.show_step)
        elif self.is_playing and self.current_step >= len(self.sorting_steps) - 1:
            self.is_playing = False
            self.play_pause_button.configure(text="Play")

    def toggle_play_pause(self):
        if not self.sorting_steps:
            self.start_sorting()
            if not self.sorting_steps:  # Check if start_sorting failed
                return
        self.is_playing = not self.is_playing
        self.play_pause_button.configure(text="Pause" if self.is_playing else "Play")
        if self.is_playing:
            if self.current_step < len(self.sorting_steps) - 1:
                self.current_step += 1
                self.show_step()

    def next_step(self):
        if not self.sorting_steps:
            self.start_sorting()
            if not self.sorting_steps:  # Check if start_sorting failed
                return
        if self.current_step < len(self.sorting_steps) - 1:
            self.current_step += 1
            self.show_step()

    def previous_step(self):
        if self.current_step > -1:
            self.current_step -= 1
            self.show_step()

    def merge_sort_with_viz(self, arr, start, end, depth):
        if depth not in self.nodes_at_depth:
            self.nodes_at_depth[depth] = []

        if end - start <= 1:
            node = TreeNode(arr[start:end], start, end, self.get_node_id())
            self.nodes_at_depth[depth].append(node)
            self.all_nodes.append(node)
            self.max_depth = max(self.max_depth, depth)
            self.array[start:end] = sorted(arr[start:end])
            self.sorting_steps.append((self.draw_node, node, start, end, depth, False, False))
            return node

        mid = (start + end + 1) // 2
        node = TreeNode(arr[start:end], start, end, self.get_node_id())
        self.nodes_at_depth[depth].append(node)
        self.all_nodes.append(node)
        self.max_depth = max(self.max_depth, depth)
        self.sorting_steps.append((self.draw_node, node, start, end, depth, False, False))

        left_child = self.merge_sort_with_viz(arr, start, mid, depth + 1)
        right_child = self.merge_sort_with_viz(arr, mid, end, depth + 1)
        left_child.parents.append(node)
        right_child.parents.append(node)
        node.children = [left_child, right_child]

        self.sorting_steps.append((self.draw_edges, node))
        return node

    def propagate_single_valued_nodes(self):
        for depth in range(self.single_value_depth):
            if depth not in self.nodes_at_depth:
                continue
            for node in self.nodes_at_depth[depth]:
                if len(node.value) == 1 and not node.children:
                    current = node
                    for d in range(depth + 1, self.single_value_depth + 1):
                        if d not in self.nodes_at_depth:
                            self.nodes_at_depth[d] = []
                        new_node = TreeNode(node.value, node.start, node.end, self.get_node_id(), parents=[current])
                        self.nodes_at_depth[d].append(new_node)
                        self.all_nodes.append(new_node)
                        self.sorting_steps.append((self.draw_node, new_node, node.start, node.end, d, False, True))
                        self.sorting_steps.append((self.draw_propagation_edge, current, new_node))
                        current.children.append(new_node)
                        current = new_node

    def merge(self, left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def build_merge_tree(self, root_node):
        merge_nodes = []
        if self.single_value_depth in self.nodes_at_depth:
            merge_nodes = [(node, node.start) for node in self.nodes_at_depth[self.single_value_depth]]
            merge_nodes.sort(key=lambda x: x[1])

        current_depth = self.single_value_depth + 1

        if merge_nodes:
            new_merge_nodes = []
            for i in range(0, len(merge_nodes) - 1, 2):
                left_node, left_start = merge_nodes[i]
                right_node, right_start = merge_nodes[i + 1]
                merged_value = self.merge(left_node.value, right_node.value)
                merged_start = min(left_node.start, right_node.start)
                merged_end = max(left_node.end, right_node.end)
                merged_node = TreeNode(
                    merged_value, merged_start, merged_end, self.get_node_id(),
                    parents=[left_node, right_node]
                )
                self.all_nodes.append(merged_node)
                left_node.children.append(merged_node)
                right_node.children.append(merged_node)
                parent = self.find_parent_split_node(merged_start, merged_end)
                if parent:
                    parent.children.append(merged_node)
                if current_depth not in self.nodes_at_depth:
                    self.nodes_at_depth[current_depth] = []
                self.nodes_at_depth[current_depth].append(merged_node)
                self.sorting_steps.append(
                    (self.draw_merge_node, merged_node, merged_start, merged_end, current_depth)
                )
                new_merge_nodes.append((merged_node, merged_start))

            if len(merge_nodes) % 2 == 1:
                unpaired_node, unpaired_start = merge_nodes[-1]
                if new_merge_nodes:
                    last_merged_node, last_merged_start = new_merge_nodes[-1]
                    merged_value = self.merge(last_merged_node.value, unpaired_node.value)
                    merged_start = min(last_merged_node.start, unpaired_node.start)
                    merged_end = max(last_merged_node.end, unpaired_node.end)
                    merged_node = TreeNode(
                        merged_value, merged_start, merged_end, self.get_node_id(),
                        parents=[last_merged_node, unpaired_node]
                    )
                    self.all_nodes.append(merged_node)
                    last_merged_node.children.append(merged_node)
                    unpaired_node.children.append(merged_node)
                    parent = self.find_parent_split_node(merged_start, merged_end)
                    if parent:
                        parent.children.append(merged_node)
                    self.nodes_at_depth[current_depth].append(merged_node)
                    self.sorting_steps.append(
                        (self.draw_merge_node, merged_node, merged_start, merged_end, current_depth)
                    )
                    new_merge_nodes[-1] = (merged_node, merged_start)
                else:
                    new_merge_nodes.append((unpaired_node, unpaired_start))

            merge_nodes = new_merge_nodes

            while len(merge_nodes) > 1:
                new_merge_nodes = []
                current_depth += 1
                for i in range(0, len(merge_nodes), 2):
                    if i + 1 < len(merge_nodes):
                        left_node, left_start = merge_nodes[i]
                        right_node, right_start = merge_nodes[i + 1]
                        merged_value = self.merge(left_node.value, right_node.value)
                        merged_start = min(left_node.start, right_node.start)
                        merged_end = max(left_node.end, right_node.end)
                        merged_node = TreeNode(
                            merged_value, merged_start, merged_end, self.get_node_id(),
                            parents=[left_node, right_node]
                        )
                        self.all_nodes.append(merged_node)
                        left_node.children.append(merged_node)
                        right_node.children.append(merged_node)
                        parent = self.find_parent_split_node(merged_start, merged_end)
                        if parent:
                            parent.children.append(merged_node)
                        if current_depth not in self.nodes_at_depth:
                            self.nodes_at_depth[current_depth] = []
                        self.nodes_at_depth[current_depth].append(merged_node)
                        self.sorting_steps.append(
                            (self.draw_merge_node, merged_node, merged_start, merged_end, current_depth)
                        )
                        new_merge_nodes.append((merged_node, merged_start))
                    else:
                        new_merge_nodes.append(merge_nodes[i])
                merge_nodes = new_merge_nodes

    def find_parent_split_node(self, start, end):
        for depth in range(self.single_value_depth):
            if depth not in self.nodes_at_depth:
                continue
            for node in self.nodes_at_depth[depth]:
                if node.start == start and node.end == end and len(node.value) > 1:
                    return node
        return None

    def draw_node(self, node, start, end, depth, is_merge, is_propagated):
        x = ((start + end) / 2 * (1200 / len(self.array))) + 350
        y = depth * 120 + 100
        node_key = (node.node_id, tuple(node.value), node.start, node.end)

        if node_key in self.node_positions:
            return

        box_size = 35
        spacing = 5
        total_width = len(node.value) * box_size + (len(node.value) - 1) * spacing
        start_x = x - total_width / 2
        node_elements = []
        fill_color = self.merge_node_color if is_merge else self.node_color

        for i, val in enumerate(node.value):
            box_x1 = start_x + i * (box_size + spacing)
            box_x2 = box_x1 + box_size
            box_y1 = y - box_size / 2
            box_y2 = y + box_size / 2
            rect_id = self.tree_canvas.create_rectangle(
                box_x1, box_y1, box_x2, box_y2,
                fill=fill_color,
                outline=self.text_color,
                width=2
            )
            text_x = (box_x1 + box_x2) / 2
            text_y = y
            text_id = self.tree_canvas.create_text(
                text_x, text_y,
                text=str(val),
                font=("Arial", 16, "bold"),
                fill=self.text_color
            )
            node_elements.append((rect_id, text_id))

        self.node_positions[node_key] = (x, y, node_elements)

    def draw_merge_node(self, node, start, end, merge_depth):
        parent_xs = []
        parent_depths = []
        for p in node.parents:
            p_key = (p.node_id, tuple(p.value), p.start, p.end)
            if p_key in self.node_positions:
                px, _, _ = self.node_positions[p_key]
                parent_xs.append(px)
                parent_depths.append(self.get_node_depth(p))

        is_odd_merge_node = (merge_depth == self.single_value_depth + 1 and
                             any(depth == merge_depth for depth in parent_depths))

        if node.node_id == "N31":
            x = sum(parent_xs) / len(parent_xs)
            y = merge_depth * 120 + 80 if len(self.array) == 10 else merge_depth * 120 + 150
        elif end - start == len(self.array) and len(node.value) == len(self.array):
            x = (sum(parent_xs) / len(parent_xs)) - 70 if len(self.array) == 10 else sum(parent_xs) / len(parent_xs)
            y = merge_depth * 120 + 150 if len(self.array) in [3, 5, 9] else merge_depth * 120 + 100
        elif is_odd_merge_node:
            x = sum(parent_xs) / len(parent_xs)
            y = merge_depth * 150 + 50
        else:
            x = sum(parent_xs) / len(parent_xs)
            y = merge_depth * 120 + 70

        node_key = (node.node_id, tuple(node.value), node.start, node.end)
        if node_key in self.node_positions:
            return

        box_size = 35
        spacing = 5
        total_width = len(node.value) * box_size + (len(node.value) - 1) * spacing
        start_x = x - total_width / 2
        node_elements = []

        for i, val in enumerate(node.value):
            box_x1 = start_x + i * (box_size + spacing)
            box_x2 = box_x1 + box_size
            box_y1 = y - box_size / 2
            box_y2 = y + box_size / 2
            rect_id = self.tree_canvas.create_rectangle(
                box_x1, box_y1, box_x2, box_y2,
                fill=self.merge_node_color,
                outline=self.text_color,
                width=2
            )
            text_x = (box_x1 + box_x2) / 2
            text_y = y
            text_id = self.tree_canvas.create_text(
                text_x, text_y,
                text=str(val),
                font=("Arial", 16, "bold"),
                fill=self.text_color
            )
            node_elements.append((rect_id, text_id))

        self.node_positions[node_key] = (x, y, node_elements)

        for p in node.parents:
            p_key = (p.node_id, tuple(p.value), p.start, p.end)
            if p_key in self.node_positions:
                px, py, _ = self.node_positions[p_key]
                edge_key = (p_key, node_key)
                if edge_key not in self.drawn_edges:
                    self.tree_canvas.create_line(
                        px, py + 15, x, y - 15,
                        arrow=tk.LAST,
                        fill=self.arrow_color,
                        width=2
                    )
                    self.drawn_edges.add(edge_key)

    def draw_edges(self, node):
        node_key = (node.node_id, tuple(node.value), node.start, node.end)
        if node_key in self.node_positions:
            x, y, _ = self.node_positions[node_key]
            for child in node.children:
                child_key = (child.node_id, tuple(child.value), child.start, child.end)
                if child_key in self.node_positions:
                    cx, cy, _ = self.node_positions[child_key]
                    edge_key = (node_key, child_key)
                    if edge_key not in self.drawn_edges:
                        edge_color = self.arrow_color
                        self.tree_canvas.create_line(
                            x, y + 15, cx, cy - 15,
                            arrow=tk.LAST,
                            fill=edge_color,
                            width=2
                        )
                        self.drawn_edges.add(edge_key)

    def draw_propagation_edge(self, parent, child):
        parent_key = (parent.node_id, tuple(parent.value), parent.start, parent.end)
        child_key = (child.node_id, tuple(child.value), child.start, child.end)
        if parent_key in self.node_positions and child_key in self.node_positions:
            px, py, _ = self.node_positions[parent_key]
            cx, cy, _ = self.node_positions[child_key]
            edge_key = (parent_key, child_key)
            if edge_key not in self.drawn_edges:
                self.tree_canvas.create_line(
                    px, py + 15, cx, cy - 15,
                    arrow=tk.LAST,
                    fill=self.arrow_color,
                    width=2
                )
                self.drawn_edges.add(edge_key)

    def get_node_depth(self, node):
        for depth, nodes in self.nodes_at_depth.items():
            if node in nodes:
                return depth
        return -1

if __name__ == "__main__":
    root = ctk.CTk()
    app = MergeSortVisualizer(root)
    root.mainloop()