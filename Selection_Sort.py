import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import random

# Set base directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the relative path to the images folder
images_dir = os.path.join(base_dir, "../other imp files")

class SelectionSortVisualizer:
    def __init__(self, root):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.root = root
        self.root.title("Selection Sort Visualizer")
        self.root.geometry("1540x810")

        # Styling variables
        self.primary_color = "#1E90FF"
        self.secondary_color = "#FF4500"
        self.node_color = "skyblue"
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
        self.number_positions = {}  # (value, idx) -> (x, y, elements)
        self.is_sorting = False
        self.sorting_steps = []
        self.current_step = -1
        self.is_playing = False
        self.array_positions = []  # (x, y) for array elements
        self.current_state = {
            "type": None,
            "array": [],
            "comparing": None,  # (i, j) indices being compared
            "swapping": None,   # (i, min_idx) indices being swapped
            "pass_num": 0
        }

    def reset_visualization(self):
        """Reset the visualization to its initial state."""
        self.is_sorting = False
        self.is_playing = False
        self.play_pause_button.configure(text="Play")
        self.tree_canvas.delete("all")
        self.number_positions.clear()
        self.sorting_steps = []
        self.current_step = -1
        self.array = []
        self.array_positions = []
        self.current_state = {
            "type": None,
            "array": [],
            "comparing": None,
            "swapping": None,
            "pass_num": 0
        }

    def generate_random_array(self):
        """Generate a random array and start sorting."""
        self.reset_visualization()
        random_array = [random.randint(0, 999) for _ in range(10)]
        self.entry.delete(0, tk.END)
        self.entry.insert(0, ",".join(map(str, random_array)))
        self.start_sorting()

    def start_sorting(self):
        """Start the selection sort visualization process."""
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
                messagebox.showerror("Error", "Input exceeds 10 numbers. Please enter up to 10 comma-separated integers.")
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

            if not self.array:
                messagebox.showerror("Error", "No valid numbers found. Please enter comma-separated integers.")
                return

            # Perform selection sort visualization
            self.selection_sort_with_viz()
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

    def show_step(self):
        """Render the current step."""
        self.tree_canvas.delete("all")
        self.number_positions.clear()

        # Execute the current step
        if 0 <= self.current_step < len(self.sorting_steps):
            func, state = self.sorting_steps[self.current_step]
            self.current_state = state  # Update current_state to the step's state
            func()

        if self.current_step >= len(self.sorting_steps) - 1:
            self.tree_canvas.create_text(
                300, 90,
                text="Sorting Completed !!!",
                font=("Helvetica", 20, "bold"),
                fill="black",
                anchor="nw"
            )
            self.is_playing = False
            self.play_pause_button.configure(text="Play")

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

    def selection_sort_with_viz(self):
        """Perform selection sort with visualization steps."""
        # Store initial state
        state = {
            "type": "initial",
            "array": self.array[:],
            "comparing": None,
            "swapping": None,
            "pass_num": 0
        }
        self.sorting_steps.append((self.draw_state, state))

        current_array = self.array[:]
        n = len(current_array)

        for i in range(n):
            min_idx = i
            # Comparison steps to find minimum
            for j in range(i + 1, n):
                state = {
                    "type": "compare",
                    "array": current_array[:],
                    "comparing": (min_idx, j),
                    "swapping": None,
                    "pass_num": i + 1
                }
                self.sorting_steps.append((self.draw_state, state))

                if current_array[j] < current_array[min_idx]:
                    min_idx = j
                    state = {
                        "type": "new_min",
                        "array": current_array[:],
                        "comparing": (i, min_idx),
                        "swapping": None,
                        "pass_num": i + 1
                    }
                    self.sorting_steps.append((self.draw_state, state))

            # Swap if minimum is found
            if min_idx != i:
                current_array[i], current_array[min_idx] = current_array[min_idx], current_array[i]
                state = {
                    "type": "swap",
                    "array": current_array[:],
                    "comparing": None,
                    "swapping": (i, min_idx),
                    "pass_num": i + 1
                }
                self.sorting_steps.append((self.draw_state, state))

            # Pass completion step
            state = {
                "type": "pass_complete",
                "array": current_array[:],
                "comparing": None,
                "swapping": None,
                "pass_num": i + 1
            }
            self.sorting_steps.append((self.draw_state, state))

        self.array = current_array

    def tree_draw_text(self, *args, **kwargs):
        """Wrapper for canvas.create_text to handle long texts safely."""
        try:
            return self.tree_canvas.create_text(*args, **kwargs)
        except Exception as e:
            print(f"Error drawing text: {e}")
            return None

    def draw_state(self):
        """Draw the current state (array and status text)."""
        canvas_width = 1200
        canvas_height = 600
        box_width = 70
        box_height = 70
        padding = 10
        y_main = canvas_height // 2

        # Draw array
        colors = [self.node_color] * len(self.current_state["array"])
        if self.current_state["type"] in ["compare", "new_min"] and self.current_state["comparing"]:
            i, j = self.current_state["comparing"]
            if 0 <= i < len(colors) and 0 <= j < len(colors):
                colors[i] = self.active_color
                colors[j] = self.active_color
        elif self.current_state["type"] == "swap" and self.current_state["swapping"]:
            i, j = self.current_state["swapping"]
            if 0 <= i < len(colors) and 0 <= j < len(colors):
                colors[i] = self.active_color
                colors[j] = self.active_color

        total_width = len(self.current_state["array"]) * (box_width + padding) - padding
        start_x = ((canvas_width - total_width) / 2) - 150

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
            self.number_positions[(value, idx)] = (
                (x0 + x1) / 2, y_main, [(rect_id, text_id)]
            )

        # Draw status text
        if self.current_step < len(self.sorting_steps) - 1:
            if self.current_state["type"] == "compare" and self.current_state["comparing"]:
                i, j = self.current_state["comparing"]
                self.tree_draw_text(
                    400, 90,
                    text=f"Comparing indices {i} and {j}",
                    font=("Helvetica", 20, "bold"),
                    fill="black",
                    anchor="center"
                )
            elif self.current_state["type"] == "new_min" and self.current_state["comparing"]:
                i, j = self.current_state["comparing"]
                self.tree_draw_text(
                    400, 90,
                    text=f"New minimum found at index {j}",
                    font=("Helvetica", 20, "bold"),
                    fill="black",
                    anchor="center"
                )
            elif self.current_state["type"] == "swap" and self.current_state["swapping"]:
                i, j = self.current_state["swapping"]
                self.tree_draw_text(
                    400, 90,
                    text=f"Swapping indices {i} and {j}",
                    font=("Helvetica", 20, "bold"),
                    fill="black",
                    anchor="center"
                )
            elif self.current_state["type"] == "pass_complete":
                self.tree_draw_text(
                    400, 90,
                    text=f"Pass {self.current_state['pass_num']} Completed",
                    font=("Helvetica", 20, "bold"),
                    fill="black",
                    anchor="center"
                )

if __name__ == "__main__":
    root = ctk.CTk()
    app = SelectionSortVisualizer(root)
    image_path = os.path.join(images_dir, "images", "selection_sort.png")
    image_label = tk.Label(root, bg="#e6f7ff")
    algorithm_label = tk.Label(root, text="Algorithm :- ", font=("Arial", 20, "bold"),
                                      fg="black")
    algorithm_label.place(x=1000, y=200)
    try:
        en = ImageTk.PhotoImage(Image.open(image_path).resize((750, 650), Image.Resampling.LANCZOS))
        image_label.config(image=en)
        image_label.place(x=1100, y=250)
    except FileNotFoundError:
        print(f"Image file not found at: {image_path}")
    root.mainloop()