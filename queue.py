import tkinter as tk
from collections import deque

from PIL import Image, ImageTk
import os

# Set base directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the relative path to the images folder
images_dir = os.path.join(base_dir, "../other imp files")



# Initialize the queue and front/rear pointers
queue = deque(maxlen=10)
front = rear = -1

# Define static colors
box_color = "#76c7c0"  # Color for filled queue boxes
empty_box_color = "#ffffff"  # Color for empty boxes
bg_color = "#33FFFF"  # Light background color for the window
status_bg_color = "#e6f7ff"  # Background color for status labels


# Function to update the visualization of the queue
def update_queue_display():
    canvas.delete("all")  # Clear previous queue visualization

    # Dimensions for visual elements on the canvas
    box_width = 60
    box_height = 40
    start_x = 50
    start_y = 150

    # Draw the queue boxes and indexes
    for i in range(10):
        x1 = start_x + i * (box_width + 10)
        x2 = x1 + box_width
        y1 = start_y
        y2 = y1 + box_height

        # Draw boxes with static colors
        if i <= rear:
            # Filled box color
            canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=2, fill=box_color)
        else:
            # Empty box color
            canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=2, fill=empty_box_color)

        # Display elements from the queue based on front and rear pointers
        if front != -1 and front <= i <= rear:
            value = queue[i]
            canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(value), font=("Arial", 16))

        # Draw index below each box
        canvas.create_text((x1 + x2) / 2, y2 + 20, text=f"{i}", font=("Arial", 12 , "bold"))

    # Add front and rear arrows

    if front == -1:
        canvas.create_text(50,110, text="Front = -1", font=("Arial", 15), fill="blue")

    if rear == -1:
        canvas.create_text(50, 130, text="Rear = -1", font=("Arial", 15), fill="green")

    if front != -1:
        # Arrow for front pointer
        front_x = start_x + front * (box_width + 10) + box_width / 2
        canvas.create_line(front_x, start_y - 20, front_x, start_y, arrow=tk.LAST, fill="blue", width=2)
        canvas.create_text(front_x, start_y - 30, text="Front", font=("Arial", 15), fill="blue")

    if rear != -1:
        # Arrow for rear pointer
        rear_x = start_x + rear * (box_width + 10) + box_width / 2
        canvas.create_line(rear_x, start_y - 40, rear_x, start_y, arrow=tk.LAST, fill="green", width=2)
        canvas.create_text(rear_x, start_y - 50, text="Rear", font=("Arial", 15), fill="green")

# Function to check if queue is empty (underflow)
def is_underflow():
    return front == -1 and rear == -1

# Function to check if queue is full (overflow)
def is_overflow():
    return rear == 9

# Function for enqueue operation
def enqueue():
    global front, rear

    if is_overflow():
        status_label.config(text="Queue Overflow!",font = ("Helvetica", 20 , "bold") ,fg="red", bg=status_bg_color)
        status_label.place(x=640, y=110)  # Fixed position for the status label
        return

    try:
        value = int(entry.get())
        if is_underflow():
            front = rear = 0  # Both pointers point to 0 for the first element
        else:
            rear += 1

        queue.append(value)
        update_queue_display()
        status_label.config(text=f"{value} inserted successfully !",font = ("Helvetica", 20 , "bold"), fg="green", bg=status_bg_color)
        status_label.place(x=610, y=110)  # Fixed position for the status label
        entry.delete(0, tk.END)  # Clear the entry field
    except ValueError:
        status_label.config(text="Please enter a valid integer.",font = ("Helvetica", 20 , "bold") ,fg="red", bg=status_bg_color)
        status_label.place(x=610, y=110)  # Fixed position for the status label

# Function for dequeue operation
def dequeue():
    global front, rear

    if is_underflow():
        status_label.config(text="Queue Underflow!",font = ("Helvetica", 20 , "bold") ,fg="red", bg=status_bg_color)
        status_label.place(x=640, y=110)  # Fixed position for the status label
        return
    else:
        deleted = queue[front]
        status_label.config(text=f"{deleted} deleted successfully!",font = ("Helvetica", 20 , "bold") ,fg="red", bg=status_bg_color)
        status_label.place(x=630, y=110)  # Fixed position for the status label)

        # Move front pointer ahead or reset pointers if queue is empty
        if front == rear:
            front = rear = -1  # Reset the queue when it becomes empty
        else:
            front += 1

        update_queue_display()

# Function to exit the application
def exit_app():
    root.quit()

# Main Tkinter window setup
root = tk.Tk()
root.title("Queue Visualization with Animation")
root.geometry("1540x810")
root.configure(bg=bg_color)  # Set a nice background color for the window

# Input frame
input_frame = tk.Frame(root, bg=bg_color)
input_frame.pack(pady=20)

# Entry field to input the value to enqueue
entry_label = tk.Label(input_frame, text="Enter value :-", font=("Arial", 14), bg=bg_color)
entry_label.grid(row=0, column=0, padx=10)

entry = tk.Entry(input_frame, font=("Arial", 14))
entry.grid(row=0, column=1, padx=10)

# Buttons for enqueue, dequeue, and exit
enqueue_button = tk.Button(input_frame, text="Enqueue", font=("Arial", 14), command=enqueue, bg="#4CAF50", fg="white")
enqueue_button.grid(row=0, column=2, padx=10)

dequeue_button = tk.Button(input_frame, text="Dequeue", font=("Arial", 14), command=dequeue, bg="#F44336", fg="white")
dequeue_button.grid(row=0, column=3, padx=10)

exit_button = tk.Button(input_frame, text="Exit", font=("Arial", 14), command=exit_app, bg="#2196F3", fg="white")
exit_button.grid(row=0, column=4, padx=10)

# Display frame with Canvas to show the visual representation of the queue
canvas = tk.Canvas(root, width=800, height=230, bg="white")
canvas.pack(pady=5)

# Label for status messages
status_label = tk.Label(root, text="", font=("Arial", 12), fg="green", bg=status_bg_color)
status_label.place(x=690, y=110)

# Start with an empty queue visualization
update_queue_display()


# Algorithm enqueue
algorithm_enqueue_label = tk.Label(root,text="Algorithm for Enqueue element :- ", font=("Arial", 20, "bold"),bg="#33FFFF", fg="black")
algorithm_enqueue_label.place(x=55, y=330)

# Image for enqueue
enqueue_image_path = os.path.join(images_dir, "images", "enqueue.png")
enqueue_image_label = tk.Label(root,bg="#e6f7ff")
en = ImageTk.PhotoImage(Image.open(enqueue_image_path).resize((700, 400), Image.Resampling.LANCZOS))
enqueue_image_label.config(image=en)
enqueue_image_label.place(x=50, y=370)


# Algorithm dequeue
algorithm_dequeue_label = tk.Label(root,text="Algorithm for Dequeue element :- ", font=("Arial", 20, "bold"),bg="#33FFFF", fg="black")
algorithm_dequeue_label.place(x=810, y=330)

# Image for dequeue
dequeue_image_path = os.path.join(images_dir, "images", "dequeue.png")
dequeue_image_label = tk.Label(root,bg="#e6f7ff")
de = ImageTk.PhotoImage(Image.open(dequeue_image_path).resize((700, 400), Image.Resampling.LANCZOS))
dequeue_image_label.config(image=de)
dequeue_image_label.place(x=800, y=370)


# Start the Tkinter event loop
root.mainloop()
