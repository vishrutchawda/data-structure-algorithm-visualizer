import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os


# Set base directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the relative path to the images folder
images_dir = os.path.join(base_dir, "../other imp files")

class StackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stack Operations GUI")
        self.root.geometry("1540x810")  # Set window size
        self.root.configure(bg="#33FFFF")

        self.stack = []
        self.stack_limit = 10

        # Title Label
        self.title_label = tk.Label(root, text="Welcome to the Stack Program!", font=("Arial", 16, "bold"),
                                     bg="#33FFFF", fg="black")
        self.title_label.pack(pady=10)

        # Dropdown menu for selecting operation
        self.operation_var = tk.StringVar(value="Push/Pop")
        self.operation_menu = tk.OptionMenu(root, self.operation_var, "Push/Pop", "Sequence",
                                             command=self.change_frame)
        self.operation_menu.pack(pady=10)

        # Frames for different operations
        self.push_pop_frame = tk.Frame(root, bg="#33FFFF")
        self.sequence_frame = tk.Frame(root, bg="#33FFFF")

        # Initialize frames
        self.setup_push_pop_frame()
        self.setup_sequence_frame()


        # Show the push/pop frame by default
        self.push_pop_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas for visualizing stack
        self.stack_canvas = tk.Canvas(root, bg="#F0F8FF", height=500, width=400)  # Adjust canvas height
        self.stack_canvas.pack(pady=10)


        # Stack size label
        self.size_label = tk.Label(root, text="Stack size :- 10", font=("Helvetica", 15), bg="#F0F8FF", fg="black")
        self.size_label.place(x=600, y=130)

        # Algorithm push
        self.algorithm_push_label = tk.Label(root, text="Algorithm for push element :- ", font=("Arial", 20, "bold"),
                                             bg="#33FFFF", fg="black")
        self.algorithm_push_label.place(x=50, y=100)

        # Image for push
        push_image_path = os.path.join(images_dir, "images", "stack_push.png")
        self.push_image_label = tk.Label(root, bg="#e6f7ff")
        self.pu = ImageTk.PhotoImage(Image.open(push_image_path).resize((500, 500), Image.Resampling.LANCZOS))
        self.push_image_label.config(image=self.pu)
        self.push_image_label.place(x=50, y=150)

        # Algorithm for pop
        self.algorithm_pop_label = tk.Label(root, text="Algorithm for pop element :- ", font=("Arial", 20, "bold"),
                                            bg="#33FFFF", fg="black")
        self.algorithm_pop_label.place(x=1000, y=100)

        # Image for pop
        pop_image_path = os.path.join(images_dir, "images", "stack_pop.png")
        self.pop_image_label = tk.Label(root, bg="#e6f7ff")
        self.po = ImageTk.PhotoImage(Image.open(pop_image_path).resize((500, 500), Image.Resampling.LANCZOS))
        self.pop_image_label.config(image=self.po)
        self.pop_image_label.place(x=1000, y=150)

        # Call change_frame to display the appropriate frame
        self.change_frame(self.operation_var.get())


    def toggle_push_pop_elements(self, show):
        """Show or hide elements related to Push/Pop operations."""
        if show:
            self.size_label.place(x=600, y=130)
            self.algorithm_push_label.place(x=50, y=100)
            self.push_image_label.place(x=50, y=150)
            self.algorithm_pop_label.place(x=1000, y=100)
            self.pop_image_label.place(x=1000, y=150)
        else:
            self.size_label.place_forget()
            self.algorithm_push_label.place_forget()
            self.push_image_label.place_forget()
            self.algorithm_pop_label.place_forget()
            self.pop_image_label.place_forget()

    def setup_push_pop_frame(self):
        """Setup UI for Push/Pop operations."""

        self.push_label = tk.Label(self.push_pop_frame, text="Enter value to push:", font=("Arial", 12), bg="#33FFFF")
        self.push_label.pack(pady=5)

        self.push_input = tk.Entry(self.push_pop_frame, font=("Arial", 12))
        self.push_input.pack(pady=5)

        self.push_button = tk.Button(self.push_pop_frame, text="Push", font=("Arial", 12), bg="#32CD32", fg="white",
                                     command=self.push_value)
        self.push_button.pack(pady=5)

        self.pop_button = tk.Button(self.push_pop_frame, text="Pop", font=("Arial", 12), bg="#FF6347", fg="white",
                                    command=self.pop_value)
        self.pop_button.pack(pady=5)

    def setup_sequence_frame(self):
        """Setup UI for Sequence operations."""
        self.sequence_label = tk.Label(self.sequence_frame, text="Enter Sequence (comma-separated, 'p' for pop):",
                                       font=("Arial", 12), bg="#33FFFF")
        self.sequence_label.pack(pady=10)

        self.sequence_input = tk.Entry(self.sequence_frame, font=("Arial", 12))
        self.sequence_input.pack(pady=5)

        self.limit_label = tk.Label(self.sequence_frame, text="Enter Stack Size:", font=("Arial", 12), bg="#33FFFF")
        self.limit_label.pack(pady=5)

        self.limit_input = tk.Entry(self.sequence_frame, font=("Arial", 12))
        self.limit_input.pack(pady=5)

        self.process_sequence_button = tk.Button(self.sequence_frame, text="Process Sequence", font=("Arial", 12),
                                                 bg="#4682B4", fg="white", command=self.process_sequence)
        self.process_sequence_button.place(x=950, y=100)

    def change_frame(self, selection):
        """Change the frame displayed based on the selected operation."""
        self.push_pop_frame.pack_forget()
        self.sequence_frame.pack_forget()

        self.stack_canvas.delete("all")

        if selection == "Push/Pop":
            self.push_pop_frame.pack(fill=tk.BOTH, expand=True)
            self.toggle_push_pop_elements(show=True)  # Show Push/Pop-specific elements
        elif selection == "Sequence":
            self.sequence_frame.pack(fill=tk.BOTH, expand=True)
            self.toggle_push_pop_elements(show=False)  # Hide Push/Pop-specific elements

    def push_value(self):
        """Push a value onto the push/pop stack."""
        value = self.push_input.get()
        if len(self.stack) >= self.stack_limit:  # Check if the stack is full
            messagebox.showwarning("Warning", "Stack is full, cannot push more elements.")
            return
        if value.isdigit():  # Check if the input is a valid number
            self.stack.append(int(value))
            self.update_stack_display(self.stack)  # Update with the main stack
        else:
            messagebox.showerror("Error", "Please enter a valid number.")
        self.push_input.delete(0, tk.END)

    def pop_value(self):
        """Pop a value from the push/pop stack."""
        if self.stack:
            self.stack.pop()
            self.update_stack_display(self.stack)  # Update with the main stack
        else:
            messagebox.showwarning("Warning", "Stack is empty, nothing to pop!")

    def display_stack(self):
        """Display the current stack."""
        if self.stack:
            stack_contents = ", ".join(map(str, self.stack))
            messagebox.showinfo("Stack Contents", f"Current Stack: {stack_contents}")
        else:
            messagebox.showinfo("Stack Contents", "Stack is empty")

    def process_sequence(self):
        """Process a sequence of operations and visualize each step with a separate stack."""
        self.stack_canvas.delete("all")  # Clear previous drawings
        seq = self.sequence_input.get().split(',')
        try:
            stack_limit = int(self.limit_input.get())
        except ValueError:
            wrongsize_label = tk.Label(text="Invalid Stack Size !!!", font=("Arial", 15 , "bold"), fg="red")
            wrongsize_label.place(x = 670 , y = 130)
            root.after(1000,wrongsize_label.destroy)
            return

        # Initialize the sequence stack
        self.sequence_stack = []
        self.sequence_top = -1  # Track the top for sequence operations

        def process_step(index):
            status_bg_color = "#e6f7ff"
            status_label = tk.Label(root, text="", font=("Arial", 15 , "bold"), fg="green")
            status_label.place(x = 690, y = 130)
            if index < len(seq):
                operation = seq[index].strip()  # Remove whitespace

                if operation.lower() == 'p':  # Pop operation
                    if self.sequence_stack:
                        self.sequence_stack.pop()
                        self.sequence_top -= 1
                        self.stack_canvas.delete("all")
                        pop_label = tk.Label(text="Popped an element", font=("Arial", 15 , "bold"),fg="green")
                        pop_label.place(x = 670, y = 130)
                        root.after(900,pop_label.destroy)
                    else:
                        # Display underflow message on the canvas
                        status_label.config(text="Stack Underflow", fg="red")
                        status_label.place(x=690, y=130)
                        root.after(900,status_label.destroy)

                elif self.sequence_top == stack_limit - 1:
                    # Display overflow message on the canvas
                    status_label.config(text=f"Stack Overflow Cannot Push :- {operation}", fg="red")
                    status_label.place(x=630, y=130)
                    root.after(900,status_label.destroy)
                else:
                    if operation.isdigit():  # Push operation
                        self.sequence_stack.append(int(operation))
                        self.sequence_top += 1
                        self.stack_canvas.delete("all")
                        push_label = tk.Label(text="Pushed :-  " + operation, font=("Arial", 15, "bold"), fg="green")
                        push_label.place(x=710, y=130)
                        root.after(900, push_label.destroy)

                    else:
                        self.stack_canvas.delete("all")
                        invalid_label = tk.Label(text=f"Invalid value '{operation}' ignored", font=("Arial", 15, "bold"), fg="red")
                        invalid_label.place(x=670, y=130)
                        root.after(900, invalid_label.destroy)


                # Update the canvas display with the sequence stack and show indexes
                self.update_stack_display(self.sequence_stack, highlight=self.sequence_top, is_sequence=True)
                self.root.after(1000, lambda: process_step(index + 1))  # Schedule the next step after 1 second

            else:
                complete_label = tk.Label(text="Sequence Completed", font=("Arial", 15, "bold"),fg="green")
                complete_label.place(x=670, y=130)
                root.after(5000, complete_label.destroy)

        # Start processing the sequence
        process_step(0)


    def update_stack_display(self, stack, highlight=None, is_sequence=False):
        """Update the visual display of the stack on the canvas, including indexes and top arrow."""
        self.stack_canvas.delete("all")  # Clear previous drawings
        y_pos = 490  # Adjust starting y position for drawing stack elements (from bottom-up)

        if not stack:
            pass
        else:
            for index, value in enumerate(stack):
                color = "yellow" if highlight == index else "white"
                # Draw stack element
                self.stack_canvas.create_rectangle(100, y_pos, 300, y_pos - 30, outline="black", fill=color)
                self.stack_canvas.create_text(200, y_pos - 15, text=str(value), font=("Arial", 12), fill="black")

                # Draw index next to the stack element
                self.stack_canvas.create_text(80, y_pos - 15, text=str(index), font=("Arial", 12), fill="blue")

                if index == len(stack) - 1:
                    # Draw arrow for the topmost element pointing left
                    arrow_y = y_pos - 15  # Center of the rectangle for the arrow
                    self.stack_canvas.create_line(330, arrow_y, 250, arrow_y, arrow=tk.LAST, fill="black", width=2)
                    self.stack_canvas.create_text(360, arrow_y, text="TOP", font=("Arial", 12), fill="black")

                y_pos -= 40  # Move up for the next stack element

        # Update the top label for the main stack (if not sequence)



# Create main window
if __name__ == "__main__":
    root = tk.Tk()
    app = StackApp(root)
    root.mainloop()