import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from tkinter import font as tkfont
import time

# Initialize array
a = []
MAX_SIZE = 10
paused = False

# Function to display the array with visualization

def toggle_pause():

    # Toggle the paused state and update the button text.

    global paused
    paused = not paused
    pause_button.config(text="Resume" if paused else "Pause")


def wait_if_paused():

    # Pause execution if the paused flag is set to True.

    while paused:
        canvas.update()
        time.sleep(0.1)  # Check periodically to minimize CPU usage

def display_algorithm(operation):

    if operation ==    1:
        algo_canvas.create_text(120, 30, text = "1) A is an array", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(300, 80, text = "2) N indicates number of elements in an array", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(265, 135, text = "3) POS indicates index to insert element", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(270, 200, text = "4) Value indicates element to be inserted", font=("Helvetica", 20),fill="black")
        algo_canvas.create_text(790, 30, text = "Step 1 :- TEMP <-- N-1", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(940, 80, text = "Step 2 :- Repeat step :- 3,4 until TEMP >= POS", font=("Helvetica", 20),fill="black")
        algo_canvas.create_text(880, 130, text = "Step 3 :- A [ TEMP + 1 ] <-- A [ TEMP ] ", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(825, 180, text = "Step 4 :- TEMP <-- TEMP + 1", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(820, 220, text="Step 5 :- A[ POS ] <-- VALUE", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(1200,215, text="Step 6 :- N <-- N + 1", font=("Helvetica", 20), fill="black")

    elif operation ==  2:
        algo_canvas.create_text(120, 30, text = "1) A is an array", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(300, 80, text = "2) N indicates number of elements in an array", font=("Helvetica", 20),fill="black")
        algo_canvas.create_text(265, 135, text = "3) POS indicates index to delete element", font=("Helvetica", 20),fill="black")
        algo_canvas.create_text(800, 30, text = "Step 1 :- TEMP <-- POS", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(940, 80, text = "Step 2 :- Repeat step :- 3,4 until TEMP <= N - 1", font=("Helvetica", 20),fill="black")
        algo_canvas.create_text(885, 130, text = "Step 3 :- A [ TEMP ] <-- A [ TEMP + 1 ] ", font=("Helvetica", 20),fill="black")
        algo_canvas.create_text(825, 180, text = "Step 4 :- TEMP <-- TEMP + 1", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(765, 225, text = "Step 5 :- N <-- N - 1", font=("Helvetica", 20), fill="black")

    elif operation ==  3:
        algo_canvas.create_text(220, 30, text="Step 1 :- I <-- 0, J <-- 0, K <-- 0", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(295, 80, text="Step 2 :- Repeat step :- 3,4,5 until I <= N - 1", font=("Helvetica", 20),fill="black")
        algo_canvas.create_text(175, 125, text="Step 3 :- C[ K ] <-- A[ I ]", font=("Helvetica", 20),fill="black")
        algo_canvas.create_text(140, 170, text="Step 4 :- I <-- I + 1", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(150, 220, text="Step 5 :- K <-- K + 1", font=("Helvetica", 20),fill="black")
        algo_canvas.create_text(860, 30, text="Step 6 :- Repeat step :- 7,8,9 until J <= M - 1", font=("Helvetica", 20),fill="black")
        algo_canvas.create_text(735, 80, text="Step 7 :- C[ K ] <-- B[ J ]", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(705, 130, text="Step 8 :- J <-- J + 1", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(710, 175, text="Step 9 :- K <-- K + 1", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(690, 220, text="Step 10 :- I <-- 0", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(1140, 115, text="Step 11 :- Repeat step :- 12,13 until", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(1195, 145, text="I <= K - 1",font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(1045, 185, text="Step 12 :- print C[ I ]", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(1045, 225, text="Step 13 :- I <-- I + 1", font=("Helvetica", 20), fill="black")

    elif operation ==  4:
        algo_canvas.create_text(200, 30, text = "1) A is an array", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(285, 100, text = "2) LB is lower limit of an array", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(290, 170, text = "3) UB is Upper limit of an array", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(870, 30, text = "Step 1 :- Count <-- LB",font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(1010, 80, text = "Step 2 :- Repeat step :- 3,4 until Count <= UB", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(870, 140, text = "Step 3 :- print A[count]", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(910, 190, text = "Step 4 :- Count <-- Count + 1", font=("Helvetica", 20), fill="black")

    elif operation ==  5:
        algo_canvas.create_text(200, 30, text = "1) A is an array", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(285, 100, text = "2) LB is lower limit of an array", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(290, 170, text = "3) UB is Upper limit of an array", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(870, 30, text = "Step 1 :- Count <-- LB", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(1000, 80, text = "Step 2 :- Repeat step :- 3 until Count <= UB", font=("Helvetica", 20),fill="black")
        algo_canvas.create_text(910, 140, text = "Step 3 :- Count <-- Count + 1", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(850, 200, text = "Step 4 :- print count", font=("Helvetica", 20), fill="black")

    elif operation ==  6:
        algo_canvas.create_text(140, 30, text="1) A is an array", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(315, 100, text="2) N indicates number of elements in an array", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(290, 170, text="3) KEY indicates element to be searched", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(750, 30, text="Step 1 :- I <-- 0", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(910, 80, text="Step 2 :- Repeat step :- 3,4 until I <= N - 1", font=("Helvetica", 20),fill="black")
        algo_canvas.create_text(885, 135, text="Step 3 :- IF A[ I ] = KEY  Then return I", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(770, 185, text="Step 4 :- I <-- I + 1", font=("Helvetica", 20), fill="black")
        algo_canvas.create_text(760, 230, text="Step 5 :- return -1", font=("Helvetica", 20), fill="black")

def display_array(canvas, array):
    canvas.delete("all")  # Clear the canvas
    rect_width = 60
    rect_height = 40
    spacing = 10
    for i, element in enumerate(array):
        x1 = spacing + i * (rect_width + spacing) + 150
        y1 = 100
        x2 = x1 + rect_width
        y2 = y1 + rect_height
        canvas.create_rectangle(x1, y1, x2, y2, fill="#ADD8E6", outline="#00008B", tags=f"rect_{i}")
        canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=str(element), font=("Helvetica", 15 , "bold"), fill="darkblue",
                           tags=f"text_{i}")

        # Display index below the rectangle
        canvas.create_text((x1 + x2) // 2, y2 + 15, text= i, font=("Helvetica", 13 , "bold"), fill="black",
                           tags=f"index_{i}")

    canvas.update()


def display_message(text):
    # Function to display any result below the array
    result_label.config(text=text)


def get_integer(prompt):
    while True:
        try:
            value = simpledialog.askinteger("Input", prompt)
            if value is not None:
                return value
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid integer.")


def create_array():
    global a
    values = simpledialog.askstring("Create Array", "Enter comma-separated values:")
    if values:
        # Convert the string input to a list of integers
        new_array = [int(x.strip()) for x in values.split(",") if x.strip().isdigit()]
        if len(new_array) > MAX_SIZE:
            messagebox.showerror("Error", f"Array size cannot exceed {MAX_SIZE}.")
        else:
            a = new_array
            display_array(canvas, a)
            display_message(f"Array created: {a}")


def insert_element():
    global a
    if len(a) >= MAX_SIZE:
        messagebox.showerror("Error", f"Cannot insert. Array size cannot exceed {MAX_SIZE}.")
        return

    # Ask for index and value
    index = get_integer("Enter index:")
    if index is None or not (0 <= index <= len(a)):
        display_message("Invalid index")
        return
    element = get_integer("Enter element:")
    if element is None:
        return

    display_message("Shifting elements to make space...")
    canvas.update()

    # Step 1: Animate shifting elements to the right
    a.append(None)  # Temporarily add a placeholder
    for i in range(len(a) - 2, index - 1, -1):  # Start shifting from the end
        animate_rectangle(i, "yellow")  # Highlight the element being shifted
        a[i + 1] = a[i]  # Move the value one position to the right
        display_array(canvas, a)  # Redraw the array with updated positions
        animate_rectangle(i + 1, "yellow")
        time.sleep(0.7)  # Pause for smooth visualization

    # Step 2: Insert the new element
    a[index] = element
    display_array(canvas, a)  # Update array display
    animate_rectangle(index, "orange")  # Highlight the insertion index
    display_message(f"Element {element} inserted at index {index}")


def delete_element():
    global a
    if not a:  # Check if the array is empty
        display_message("No elements in the array to delete.")
        return

    # Step 1: Prompt the user for the index to delete
    index = get_integer("Enter the index to delete:")
    if index is None or not (0 <= index < len(a)):
        display_message("Invalid index")
        return

    display_message(f"Deleting element at index {index}...")
    canvas.update()
    time.sleep(0.5)

    # Step 2: Highlight the element being deleted
    animate_rectangle(index, "red")  # Highlight the element to delete
    time.sleep(0.7)

    # Step 3: Animate shifting the elements to the left
    for i in range(index + 1, len(a)):  # Shift elements to the left
        animate_rectangle(i, "yellow")  # Highlight the element being shifted
        a[i - 1] = a[i]  # Move the value left
        display_array(canvas, a)  # Update array display
        animate_rectangle(i-1, "yellow")
        time.sleep(0.7)

    # Step 4: Remove the last element after shifting
    a.pop()
    display_array(canvas, a)  # Final array display
    display_message(f"Element at index {index} has been deleted.")


def traverse():
    display_message("Traversing elements...")
    for i ,_ in enumerate(a):
        display_message(f"Traversed Element :- {a[i]}")
        time.sleep(0.7)
        animate_rectangle(i, "yellow")  # Highlight each element

    display_message("Traversing Completed")


def search_element():
    if not a:
        display_message("No elements in the array")
        return
    selement = get_integer("Enter element to search:")
    display_message(f"To Be Searched: {selement}")  # Display element to be searched
    found = False

    for i, element in enumerate(a):
        animate_rectangle(i, "orange")  # Highlight the current element
        root.after(700)
        if element == selement:
            canvas.itemconfig(f"rect_{i}", fill="green")  # Highlight found element
            canvas.update()  # Update canvas to reflect changes
            display_message(f"Element found at index {i}")
            found = True
            break

    if not found:
        display_message("Element not found")


def merge_array():
    global a
    values = simpledialog.askstring("Merge Array", "Enter comma-separated values:")
    if values:
        new_elements = [int(x.strip()) for x in values.split(",") if x.strip().isdigit()]
        if len(a) + len(new_elements) > MAX_SIZE:
            messagebox.showerror("Error", f"Cannot merge. Array size cannot exceed {MAX_SIZE}.")
        else:
            a.extend(new_elements)
            display_array(canvas, a)
            display_message("Array Merged")


def count_elements():
    count = 0
    display_message("Counting elements...")
    for i, _ in enumerate(a):
        animate_rectangle(i, "yellow")  # Highlight each element as it is counted
        count += 1
        display_message(f"Count :- {count}")  # Update count after traversing each element
    display_message(f"Total elements :- {count}")


def reset_array():
    global a
    a.clear()
    canvas.delete("all")
    display_message("Array has been reset.")


# Function to handle the operation submission
def submit_operation(event=None):
    choice = operation_var.get()
    if choice == "Create Array":
        create_array()

    elif choice == "Insert Element":
        algo_canvas.delete("all")
        display_algorithm(1)
        insert_element()

    elif choice == "Delete Element":
        algo_canvas.delete("all")
        display_algorithm(2)
        delete_element()

    elif choice == "Merge Array":
        algo_canvas.delete("all")
        display_algorithm(3)
        merge_array()

    elif choice == "Traverse Element":
        algo_canvas.delete("all")
        display_algorithm(4)
        traverse()

    elif choice == "Count Elements":
        algo_canvas.delete("all")
        display_algorithm(5)
        count_elements()

    elif choice == "Search Element":
        algo_canvas.delete("all")
        display_algorithm(6)
        search_element()

    elif choice == "Reset":
        algo_canvas.delete("all")
        reset_array()


def animate_rectangle(index, color):
    # Animate the rectangle to show which element is being processed
    canvas.itemconfig(f"rect_{index}", fill=color)
    canvas.update()
    time.sleep(0.5)  # Pause for visualization
    wait_if_paused()  # Check if paused during animation
    canvas.itemconfig(f"rect_{index}", fill="#ADD8E6")  # Reset color



# Create main window
root = tk.Tk()
root.title("Array Operations with Visualization")
root.configure(bg="lightblue")
root.geometry("1540x810")

# Customize fonts and styles
title_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
button_font = tkfont.Font(family="Helvetica", size=12)
highlight_color = "#FFD700"

# Create dropdown menu for selecting operations at the top
operation_var = tk.StringVar(value="Select Operation")
operation_menu = ttk.Combobox(root, textvariable=operation_var, values=[
    "Create Array", "Insert Element", "Delete Element", "Merge Array", "Traverse Element", "Count Elements", "Search Element","Reset"
], state="readonly", width=30, font=button_font)
operation_menu.pack(pady=10)

# Create a canvas for algorithm
algo_canvas = tk.Canvas(root, width=1430, height=250, highlightthickness=5, highlightbackground=highlight_color)
algo_canvas.place(x = 50 , y = 500)

#algorithm label
algo_label = tk.Label(root , text = "Algorithm :- " , font=("Helvetica", 17 , "bold"), bg="lightblue" , fg="black")
algo_label.place(x = 70 , y = 460)

# Create a canvas frame with gradient background
canvas_frame = tk.Frame(root, bg="lightblue", padx=10, pady=10)
canvas_frame.pack(pady=10)
canvas = tk.Canvas(canvas_frame, width=1000, height=300, bg="#E6E6FA", highlightthickness=5, highlightbackground=highlight_color)
canvas.pack(pady=10)

# Label for showing results below the array
result_label = tk.Label(root, text="", font=("Helvetica", 15), bg="lightblue" , fg="darkblue")
result_label.place(x =670 , y = 400)

# Submit button and bind Enter key to submit operation
submit_button = tk.Button(root, text="Submit Operation", command=submit_operation, font=button_font, bg=highlight_color, activebackground="orange", width=25)
submit_button.place(x =650 , y = 450)
root.bind('<Return>', submit_operation)

# Create a Pause/Resume button
pause_button = tk.Button(root, text="Pause", command=toggle_pause, font=button_font, bg=highlight_color, activebackground="orange", width=10)
pause_button.place(x=1350, y=450)


#size of array
size_label = tk.Label(root, text="Array size :- 10", font=("Helvetica", 15), bg="#E6E6FA", fg="black")
size_label.place(x = 300 , y = 100)

# Start the GUI loop
root.mainloop()