import tkinter as tk
import math
from PIL import Image, ImageTk
import os

# Set base directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the relative path to the images folder
images_dir = os.path.join(base_dir, "../other imp files")


# Initialize the circular queue with a maximum length
MAX_QUEUE_SIZE = 10
queue = [None] * MAX_QUEUE_SIZE  # Use a fixed size list
front = rear = -1

# Define static colors
box_color = "#76c7c0"  # Color for filled queue boxes
empty_box_color = "#ffffff"  # Color for empty boxes
bg_color = "#33ffff"  # Light background color for the window
status_bg_color = "#e6f7ff"  # Background color for status labels

# Function to update the visualization of the circular queue
def update_queue_display():
    canvas.delete("all")  # Clear previous queue visualization

    # Parameters for circular layout
    radius = 160  # Radius of the circular layout
    center_x = 300  # Center X position of the circle
    center_y = 200  # Center Y position of the circle

    # Draw the queue boxes and indexes
    for i in range(MAX_QUEUE_SIZE):
        angle = 2 * math.pi * i / MAX_QUEUE_SIZE  # Calculate angle for each position
        x = center_x + radius * math.cos(angle)  # X position of the box
        y = center_y + radius * math.sin(angle)  # Y position of the box

        # Draw boxes with static colors
        if (front != -1) and ((front <= rear and i >= front and i <= rear) or (front > rear and (i >= front or i <= rear))):
            # Filled box color
            canvas.create_rectangle(x - 30, y - 20, x + 30, y + 20, outline="black", width=2, fill=box_color)
            # Display elements from the queue
            canvas.create_text(x, y, text=str(queue[i]), font=("Arial", 16))
        else:
            # Empty box color
            canvas.create_rectangle(x - 30, y - 20, x + 30, y + 20, outline="black", width=2, fill=empty_box_color)

        # Draw index below each box
        canvas.create_text(x, y + 30, text=f"{i}", font=("Arial", 12 , "bold"))


    # Add front and rear arrows

    if front == -1:
        canvas.create_text(510,140, text="Front = -1", font=("Arial", 15), fill="blue")

    if rear == -1:
        canvas.create_text(510, 160, text="Rear = -1", font=("Arial", 15), fill="green")

    if front != -1:
        # Arrow for front pointer
        front_angle = 2 * math.pi * front / MAX_QUEUE_SIZE
        front_x = center_x + radius * math.cos(front_angle)
        front_y = center_y + radius * math.sin(front_angle)
        canvas.create_line(front_x, front_y - 40, front_x, front_y - 10, arrow=tk.LAST, fill="blue", width=2)
        canvas.create_text(front_x, front_y - 50, text="Front", font=("Arial", 15), fill="blue")

    if rear != -1:
        # Arrow for rear pointer
        rear_angle = 2 * math.pi * rear / MAX_QUEUE_SIZE
        rear_x = center_x + radius * math.cos(rear_angle)
        rear_y = center_y + radius * math.sin(rear_angle)
        canvas.create_line(rear_x, rear_y - 40, rear_x, rear_y - 10, arrow=tk.LAST, fill="green", width=2)
        canvas.create_text(rear_x, rear_y - 50, text="Rear", font=("Arial", 15), fill="green")

# Function to check if queue is empty (underflow)
def is_underflow():
    return front == -1

# Function to check if queue is full (overflow)
def is_overflow():
    return (rear + 1) % MAX_QUEUE_SIZE == front

# Function for enqueue operation
def enqueue():
    global front, rear

    if is_overflow():
        status_label.config(text="Queue Overflow !",font = ("Helvetica", 20 , "bold") ,fg="red", bg=status_bg_color)
        status_label.place(x=640, y=530)
        return

    try:
        value = int(entry.get())
        if is_underflow():
            front = rear = 0  # Both pointers point to 0 for the first element
        else:
            rear = (rear + 1) % MAX_QUEUE_SIZE  # Move rear to the next position

        queue[rear] = value  # Insert the new value at the rear
        update_queue_display()
        status_label.config(text=f"{value} inserted successfully !",font = ("Helvetica", 20 , "bold") , fg="green", bg=status_bg_color)
        status_label.place(x=610, y=530)
        entry.delete(0, tk.END)  # Clear the entry field
    except ValueError:
        status_label.config(text="Please enter a valid integer.",font = ("Helvetica", 20 , "bold") , fg="red", bg=status_bg_color)
        status_label.place(x=570, y=530)

# Function for dequeue operation
def dequeue():
    global front, rear

    if is_underflow():
        status_label.config(text="Queue Underflow !",font = ("Helvetica", 20 , "bold") , fg="red", bg=status_bg_color)
        status_label.place(x=640, y=530)  # Fixed position for the status label
        return

    deleted = queue[front]
    status_label.config(text=f"{deleted} deleted successfully !",font = ("Helvetica", 20 , "bold") , fg="red", bg=status_bg_color)
    status_label.place(x=610, y=530)  # Fixed position for the status label

    # Move front pointer ahead or reset pointers if queue is empty
    if front == rear:
        front = rear = -1  # Reset the queue when it becomes empty
    else:
        front = (front + 1) % MAX_QUEUE_SIZE  # Move front to the next position

    update_queue_display()

# Function to exit the application
def exit_app():
    root.quit()

# Main Tkinter window setup
root = tk.Tk()
root.title("Circular Queue Visualization")
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
canvas = tk.Canvas(root, width=600, height=400, bg="white")
canvas.place(x = 450 , y = 100)


# Algorithm enqueue
algorithm_enqueue_label = tk.Label(root,text="Algorithm for Enqueue element :- ", font=("Arial", 20, "bold"),bg="#33FFFF", fg="black")
algorithm_enqueue_label.place(x=15, y=60)

# Image for enqueue
enqueue_image_path = os.path.join(images_dir, "images", "circular_enqueue.png")
enqueue_image_label = tk.Label(root,bg="#e6f7ff")
en = ImageTk.PhotoImage(Image.open(enqueue_image_path).resize((500, 600), Image.Resampling.LANCZOS))
enqueue_image_label.config(image=en)
enqueue_image_label.place(x=15, y=100)


# Algorithm dequeue
algorithm_dequeue_label = tk.Label(root,text="Algorithm for Dequeue element :- ", font=("Arial", 20, "bold"),bg="#33FFFF", fg="black")
algorithm_dequeue_label.place(x=1020, y=60)

# Image for dequeue
dequeue_image_path = os.path.join(images_dir, "images", "circular_dequeue.png")
dequeue_image_label = tk.Label(root,bg="#e6f7ff")
de = ImageTk.PhotoImage(Image.open(dequeue_image_path).resize((500, 600), Image.Resampling.LANCZOS))
dequeue_image_label.config(image=de)
dequeue_image_label.place(x=1015, y=100)

# Label for status messages
status_label = tk.Label(root, text="")

# Start with an empty queue visualization
update_queue_display()

# Start the Tkinter event loop
root.mainloop()
