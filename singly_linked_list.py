import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import os
import time

# Set base directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the relative path to the images folder
images_dir = os.path.join(base_dir, "../other imp files")

# Global list to represent the linked list
sll = []
max_size = 8
paused = False

# Main Tkinter window
root = tk.Tk()
root.title("Singly Linked List GUI")
root.configure(bg="lightgreen")

canvas = tk.Canvas(root, width=1510, height=700, bg="white")
canvas.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

status_label = tk.Label(canvas, text="", bg="white", fg="black", font=("Helvetica", 20, "bold"))
status_label.place(x=780, y=50)

current_algo = None
current_image_label = None

operation_var = tk.StringVar(value="Select Operation")
operations = [
    "Create Singly Linked List", "Insert at Beginning", "Insert at End", "Insert after Specific",
    "Delete from Beginning", "Delete from End", "Delete Specific",
    "Traverse", "Count Nodes", "Search Element"
]


dropdown = tk.OptionMenu(root, operation_var, *operations)
dropdown.grid(row=0, column=0, padx=10, pady=10)

def toggle_pause():

    # Toggle the paused state and update the button text.

    global paused
    paused = not paused
    pause_button.config(text="Resume" if paused else "Pause")


def wait_if_paused():

    # Pause execution if the paused flag is set to True.

    while paused:
        root.update_idletasks()
        root.update()
        time.sleep(0.1)  # Check periodically to minimize CPU usage


def load_images():
    try:
        # Resize images to a more suitable size
        ins_beg_image_path = os.path.join(images_dir, "images", "sin_ins_beg.png")
        ins_end_image_path = os.path.join(images_dir, "images", "sin_ins_end.png")
        ins_aft_image_path = os.path.join(images_dir, "images", "sin_ins_aft.png")
        del_beg_image_path = os.path.join(images_dir, "images", "sin_del_beg.png")
        del_end_image_path = os.path.join(images_dir, "images", "sin_del_end.png")
        del_spe_image_path = os.path.join(images_dir, "images", "sin_del_spe.png")
        tra_image_path = os.path.join(images_dir, "images", "sin_traversing.png")
        count_image_path = os.path.join(images_dir, "images", "sin_count.png")
        search_image_path = os.path.join(images_dir, "images", "sin_search.png")

        ib = ImageTk.PhotoImage(Image.open(ins_beg_image_path).resize((700, 460), Image.Resampling.LANCZOS))
        ie = ImageTk.PhotoImage(Image.open(ins_end_image_path).resize((790, 450), Image.Resampling.LANCZOS))
        ia = ImageTk.PhotoImage(Image.open(ins_aft_image_path).resize((810, 450), Image.Resampling.LANCZOS))
        db = ImageTk.PhotoImage(Image.open(del_beg_image_path).resize((800, 450), Image.Resampling.LANCZOS))
        de = ImageTk.PhotoImage(Image.open(del_end_image_path).resize((870, 450), Image.Resampling.LANCZOS))
        ds = ImageTk.PhotoImage(Image.open(del_spe_image_path).resize((750, 450), Image.Resampling.LANCZOS))
        tr = ImageTk.PhotoImage(Image.open(tra_image_path).resize((860, 470), Image.Resampling.LANCZOS))
        cn = ImageTk.PhotoImage(Image.open(count_image_path).resize((800, 470), Image.Resampling.LANCZOS))
        se = ImageTk.PhotoImage(Image.open(search_image_path).resize((770, 470), Image.Resampling.LANCZOS))

        return {
            "Insert at Beginning": ib,
            "Insert at End": ie,
            "Insert after Specific": ia,
            "Delete from Beginning": db,
            "Delete from End": de,
            "Delete Specific": ds,
            "Traverse": tr,
            "Count Nodes": cn,
            "Search Element": se
        }
    except Exception as e:
        print(f"Error loading images: {e}")
        return {}


images = load_images()


def get_input(prompt, allow_multiple=False):
    """Display a prompt and get validated integer input from the user."""
    input_data = simpledialog.askstring("Input", prompt)
    if input_data:
        try:
            if allow_multiple:
                return [int(value) for value in input_data.replace(",", " ").split()]
            return int(input_data)
        except ValueError:
            status_label.config(text="Invalid input! Please enter numbers only.")
            return None
    return None


def create_singly_linked_list(values):
    """Create a singly linked list from a list of values."""
    global sll
    if len(values) > max_size:
        messagebox.showerror("Error", f"List size cannot exceed {max_size}.")
        return
    sll = values


def insert_at_beginning(value):
    """Insert a value at the beginning of the linked list."""
    global sll
    if len(sll) >= max_size:
        messagebox.showerror("Error", f"Cannot insert. List size cannot exceed {max_size}.")
        return
    sll.insert(0, value)


def insert_at_end(value):
    """Insert a value at the end of the linked list."""
    global sll
    sll.append(value)


def insert_after_specific(value, after_value):
    """Insert a value after a specific value in the linked list."""
    global sll
    if len(sll) >= max_size:
        messagebox.showerror("Error", f"Cannot insert. List size cannot exceed {max_size}.")
        return False
    try:
        index = sll.index(after_value)
        sll.insert(index + 1, value)
    except ValueError:
        return False
    return True


def delete_from_beginning():
    """Delete a value from the beginning of the linked list."""
    global sll
    if sll:
        sll.pop(0)
        return True
    return False


def delete_from_end():
    """Delete a value from the end of the linked list."""
    global sll
    if sll:
        sll.pop()
        return True
    return False


def delete_specific(value):
    """Delete a specific value from the linked list."""
    global sll
    try:
        sll.remove(value)
        return True
    except ValueError:
        return False


def traverse():
    """Traverse and display the linked list."""
    status_label.config(text="Traversing elements...")

    px = -100
    arrow = None
    ptr = None
    i = 0


    def move_pointer():
        wait_if_paused()  # Check if paused during animation
        nonlocal px, arrow, ptr, i
        dx = 190  # Horizontal movement step size
        if i < len(sll):  # Move until the last node
            # Move the arrow and PTR text by dx units
            status_label.config(text=f"Traversed Element :- {sll[i]}")
            canvas.itemconfig(node_ids[i], fill="yellow")
            canvas.move(arrow, dx, 0)
            canvas.move(ptr, dx, 0)
            root.update()
            root.after(900)  # Pause for visualization
            root.update()
            canvas.itemconfig(node_ids[i], fill="lightblue")  # Reset color
            px += dx  # Update the current position
            i += 1
            move_pointer()
        else:
            return  # Stop moving after reaching the last node

    # Create the arrow and PTR text once, only for the first time
    arrow = canvas.create_line(px, 200, px, 150, arrow=tk.LAST, fill="black", width=3)
    ptr = canvas.create_text(px, 210, text="PTR", font=("Arial", 15, "bold"), fill="black")

    # Start the animation
    move_pointer()
    status_label.config(text="Traversing Completed")


def count_nodes():
    """Display the node count."""
    count = 1
    status_label.config(text="Counting elements...")

    px = -100
    arrow = None
    ptr = None
    i = 0


    def move_pointer():
        wait_if_paused()  # Check if paused during animation
        nonlocal px, arrow, ptr, i, count
        dx = 190  # Horizontal movement step size
        if i < len(sll):  # Move until the last node
            # Move the arrow and PTR text by dx units
            status_label.config(text=f"Count :- {count}")
            canvas.itemconfig(node_ids[i], fill="yellow")
            canvas.move(arrow, dx, 0)
            canvas.move(ptr, dx, 0)
            root.update()
            root.after(900)  # Pause for visualization
            root.update()
            canvas.itemconfig(node_ids[i], fill="lightblue")  # Reset color
            count += 1
            px += dx  # Update the current position
            i += 1
            move_pointer()
        else:
            return  # Stop moving after reaching the last node

    # Create the arrow and PTR text once, only for the first time
    arrow = canvas.create_line(px, 200, px, 150, arrow=tk.LAST, fill="black", width=3)
    ptr = canvas.create_text(px, 210, text="PTR", font=("Arial", 15, "bold"), fill="black")

    # Start the animation
    move_pointer()
    status_label.config(text=f"Total elements :- {count - 1}")


def search():
    """Search and display the search result."""
    if not sll:
        status_label.config(text="No elements in the array")
        return
    element = get_input("Enter element to be search :-")
    status_label.config(text=f"To Be Searched :- {element}")  # Display element to be searched
    found = False


    px = -100
    arrow = None
    ptr = None
    i = 0

    def move_pointer():
        wait_if_paused()  # Check if paused during animation
        nonlocal px, arrow, ptr, i, found
        dx = 190  # Horizontal movement step size

        # special case
        if i == len(sll):
            i -= 1
            if sll[i] == element:
                canvas.itemconfig(node_ids[i], fill="orange")
                canvas.move(arrow, dx, 0)
                canvas.move(ptr, dx, 0)
                root.update()
                root.after(1000)
                canvas.itemconfig(node_ids[i], fill="green")  # Highlight found element
                status_label.config(text=f"Element found !!")
                found = True
                root.update()
                root.after(5000)
                return
            return

        if sll[i] == element:
            canvas.itemconfig(node_ids[i], fill="orange")
            canvas.move(arrow, dx, 0)
            canvas.move(ptr, dx, 0)
            root.update()
            root.after(1000)
            canvas.itemconfig(node_ids[i], fill="green")  # Highlight found element
            status_label.config(text=f"Element found !!")
            found = True
            root.update()
            root.after(5000)
            return

        elif i < len(sll) and sll[i] != element:  # Move until the last node
            # Move the arrow and PTR text by dx units
            canvas.itemconfig(node_ids[i], fill="orange")
            canvas.move(arrow, dx, 0)
            canvas.move(ptr, dx, 0)
            root.update()
            root.after(700)
            canvas.itemconfig(node_ids[i], fill="lightblue")  # Reset color
            px += dx  # Update the current position
            i += 1
            move_pointer()



        else:
            return

    # Create the arrow and PTR text once, only for the first time
    arrow = canvas.create_line(px, 200, px, 150, arrow=tk.LAST, fill="black", width=3)
    ptr = canvas.create_text(px, 210, text="PTR", font=("Arial", 15, "bold"), fill="black")

    # Start the animation
    move_pointer()
    if not found:
        status_label.config(text="Element not found !!!")


def animate_ptr(operation, val):
    wait_if_paused()  # Check if paused during animation

    if operation == 1:
        px = -100
        arrow = None
        ptr = None
        i = 0


        def move_pointer():
            wait_if_paused()  # Check if paused during animation
            nonlocal px, arrow, ptr, i
            dx = 190  # Horizontal movement step size
            if i < len(sll):  # Move until the last node
                # Move the arrow and PTR text by dx units
                canvas.move(arrow, dx, 0)
                canvas.move(ptr, dx, 0)
                root.update()
                px += dx  # Update the current position
                i += 1
                root.after(750)  # Schedule the next frame
                move_pointer()
            else:
                # root.after(2500)
                return  # Stop moving after reaching the last node

        # Create the arrow and PTR text once, only for the first time
        arrow = canvas.create_line(px, 200, px, 150, arrow=tk.LAST, fill="black", width=3)
        ptr = canvas.create_text(px, 210, text="PTR", font=("Arial", 15, "bold"), fill="black")

        # Start the animation
        move_pointer()

    elif operation == 2:
        px = 90
        prex = -100
        arrow = None
        prearrow = None
        ptr = None
        preptr = None
        i = 0


        def move_pointer():
            wait_if_paused()  # Check if paused during animation
            nonlocal px, prex, arrow, prearrow, ptr, preptr, i
            dx = 190  # Horizontal movement step size
            if i <= sll.index(val):  # Move until the last node
                # Move the arrow and PTR text by dx units
                canvas.move(arrow, dx, 0)
                canvas.move(ptr, dx, 0)
                canvas.move(prearrow, dx, 0)
                canvas.move(preptr, dx, 0)
                root.update()
                px += dx  # Update the current position
                prex += dx
                i += 1
                root.after(750)  # Schedule the next frame
                move_pointer()
            else:
                return  # Stop moving after reaching the last node

        # Create the arrow and PTR text once, only for the first time
        arrow = canvas.create_line(px, 200, px, 150, arrow=tk.LAST, fill="black", width=3)
        ptr = canvas.create_text(px, 210, text="PTR", font=("Arial", 15, "bold"), fill="black")
        prearrow = canvas.create_line(prex, 200, prex, 150, arrow=tk.LAST, fill="black", width=3)
        preptr = canvas.create_text(prex, 210, text="Pre PTR", font=("Arial", 15, "bold"), fill="black")
        # Start the animation
        move_pointer()

    elif operation == 3:
        px = 90
        prex = -100
        arrow = None
        prearrow = None
        ptr = None
        preptr = None
        i = 0


        def move_pointer():
            wait_if_paused()  # Check if paused during animation
            nonlocal px, prex, arrow, prearrow, ptr, preptr, i
            dx = 190  # Horizontal movement step size
            if i < sll.index(val):  # Move until the last node
                # Move the arrow and PTR text by dx units
                canvas.move(arrow, dx, 0)
                canvas.move(ptr, dx, 0)
                canvas.move(prearrow, dx, 0)
                canvas.move(preptr, dx, 0)
                root.update()
                px += dx  # Update the current position
                prex += dx
                i += 1
                root.after(750)  # Schedule the next frame
                move_pointer()
            else:
                return  # Stop moving after reaching the last node

        # Create the arrow and PTR text once, only for the first time
        arrow = canvas.create_line(px, 200, px, 150, arrow=tk.LAST, fill="black", width=3)
        ptr = canvas.create_text(px, 210, text="PTR", font=("Arial", 15, "bold"), fill="black")
        prearrow = canvas.create_line(prex, 200, prex, 150, arrow=tk.LAST, fill="black", width=3)
        preptr = canvas.create_text(prex, 210, text="Pre PTR", font=("Arial", 15, "bold"), fill="black")
        # Start the animation
        move_pointer()

    elif operation == 4:
        px = 90
        prex = -100
        arrow = None
        prearrow = None
        ptr = None
        preptr = None
        i = 0


        def move_pointer():
            wait_if_paused()  # Check if paused during animation
            nonlocal px, prex, arrow, prearrow, ptr, preptr, i
            dx = 190  # Horizontal movement step size
            if i < len(sll) - 1:  # Move until the last node
                # Move the arrow and PTR text by dx units
                canvas.move(arrow, dx, 0)
                canvas.move(ptr, dx, 0)
                canvas.move(prearrow, dx, 0)
                canvas.move(preptr, dx, 0)
                root.update()
                px += dx  # Update the current position
                prex += dx
                i += 1
                root.after(750)  # Schedule the next frame
                move_pointer()
            else:
                return  # Stop moving after reaching the last node

        # Create the arrow and PTR text once, only for the first time
        arrow = canvas.create_line(px, 200, px, 150, arrow=tk.LAST, fill="black", width=3)
        ptr = canvas.create_text(px, 210, text="PTR", font=("Arial", 15, "bold"), fill="black")
        prearrow = canvas.create_line(prex, 200, prex, 150, arrow=tk.LAST, fill="black", width=3)
        preptr = canvas.create_text(prex, 210, text="Pre PTR", font=("Arial", 15, "bold"), fill="black")
        # Start the animation
        move_pointer()


# GUI for Linked List Operations
def run_operation():
    global current_algo, current_image_label
    operation = operation_var.get()


    def clear_previous_widgets():
        """Destroys previous algo and image_label widgets, if they exist."""
        global current_algo, current_image_label
        if current_algo is not None:
            current_algo.destroy()
            current_algo = None
        if current_image_label is not None:
            current_image_label.destroy()
            current_image_label = None

    # Update the image label dynamically instead of creating new labels each time
    current_image = images.get(operation, None)
    clear_previous_widgets()


    if operation == "Create Singly Linked List":
        input_values = get_input("Enter values separated by space or comma:", allow_multiple=True)
        if input_values:
            create_singly_linked_list(input_values)
            status_label.config(text="Singly Linked List Created!")
        clear_status_label()

    elif operation == "Insert at Beginning":

        # image and algorithm
        current_algo = tk.Label(canvas, text="Algorithm For Inserting Node at Beginning :- ", bg="white", fg="black",font=("Helvetica", 20, "bold"))
        current_algo.place(x=70, y=270)

        current_image_label = tk.Label(canvas, bg="white")
        current_image_label.config(image=current_image)
        current_image_label.place(x=710, y=230)

        input_data = get_input("Enter value to insert at the beginning:")
        if input_data is not None:
            insert_at_beginning(input_data)
            status_label.config(text="Inserted at Beginning.")
        clear_status_label()

    elif operation == "Insert at End":

        # image and algorithm
        current_algo = tk.Label(canvas, text="Algorithm For Inserting Node at End :- ", bg="white", fg="black",font=("Helvetica", 20, "bold"))
        current_algo.place(x=80, y=270)

        current_image_label = tk.Label(canvas, bg="white")
        current_image_label.config(image=current_image)
        current_image_label.place(x=690, y=230)

        input_data = get_input("Enter value to insert at the end:")
        if input_data is not None:
            if len(sll) < max_size:
                wait_if_paused()  # Check if paused during animation
                animate_ptr(1, 0)
                insert_at_end(input_data)
                status_label.config(text="Inserted at End.")
            else:
                messagebox.showerror("Error", f"Cannot insert. List size cannot exceed {max_size}.")
        clear_status_label()

    elif operation == "Insert after Specific":

        # image and algorithm
        current_algo = tk.Label(canvas, text="Algorithm For Inserting Node After a Node :- ", bg="white", fg="black",font=("Helvetica", 20, "bold"))
        current_algo.place(x=30, y=270)

        current_image_label = tk.Label(canvas, bg="white")
        current_image_label.config(image=current_image)
        current_image_label.place(x=690, y=240)

        after_value = get_input("Enter the value to insert after:")
        input_data = get_input("Enter value to insert:")
        if after_value is not None and input_data is not None:
            if len(sll) < max_size:
                animate_ptr(2, after_value)
                if insert_after_specific(input_data, after_value):
                    status_label.config(text=f"Inserted after {after_value}")
                else:
                    status_label.config(text="Value not found.")

            else:
                messagebox.showerror("Error", f"Cannot insert. List size cannot exceed {max_size}.")

        clear_status_label()

    elif operation == "Delete from Beginning":

        # image and algorithm
        current_algo = tk.Label(canvas, text="Algorithm For Deleting Node From Beginning :- ", bg="white", fg="black",font=("Helvetica", 20, "bold"))
        current_algo.place(x=30, y=270)

        current_image_label = tk.Label(canvas, bg="white")
        current_image_label.config(image=current_image)
        current_image_label.place(x=690, y=240)

        if delete_from_beginning():
            status_label.config(text="Deleted from Beginning.")
        else:
            status_label.config(text="List is empty.")
        clear_status_label()

    elif operation == "Delete from End":

        # image and algorithm
        current_algo = tk.Label(canvas, text="Algorithm For Deleting Node From End :- ", bg="white", fg="black",font=("Helvetica", 20, "bold"))
        current_algo.place(x=30, y=270)

        current_image_label = tk.Label(canvas, bg="white")
        current_image_label.config(image=current_image)
        current_image_label.place(x=620, y=240)

        wait_if_paused()  # Check if paused during animation
        animate_ptr(4, 0)
        if delete_from_end():
            status_label.config(text="Deleted from End.")
        else:
            status_label.config(text="List is empty.")
        clear_status_label()

    elif operation == "Delete Specific":

        # image and algorithm
        current_algo = tk.Label(canvas, text="Algorithm For Deleting Specific Node :- ", bg="white", fg="black",font=("Helvetica", 20, "bold"))
        current_algo.place(x=90, y=270)

        current_image_label = tk.Label(canvas, bg="white")
        current_image_label.config(image=current_image)
        current_image_label.place(x=700, y=240)

        input_data = get_input("Enter value to delete:")
        wait_if_paused()  # Check if paused during animation
        animate_ptr(3, input_data)
        if input_data is not None:
            if delete_specific(input_data):
                status_label.config(text=f"Deleted value {input_data}")
            else:
                status_label.config(text="Value not found.")
        clear_status_label()

    elif operation == "Traverse":

        # image and algorithm
        current_algo = tk.Label(canvas, text="Algorithm For Traversing Linked List :- ", bg="white", fg="black",font=("Helvetica", 20, "bold"))
        current_algo.place(x=90, y=270)

        current_image_label = tk.Label(canvas, bg="white")
        current_image_label.config(image=current_image)
        current_image_label.place(x=650, y=230)

        traverse()
        clear_status_label()

    elif operation == "Count Nodes":

        # image and algorithm
        current_algo = tk.Label(canvas, text="Algorithm For Counting Nodes in Linked List :- ", bg="white", fg="black",font=("Helvetica", 20, "bold"))
        current_algo.place(x=50, y=270)

        current_image_label = tk.Label(canvas, bg="white")
        current_image_label.config(image=current_image)
        current_image_label.place(x=700, y=230)

        count_nodes()
        clear_status_label()

    elif operation == "Search Element":

        # image and algorithm
        current_algo = tk.Label(canvas, text="Algorithm For Searching Nodes in Linked List :- ", bg="white", fg="black",font=("Helvetica", 20, "bold"))
        current_algo.place(x=50, y=270)

        current_image_label = tk.Label(canvas, bg="white")
        current_image_label.config(image=current_image)
        current_image_label.place(x=730, y=230)  # Check if paused during animation

        search()
        clear_status_label()

    update_visual()


def clear_status_label(delay=3000):
    root.after(delay, lambda: status_label.config(text=""))


node_ids = {}


def update_visual():
    """Update the visual representation of the singly linked list."""
    global node_ids
    node_ids.clear()
    canvas.delete("all")  # Clear previous drawings
    canvas.create_window(780, 30, window=status_label)
    wait_if_paused()  # Check if paused during animation

    # Parameters for drawing the nodes
    rect_width, rect_height = 100, 50  # Size of each node
    next_width = 50  # Width for the next pointer box
    nodes_per_row = 8
    margin = 40  # Increased margin between nodes
    x_start = margin  # Initial x position
    y_start = 100  # Initial y position


    x, y = x_start, y_start  # Start drawing at this position

    if len(sll) == 0:
        # If the list is empty, stop here after clearing the canvas
        return

    for i, value in enumerate(sll):
        wait_if_paused()  # Check if paused during animation
        # Data portion for both directions
        data_x = x
        pointer_x = x + rect_width // 2

        # Draw the data section
        data_rect_id = canvas.create_rectangle(data_x, y, data_x + rect_width // 2, y + rect_height,
                                               fill="lightblue", outline="black")
        canvas.create_text(data_x + rect_width // 4, y + rect_height // 2, text=str(value),
                           fill="black", font=("Helvetica", 18))

        # Draw the next portion (pointer section)
        canvas.create_rectangle(pointer_x, y, pointer_x + next_width, y + rect_height, fill="lightgray",
                                outline="black")

        node_ids[i] = data_rect_id

        if i < len(sll) - 1:
            wait_if_paused()  # Check if paused during animation
            # Draw an arrow connecting the nodes
            next_node_x = x + rect_width + margin  # x position of the next node's left edge
            canvas.create_line(data_x + rect_width - 30, y + rect_height // 2, next_node_x + 50, y + rect_height // 2,
                               arrow=tk.LAST, fill="black", width=3)

        else:
            wait_if_paused()  # Check if paused during animation
            # Mark the last node's next portion as "NULL"
            canvas.create_text(pointer_x + next_width // 2, y + rect_height // 2, text="NULL", fill="black",
                               font=("Helvetica", 12))

        # Move to the next node
        x += 1 * (rect_width + margin + next_width)

    # start pointer
    canvas.create_line(70, 55, 70, 100, arrow=tk.LAST, fill="black", width=3)
    canvas.create_text(70, 45, text="Start", font=("Arial", 15, "bold"), fill="black")


run_button = tk.Button(root, text="Run Operation", command=run_operation, bg="lightblue",fg="black", font=("Helvetica", 12))
run_button.grid(row=0, column=1, padx=10, pady=10)
root.bind('<Return>', lambda event: run_operation())

# Create a Pause/Resume button
pause_button = tk.Button(root, text="Pause", command=toggle_pause, font=("Helvetica" , 12), bg="lightblue", activebackground="white", width=10)
pause_button.place(x=1350, y=13)

root.mainloop()