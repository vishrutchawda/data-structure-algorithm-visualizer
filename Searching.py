import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import os

# Set base directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the relative path to the images folder
images_dir = os.path.join(base_dir, "../other imp files")


def SearchVisualizer(master_window):
    global master,images  # Store master globally
    master = master_window

    master.title("Search Algorithms Visualization")
    master.configure(bg="#3A3A3A")

    # Declare global variables to manage shared state
    global entry, canvas, status_label, binary_values, target, lb, ub, mid, next_step_button, prev_step_button, history
    binary_values = []
    target = None
    lb = 0
    ub = 0
    mid = 0
    next_step_button = None
    prev_step_button = None
    history = []  # To store history of (lb, ub, mid)

    # Styling for labels and entry
    label = tk.Label(master, text="Enter comma-separated values:", font=("Helvetica", 12, "bold"), bg="#3A3A3A", fg="white")
    label.grid(row=0, column=0, columnspan=3, pady=(20, 5), padx=20)

    entry = tk.Entry(master, font=("Helvetica", 12), bg="#262626", fg="white", borderwidth=3, relief="groove", width=50)
    entry.grid(row=1, column=0, columnspan=3, pady=(0, 20), padx=20)

    # Buttons with styling
    linear_button = tk.Button(master, text="Linear Search", command=linear_search, font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", activebackground="#45A049", width=15, height=2)
    linear_button.grid(row=2, column=0, pady=(0, 10))

    binary_button = tk.Button(master, text="Binary Search", command=start_binary_search, font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", activebackground="#45A049", width=15, height=2)
    binary_button.grid(row=2, column=1, pady=(0, 10))

    exit_button = tk.Button(master, text="Exit", command=master.quit, font=("Helvetica", 12, "bold"), bg="#F44336", fg="white", activebackground="#D32F2F", width=15, height=2)
    exit_button.grid(row=2, column=2, pady=(0, 10))

    # Canvas for visualization with a customized background color
    canvas = tk.Canvas(master, width=1500, height=550, bg="#FFF5E1", borderwidth=0, highlightthickness=0)
    canvas.grid(row=3, column=0, columnspan=3, pady=20, padx=20)

    # Status label for messages
    status_label = tk.Label(master, text="", font=("Helvetica", 20, "bold"), bg="#FFF5E1", fg="#FF7043")
    status_label.place(x=220, y=200)

    images = load_images()


def load_images():
        try:
            # Resize images to a more suitable size
            linear_search_image_path = os.path.join(images_dir, "images", "linear_search.png")
            binary_search_image_path = os.path.join(images_dir, "images", "binary_search.png")

            ls = ImageTk.PhotoImage(Image.open(linear_search_image_path).resize((600, 500), Image.Resampling.LANCZOS))
            bs = ImageTk.PhotoImage(Image.open(binary_search_image_path).resize((650, 540), Image.Resampling.LANCZOS))


            return {
                "Linear Search": ls,
                "Binary Search": bs,
            }
        except Exception as e:
            print(f"Error loading images: {e}")
            return {}


current_image_label = None

def algorithm(algo):
    """Updates the displayed algorithm image based on user selection."""
    global current_image_label,images

    # Remove previous image label if it exists
    if current_image_label is not None:
        current_image_label.destroy()

    # Update the image label dynamically instead of creating new labels each time
    algo_image = images.get(algo)

    if algo == "Linear Search":
        # Create a new label for the selected image
        current_image_label = tk.Label(master, image=algo_image, bg="#3A3A3A")
        current_image_label.place(x = 900 , y = 200)

    elif algo == "Binary Search":
        # Create a new label for the selected image
        current_image_label = tk.Label(master, image=algo_image, bg="#3A3A3A")
        current_image_label.place(x = 850 , y = 180)

    else:
        messagebox.showwarning("Image Not Found", f"Image for {algo} not found!")


def get_values():
    """Retrieve and validate user-entered list of integers."""
    input_data = entry.get()
    try:
        values = [int(x.strip()) for x in input_data.split(",")]
        if not values:
            raise ValueError("Input list is empty.")
        return values
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid list of integers.")
        return None

def clear_canvas():
    """Clear the visualization canvas."""
    canvas.delete("all")

def draw_list(lst, highlight_index=None):
    """Draws the list on the canvas, with optional highlighting of a specific index."""
    clear_canvas()
    box_width = 60
    box_height = 60
    padding = 15
    y_position = 200

    for index, value in enumerate(lst):
        x_position = index * (box_width + padding) + 20
        color = "#90CAF9" if highlight_index != index else "#FF7043"

        canvas.create_rectangle(x_position, y_position, x_position + box_width, y_position + box_height, fill=color, outline="#1E88E5")
        canvas.create_text(x_position + box_width / 2, y_position + box_height / 2, text=str(value), font=("Arial", 15, "bold"))
        canvas.create_text(x_position + box_width / 2, y_position + box_height + 15, text=str(index), font=("Arial", 15), fill="#616161")

    canvas.update()

def linear_search():
    """Performs a linear search on the list for a specified target value."""
    algorithm("Linear Search")

    values = get_values()
    if values is None:
        return

    draw_list(values)
    target_value = get_target_value()
    if target_value is None:
        return

    status_label.config(text=f"Element to be Searched: {target_value}")

    for index, value in enumerate(values):
        draw_list(values, highlight_index=index)
        canvas.update()
        canvas.after(500)
        if value == target_value:
            status_label.config(text=f"Element {target_value} found at index {index}")
            return

    status_label.config(text=f"Element {target_value} not found in the list")

def start_binary_search():
    """Initialize binary search variables and create the Next and Previous Step buttons."""
    global binary_values, target, lb, ub, mid, history, next_step_button, prev_step_button

    algorithm("Binary Search")

    values = get_values()
    if values is None:
        return

    binary_values = sorted(values)
    draw_list(binary_values)

    target = get_target_value()
    if target is None:
        return

    lb = 0
    ub = len(binary_values) - 1
    history = []  # Reset history
    status_label.config(text=f"Element to be Searched: {target}")

    if next_step_button:
        next_step_button.destroy()
    if prev_step_button:
        prev_step_button.destroy()

    # Create "Next Step" button
    next_step_button = tk.Button(master, text="Next Step", command=perform_next_step, font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", activebackground="#45A049", width=12, height=1)
    next_step_button.place(x=220 , y=670)

    # Create "Previous Step" button
    prev_step_button = tk.Button(master, text="Previous Step", command=perform_prev_step, font=("Helvetica", 12, "bold"), bg="#FF7043", fg="white", activebackground="#FF7043", width=12, height=1)
    prev_step_button.place(x=390, y=670)

    perform_next_step()


def perform_next_step():
    global binary_values, target, lb, ub, history
    """Performs a single step of the binary search."""
    if lb <= ub:
        mid = (lb + ub) // 2

        # Save the current state to history
        history.append((lb, ub, mid))

        draw_list(binary_values, highlight_index=mid)

        # Clear previous status text
        canvas.delete("status_text")

        # Update bounds and mid values
        canvas.create_text(100, 310, text=f"LB :- {lb}", font=("Helvetica", 20), fill="black", tags="status_text")
        canvas.create_text(100, 340, text=f"UB :- {ub}", font=("Helvetica", 20), fill="black", tags="status_text")
        canvas.create_text(100, 370, text=f"MID :- {mid}", font=("Helvetica", 20), fill="black", tags="status_text")

        # Check value at mid and adjust lb or ub accordingly
        if binary_values[mid] < target:
            canvas.create_text(400, 310, text=f"A[mid] < {target}       Yes", font=("Helvetica", 20), fill="black", tags="status_text")
            canvas.create_text(400, 340, text=f"A[mid] > {target}       No", font=("Helvetica", 20), fill="black", tags="status_text")
            canvas.create_text(400, 370, text=f"A[mid] == {target}      No", font=("Helvetica", 20), fill="black", tags="status_text")
            lb = mid + 1
        elif binary_values[mid] > target:
            canvas.create_text(400, 310, text=f"A[mid] < {target}       No", font=("Helvetica", 20), fill="black", tags="status_text")
            canvas.create_text(400, 340, text=f"A[mid] > {target}       Yes", font=("Helvetica", 20), fill="black", tags="status_text")
            canvas.create_text(400, 370, text=f"A[mid] == {target}      No", font=("Helvetica", 20), fill="black", tags="status_text")
            ub = mid - 1
        else:
            canvas.create_text(400, 310, text=f"A[mid] < {target}       No", font=("Helvetica", 20), fill="black", tags="status_text")
            canvas.create_text(400, 340, text=f"A[mid] > {target}       No", font=("Helvetica", 20), fill="black", tags="status_text")
            canvas.create_text(400, 370, text=f"A[mid] == {target}      Yes", font=("Helvetica", 20), fill="black", tags="status_text")
            status_label.config(text=f"Element {target} found at index {mid}")
            next_step_button.destroy()
            prev_step_button.destroy()
            return

    else:
        status_label.config(text=f"Element {target} not found in the list")
        next_step_button.destroy()
        prev_step_button.destroy()


def perform_prev_step():
    """Performs the previous step of the binary search."""
    global lb, ub, mid, history

    if len(history) > 1:
        # Remove the current state from history
        history.pop()

        # Restore the last state from history
        lb, ub, mid = history[-1]  # Get the previous state without removing it

        draw_list(binary_values, highlight_index=mid)

        # Update status text to reflect the restored state
        canvas.delete("status_text")
        canvas.create_text(100, 310, text=f"LB :- {lb}", font=("Helvetica", 20), fill="black", tags="status_text")
        canvas.create_text(100, 340, text=f"UB :- {ub}", font=("Helvetica", 20), fill="black", tags="status_text")
        canvas.create_text(100, 370, text=f"MID :- {mid}", font=("Helvetica", 20), fill="black", tags="status_text")

        # Check value at mid and adjust lb or ub accordingly
        if binary_values[mid] < target:
            canvas.create_text(400, 310, text=f"A[mid] < {target}       Yes", font=("Helvetica", 20), fill="black",
                               tags="status_text")
            canvas.create_text(400, 340, text=f"A[mid] > {target}       No", font=("Helvetica", 20), fill="black",
                               tags="status_text")
            canvas.create_text(400, 370, text=f"A[mid] == {target}      No", font=("Helvetica", 20), fill="black",
                               tags="status_text")
            lb = mid + 1
        elif binary_values[mid] > target:
            canvas.create_text(400, 310, text=f"A[mid] < {target}       No", font=("Helvetica", 20), fill="black",
                               tags="status_text")
            canvas.create_text(400, 340, text=f"A[mid] > {target}       Yes", font=("Helvetica", 20), fill="black",
                               tags="status_text")
            canvas.create_text(400, 370, text=f"A[mid] == {target}      No", font=("Helvetica", 20), fill="black",
                               tags="status_text")
            ub = mid - 1
        else:
            canvas.create_text(400, 310, text=f"A[mid] < {target}       No", font=("Helvetica", 20), fill="black",
                               tags="status_text")
            canvas.create_text(400, 340, text=f"A[mid] > {target}       No", font=("Helvetica", 20), fill="black",
                               tags="status_text")
            canvas.create_text(400, 370, text=f"A[mid] == {target}      Yes", font=("Helvetica", 20), fill="black",
                               tags="status_text")
            status_label.config(text=f"Element {target} found at index {mid}")
            next_step_button.destroy()
            prev_step_button.destroy()
            return

    else:
        status_label.config(text="No previous steps available.")


def get_target_value():
    """Prompts user for the target value to search for."""
    return simpledialog.askinteger("Input", "Enter the value to be searched:")


if __name__ == "__main__":
    root = tk.Tk()
    SearchVisualizer(root)
    root.mainloop()
