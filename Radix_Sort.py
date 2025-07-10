import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import random

class RadixSortVisualizer:
    def __init__(self, root):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.root = root
        self.root.title("Radix Sort Side-by-Side Bucket Visualizer")
        self.root.geometry("1540x810")

        # Styling variables
        self.primary_color = "#1E90FF"
        self.secondary_color = "#FF4500"
        self.node_color = "skyblue"
        self.bucket_color = "lightgray"
        self.active_color = "yellow"
        self.bg_color = "#F5F5F5"
        self.text_color = "#333333"

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
            placeholder_text="e.g., 170, 45, 75, 90, 802",
            corner_radius=10
        )
        self.entry.pack(side="left", padx=10)
        self.entry.bind("<Return>", lambda event: self.start_sorting())

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

        # Control frame
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

        # Canvas setup
        self.canvas_frame = ctk.CTkFrame(self.root, fg_color=self.bg_color)
        self.canvas_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.tree_canvas = tk.Canvas(
            self.canvas_frame,
            width=1200,
            height=600,
            bg=self.bg_color,
            highlightthickness=0
        )

        self.tree_canvas.pack(side="left", fill="both", expand=True)



        # Initialize variables
        self.array = []
        self.delay = 500
        self.bucket_positions = {}  # bucket_id -> (x0, x1, y0, y1)
        self.number_positions = {}  # (num, idx, digit, stage) -> (x, y, elements)
        self.is_sorting = False
        self.sorting_steps = []
        self.current_step = -1
        self.is_playing = False
        self.max_digits = 0
        self.buckets = [[] for _ in range(10)]  # Current bucket contents
        self.bucket_counts = [0] * 10  # Track number of elements in each bucket
        self.array_positions = []  # (x, y) for array elements
        self.current_state = {"type": None, "buckets": [[] for _ in range(10)], "array": [], "exp": 0,
                              "assigning": None, "placing": None, "to_index": None}

    def reset_visualization(self):
        """Reset the visualization to its initial state."""
        self.is_sorting = False
        self.is_playing = False
        self.play_pause_button.configure(text="Play")
        self.tree_canvas.delete("all")
        self.bucket_positions.clear()
        self.number_positions.clear()
        self.sorting_steps = []
        self.current_step = -1
        self.array = []
        self.max_digits = 0
        self.buckets = [[] for _ in range(10)]
        self.bucket_counts = [0] * 10
        self.array_positions = []
        self.current_state = {"type": None, "buckets": [[] for _ in range(10)], "array": [], "exp": 0,
                              "assigning": None, "placing": None, "to_index": None}

    def generate_random_array(self):
        """Generate a random array and start sorting."""
        self.reset_visualization()
        random_array = [random.randint(0, 999) for _ in range(10)]
        self.entry.delete(0, tk.END)
        self.entry.insert(0, ",".join(map(str, random_array)))
        self.start_sorting()

    def start_sorting(self):
        """Start the radix sort visualization process."""
        if self.is_sorting:
            messagebox.showerror("Warning", "Visualization is already in progress!")
            return

        self.reset_visualization()
        try:
            self.is_sorting = True
            input_str = self.entry.get().strip()
            if not input_str:
                messagebox.showerror("Error", "Input field is empty. Please enter comma-separated numbers.")
                return

            input_values = [x.strip() for x in input_str.split(",") if x.strip()]
            if not input_values:
                messagebox.showerror("Error", "No valid numbers found. Please enter comma-separated integers.")
                return

            if len(input_values) > 10:
                messagebox.showerror("Error","Input exceeds 10 numbers. Please enter up to 10 comma-separated integers.")
                return

            self.array = []
            for val in input_values:
                try:
                    num = int(val)
                    if num < 0:
                        messagebox.showerror("Error", "Negative numbers are not allowed. Please enter non-negative integers.")
                        return
                    self.array.append(num)
                except ValueError:
                    messagebox.showerror("Error", f"Invalid input '{val}'. Please enter valid comma-separated integers.")
                    return

            if len(self.array) > 20:
                messagebox.showerror("Error", "Array size exceeds 20 numbers. Please enter fewer numbers.")
                return

            if not self.array:
                messagebox.showerror("Error", "No valid numbers found. Please enter comma-separated integers.")
                return

            # Calculate max digits for radix sort
            self.max_digits = len(str(max(self.array))) if self.array else 1

            # Initialize bucket positions
            self.setup_buckets()

            # Perform radix sort visualization
            self.radix_sort_with_viz()
            if not self.sorting_steps:
                messagebox.showerror("Error", "No sorting steps generated. Please try again.")
                return

            # Display initial step
            self.current_step = 0
            self.show_step()

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
        finally:
            self.is_sorting = False

    def setup_buckets(self):
        """Set up side-by-side bucket positions at the bottom."""
        canvas_width = 1200
        canvas_height = 600
        self.bucket_width = 70
        self.bucket_height = 220
        padding = 20
        y_buckets_base = canvas_height - 80
        bucket_start_x = (canvas_width - 10 * (self.bucket_width + padding * 2) + padding) / 2

        for b in range(10):
            x0 = bucket_start_x + b * (self.bucket_width + padding * 2)
            x1 = x0 + self.bucket_width
            y0 = y_buckets_base - self.bucket_height
            y1 = y_buckets_base
            self.bucket_positions[b] = (x0, x1, y0, y1)

    def show_step(self):
        """Render the current step."""
        self.tree_canvas.delete("all")
        self.number_positions.clear()

        # Draw buckets
        for bucket_id in range(10):
            self.draw_bucket(bucket_id)

        # Execute the current step
        if 0 <= self.current_step < len(self.sorting_steps):
            func, state = self.sorting_steps[self.current_step]
            self.current_state = state  # Update current_state to the step's state
            func()

        if self.current_step >= len(self.sorting_steps) - 1 and not self.is_playing:
            self.tree_canvas.create_text(
                700, 50,
                text="Sorting Completed !!!",
                font=("Helvetica", 20, "bold"),
                fill="black",
                anchor="nw"
            )

        if self.is_playing and self.current_step < len(self.sorting_steps) - 1:
            self.current_step += 1
            self.root.after(self.delay, self.show_step)
        elif self.is_playing and self.current_step >= len(self.sorting_steps) - 1:
            self.is_playing = False
            self.play_pause_button.configure(text="Play")

    def toggle_play_pause(self):
        """Toggle play/pause for animation."""
        if not self.sorting_steps:
            self.start_sorting()
            if not self.sorting_steps:
                return
        self.is_playing = not self.is_playing
        self.play_pause_button.configure(text="Pause" if self.is_playing else "Play")
        if self.is_playing and self.current_step < len(self.sorting_steps) - 1:
            self.current_step += 1
            self.show_step()

    def next_step(self):
        """Advance to the next step."""
        if not self.sorting_steps:
            self.start_sorting()
            if not self.sorting_steps:
                return
        if self.current_step < len(self.sorting_steps) - 1:
            self.current_step += 1
            self.show_step()

    def previous_step(self):
        """Go back to the previous step."""
        if self.current_step > 0:
            self.current_step -= 1
            self.show_step()

    def get_digit(self, num, exp):
        """Extract the digit at the given exponent (1 for units, 10 for tens, etc.)."""
        return (num // exp) % 10

    def radix_sort_with_viz(self):
        """Perform radix sort with visualization steps, tracking visual positions."""
        # Store initial state
        state = {
            "type": "initial",
            "array": self.array[:],
            "buckets": [[] for _ in range(10)],
            "exp": 0,
            "assigning": None,
            "placing": None,
            "to_index": None,
            "visual_positions": {},  # (num, bucket_id) -> visual_slot (from bottom)
            "phase": 0  # Track phase number
        }
        self.sorting_steps.append((self.draw_state, state))

        current_array = self.array[:]
        current_buckets = [[] for _ in range(10)]
        current_bucket_counts = [0] * 10
        visual_positions = {}  # Track visual slot for each number

        for digit in range(self.max_digits):
            exp = 10 ** digit
            phase = digit + 1  # Phase number (1-based for display)
            # Distribution phase
            for idx, num in enumerate(current_array):
                d = self.get_digit(num, exp)
                visual_slot = current_bucket_counts[d]  # Slot from bottom (0 is bottommost)
                current_buckets[d].append(num)
                current_bucket_counts[d] += 1
                visual_positions[(num, d)] = visual_slot  # Store visual slot
                state = {
                    "type": "radix_assign",
                    "array": current_array[:],
                    "buckets": [b[:] for b in current_buckets],
                    "exp": exp,
                    "assigning": {"num": num, "index": idx, "digit": d, "exp": exp, "visual_slot": visual_slot},
                    "placing": None,
                    "to_index": None,
                    "visual_positions": visual_positions.copy(),
                    "phase": phase
                }
                self.sorting_steps.append((self.draw_state, state))

            # Collection phase
            new_array = []
            to_index = 0
            for bucket_id in range(10):
                bucket_content = current_buckets[bucket_id][:]
                for i in range(len(bucket_content)):
                    num = current_buckets[bucket_id].pop(0)  # Remove from front
                    current_bucket_counts[bucket_id] -= 1
                    visual_slot = visual_positions.get((num, bucket_id), 0)  # Get original slot
                    new_array.append(num)
                    state = {
                        "type": "radix_place_back",
                        "array": new_array + current_array[len(new_array):],
                        "buckets": [b[:] for b in current_buckets],
                        "exp": exp,
                        "assigning": None,
                        "placing": {"from_bucket": bucket_id, "num": num, "visual_slot": visual_slot},
                        "to_index": to_index,
                        "visual_positions": visual_positions.copy(),
                        "phase": phase
                    }
                    self.sorting_steps.append((self.draw_state, state))
                    to_index += 1

            current_array = new_array
            # Array update step
            state = {
                "type": "array_update",
                "array": current_array[:],
                "buckets": [[] for _ in range(10)],
                "exp": exp,
                "assigning": None,
                "placing": None,
                "to_index": None,
                "visual_positions": {},
                "phase": phase
            }
            self.sorting_steps.append((self.draw_state, state))

            # Phase completion step
            state = {
                "type": "phase_complete",
                "array": current_array[:],
                "buckets": [[] for _ in range(10)],
                "exp": exp,
                "assigning": None,
                "placing": None,
                "to_index": None,
                "visual_positions": {},
                "phase": phase
            }
            self.sorting_steps.append((self.draw_state, state))

            current_buckets = [[] for _ in range(10)]
            current_bucket_counts = [0] * 10
            visual_positions = {}  # Reset for next digit

        self.array = current_array

    def draw_bucket(self, bucket_id):
        """Draw a bucket with its contents, using fixed visual slots."""
        if bucket_id not in self.bucket_positions:
            return

        x0, x1, y0, y1 = self.bucket_positions[bucket_id]
        x0 += 300
        x1 += 300
        y0 += 150
        y1 += 150
        element_box_width = 50
        element_box_height = 45
        element_spacing = 10
        max_elements = self.bucket_height // (element_box_height + element_spacing)

        # Draw bucket lines
        line_color = "black"
        self.tree_canvas.create_line(x0, y0, x0, y1, fill=line_color, width=2)
        self.tree_canvas.create_line(x1, y0, x1, y1, fill=line_color, width=2)
        self.tree_canvas.create_line(x0, y1, x1, y1, fill=line_color, width=2)
        self.tree_canvas.create_text((x0 + x1) / 2, y1 + 20, text=str(bucket_id),
                                     fill="black", font=("Helvetica", 15, "bold"))

        # Draw bucket contents using visual slots
        bucket_content = self.current_state["buckets"][bucket_id]
        visual_positions = self.current_state.get("visual_positions", {})
        fill = self.active_color if (
                (self.current_state["type"] == "radix_assign" and
                 bucket_id == self.current_state["assigning"].get("digit") if self.current_state[
                    "assigning"] else False) or
                (self.current_state["type"] == "radix_place_back" and
                 bucket_id == self.current_state["placing"].get("from_bucket") if self.current_state[
                    "placing"] else False)
        ) else self.bucket_color

        # Draw each number in its original visual slot
        for num in bucket_content:
            visual_slot = visual_positions.get((num, bucket_id), 0)
            if visual_slot >= max_elements:
                continue  # Skip if beyond display limit
            y_element = y1 - (visual_slot + 1) * (element_box_height + element_spacing) + element_box_height / 2
            x_element_center = (x0 + x1) / 2
            x_element_left = x_element_center - element_box_width / 2
            x_element_right = x_element_center + element_box_width / 2
            rect_id = self.tree_canvas.create_rectangle(
                x_element_left, y_element - element_box_height / 2,
                x_element_right, y_element + element_box_height / 2,
                fill=fill, outline="black"
            )
            text_id = self.tree_canvas.create_text(
                x_element_center, y_element, text=str(num),
                fill="black", font=("Helvetica", 15, "bold")
            )
            self.number_positions[(num, bucket_id, visual_slot, "bucket")] = (
                x_element_center, y_element, [(rect_id, text_id)]
            )

    def draw_state(self):
        """Draw the current state (array, buckets, and status text)."""
        canvas_width = 1200
        canvas_height = 600
        box_width = 70
        box_height = 70
        padding = 10
        y_main = 250

        # Draw array
        colors = [self.node_color] * len(self.current_state["array"])
        if self.current_state["type"] == "radix_assign" and self.current_state["assigning"]:
            assigning_index = self.current_state["assigning"].get("index")
            if assigning_index is not None and 0 <= assigning_index < len(colors):
                colors[assigning_index] = self.active_color
        elif self.current_state["type"] == "radix_place_back" and self.current_state["placing"]:
            to_index = self.current_state["to_index"]
            if to_index is not None and 0 <= to_index < len(colors):
                colors[to_index] = self.active_color

        total_width = len(self.current_state["array"]) * (box_width + padding) - padding
        start_x = ((canvas_width - total_width) / 2) + 300
        self.array_positions = []

        for idx, value in enumerate(self.current_state["array"]):
            x0 = start_x + idx * (box_width + padding)
            x1 = x0 + box_width
            y0 = y_main - box_height / 2
            y1 = y_main + box_height / 2
            rect_id = self.tree_canvas.create_rectangle(
                x0, y0, x1, y1, fill=colors[idx], outline="black"
            )
            text_id = self.tree_canvas.create_text(
                (x0 + x1) / 2, (y0 + y1) / 2, text=str(value),
                fill="black", font=("Helvetica", 15, "bold")
            )
            self.tree_canvas.create_text(
                (x0 + x1) / 2, y1 + 15, text=str(idx),
                fill="black", font=("Helvetica", 17, "bold")
            )
            self.array_positions.append(((x0 + x1) / 2, y_main))
            self.number_positions[(value, idx, "array")] = (
                (x0 + x1) / 2, y_main, [(rect_id, text_id)]
            )

        # Draw buckets
        for bucket_id in range(10):
            self.draw_bucket(bucket_id)

        # Draw status text
        if self.current_state["type"] == "radix_assign" and self.current_state["assigning"]:
            assigning = self.current_state["assigning"]
            self.tree_canvas.create_text(
                700, 50,
                text=f"Placing {assigning['num']} in bucket {assigning['digit']}",
                font=("Helvetica", 20, "bold"),
                fill="black",
                anchor="nw"
            )
        elif self.current_state["type"] == "radix_place_back" and self.current_state["placing"]:
            placing = self.current_state["placing"]
            self.tree_canvas.create_text(
                700, 50,
                text=f"Move from bucket {placing['from_bucket']} to index {self.current_state['to_index']}",
                font=("Helvetica", 20, "bold"),
                fill="black",
                anchor="nw"
            )
        elif self.current_state["type"] == "phase_complete"and self.current_step < len(self.sorting_steps) - 1:
            phase = self.current_state["phase"]
            self.tree_canvas.create_text(
                700, 50,
                text=f"Phase {phase} Completed .",
                font=("Helvetica", 20, "bold"),
                fill="black",
                anchor="nw"
            )

        # Draw digit position text (e.g., units, tens)
        if self.current_state["exp"]:
            exp = self.current_state["exp"]
            if exp == 1:
                position = "units"
            elif exp == 10:
                position = "tens"
            elif exp == 100:
                position = "hundreds"
            else:
                position = f"10^{int(exp).bit_length() - 1}"



if __name__ == "__main__":
    root = ctk.CTk()
    app = RadixSortVisualizer(root)
    root.mainloop()