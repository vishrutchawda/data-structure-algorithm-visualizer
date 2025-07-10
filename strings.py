import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
import os


# Set base directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the relative path to the images folder
images_dir = os.path.join(base_dir, "../other imp files")


def string_operations_gui():
    def update_output(text):
        output_label.config(text=text)

    def draw_string_visualization():
        # Clear the previous canvas
        canvas.delete("all")

        if user_string:
            # Draw the string as an array of characters with indices
            x_start = 50  # starting x position
            y_start = 50  # starting y position
            box_width = 40  # width of each box
            box_height = 40  # height of each box
            padding = 10  # space between boxes

            for i, char in enumerate(user_string):
                # Draw the box for each character
                x0 = x_start + i * (box_width + padding)
                y0 = y_start
                x1 = x0 + box_width
                y1 = y0 + box_height

                # Draw rectangle
                canvas.create_rectangle(x0, y0, x1, y1, fill="#ffffcc", outline="black", width=2)
                # Place character inside the box
                canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=char, font=("Arial", 16))

                canvas.create_text((x0 + x1) // 2, y1 + 15, text=str(i), font=("Arial", 15))

    def load_images():
        try:
            # Resize images to a more suitable size
            len_image_path = os.path.join(images_dir, "images", "string_length.png")
            con_image_path = os.path.join(images_dir, "images", "string_concadinate.png")
            com_image_path = os.path.join(images_dir, "images", "string_compare.png")
            sub_image_path = os.path.join(images_dir, "images", "sub_string.png")
            rev_image_path = os.path.join(images_dir, "images", "reverse_string.png")
            low_image_path = os.path.join(images_dir, "images", "string_lower.png")
            upr_image_path = os.path.join(images_dir, "images", "string_upper.png")


            sl = ImageTk.PhotoImage(Image.open(len_image_path).resize((550, 500), Image.Resampling.LANCZOS))
            sc = ImageTk.PhotoImage(Image.open(con_image_path).resize((550, 550), Image.Resampling.LANCZOS))
            scm = ImageTk.PhotoImage(Image.open(com_image_path).resize((550, 550), Image.Resampling.LANCZOS))
            ss = ImageTk.PhotoImage(Image.open(sub_image_path).resize((550, 550), Image.Resampling.LANCZOS))
            rs = ImageTk.PhotoImage(Image.open(rev_image_path).resize((550, 550), Image.Resampling.LANCZOS))
            slo = ImageTk.PhotoImage(Image.open(low_image_path).resize((550, 550), Image.Resampling.LANCZOS))
            su = ImageTk.PhotoImage(Image.open(upr_image_path).resize((550, 550), Image.Resampling.LANCZOS))
            return {
                "String Length": sl,
                "Concatenate": sc,
                "Compare": scm,
                "Substring": ss,
                "Reverse": rs,
                "To Lowercase": slo,
                "To Uppercase": su
            }
        except Exception as e:
            print(f"Error loading images: {e}")
            return {}

    def perform_operation():
        operation = selected_operation.get()

        # Update the image label dynamically instead of creating new labels each time
        current_image = images.get(operation, None)


        if operation == "Insert String":
            insert_string()
        elif operation == "String Length":
            image_label.config(image=current_image)
            image_label.place(x=950, y=200)
            length_of_string()
        elif operation == "Concatenate":
            image_label.config(image=current_image)
            image_label.place(x=950, y=150)
            concatenate_strings()
        elif operation == "Compare":
            image_label.config(image=current_image)
            image_label.place(x=950, y=150)
            compare_strings()
        elif operation == "Substring":
            image_label.config(image=current_image)
            image_label.place(x=950, y=150)
            substring_of_string()
        elif operation == "Reverse":
            image_label.config(image=current_image)
            image_label.place(x=950, y=150)
            reverse_string()
        elif operation == "To Lowercase":
            image_label.config(image=current_image)
            image_label.place(x=950, y=150)
            string_to_lowercase()
        elif operation == "To Uppercase":
            image_label.config(image=current_image)
            image_label.place(x=950, y=150)
            string_to_uppercase()

    def insert_string():
        global user_string
        user_string = simpledialog.askstring("Input", "Enter a string:")
        if user_string:
            update_output(f"String inserted: {user_string}")
            draw_string_visualization()
        else:
            update_output("No string entered.")

    def length_of_string():
        if user_string:
            update_output("Calculating length...")
            length = 0

            def highlight_next_char(index):
                nonlocal length
                if index < len(user_string):
                    x_start = 50 + index * (40 + 10)
                    y_start = 50
                    x1 = x_start + 40
                    y1 = y_start + 40

                    # Highlight character by changing its color
                    canvas.create_rectangle(x_start, y_start, x1, y1, fill="lightblue", outline="black", width=2)
                    canvas.create_text((x_start + x1) // 2, (y_start + y1) // 2, text=user_string[index],
                                       font=("Arial", 16))

                    length += 1
                    output_label.config(text=f"Counting... {length}")
                    window.after(500, highlight_next_char, index + 1)  # Delay of 500ms before highlighting next character
                else:
                    output_label.config(text=f"Length of the string: {length}")

            highlight_next_char(0)
        else:
            update_output("No string entered yet.")

    def concatenate_strings():
        global user_string
        if user_string:
            second_string = simpledialog.askstring("Input", "Enter another string to concatenate:")
            if second_string:
                user_string += second_string
                update_output(f"Concatenated string: {user_string}")
                draw_string_visualization()
        else:
            update_output("No string entered yet.")

    def compare_strings():
        if user_string:
            compare_string = simpledialog.askstring("Input", "Enter a string to compare:")
            if user_string == compare_string:
                update_output("Strings are equal.")
            else:
                update_output("Strings are not equal.")
        else:
            update_output("No string entered yet.")

    def substring_of_string():
        if user_string:
            try:
                start = int(simpledialog.askstring("Input", "Enter start index for the substring:"))
                end = int(simpledialog.askstring("Input", "Enter end index for the substring:"))
                if 0 <= start < end <= len(user_string):
                    substring = user_string[start:end]
                    update_output(f"Substring: {substring}")
                else:
                    update_output("Invalid indices. Start should be less than end.")
            except ValueError:
                update_output("Invalid input.")
        else:
            update_output("No string entered yet.")

    def reverse_string():
        global user_string
        if user_string:
            user_string = user_string[::-1]
            update_output(f"Reversed string: {user_string}")
            draw_string_visualization()
        else:
            update_output("No string entered yet.")

    def string_to_lowercase():
        global user_string
        if user_string:
            user_string = user_string.lower()
            update_output(f"String in lowercase: {user_string}")
            draw_string_visualization()
        else:
            update_output("No string entered yet.")

    def string_to_uppercase():
        global user_string
        if user_string:
            user_string = user_string.upper()
            update_output(f"String in uppercase: {user_string}")
            draw_string_visualization()
        else:
            update_output("No string entered yet.")

    # Initialize main window
    window = tk.Tk()
    window.title("String Operations GUI")
    window.geometry("1540x810")  # Adjust the window size to accommodate the image
    window.configure(bg="#33FFFF")

    # Global string to be manipulated
    global user_string
    user_string = ""

    # Title Label
    title_label = tk.Label(window, text="String Operations", font=("Helvetica", 18, "bold"), bg="#b3daff", pady=10)
    title_label.pack()

    status_label = tk.Label(window, text="Algorithm :- ", font=("Arial", 20), fg="black", bg="#33FFFF")
    status_label.place(x=980, y=60)


    # Drop-down Menu for operations
    operations = [
        "Insert String",
        "String Length",
        "Concatenate",
        "Compare",
        "Substring",
        "Reverse",
        "To Lowercase",
        "To Uppercase"
    ]

    selected_operation = tk.StringVar(window)
    selected_operation.set(operations[0])  # Default option

    operation_menu = tk.OptionMenu(window, selected_operation, *operations)
    operation_menu.config(width=20, font=("Arial", 12), bg="#80bfff", relief="raised")
    operation_menu.pack(pady=20)

    # Button to perform the selected operation
    perform_button = tk.Button(window, text="Perform Operation", command=perform_operation, bg="#80bfff",
                               font=("Arial", 12, "bold"), relief="raised")
    perform_button.pack(pady=10)

    # Bind the Enter key to perform the operation
    window.bind('<Return>', lambda event: perform_operation())

    # Output Label
    output_label = tk.Label(window, text="", font=("Helvetica", 17 , "bold"), bg="#33FFFF", pady=10)
    output_label.pack(pady=20)

    # Canvas for string visualization (as a character array)
    canvas = tk.Canvas(window, width=900, height=200, bg="white")
    canvas.place(x=10,y=350)


    # Image Label for displaying images
    image_label = tk.Label(window, bg="#33FFFF")
    image_label.pack(side="right", padx=20, pady=20)

    # Load images after initializing the window
    images = load_images()

    # Exit Button
    exit_button = tk.Button(window, text="Exit", command=window.destroy, width=10, bg="#ff6666",
                            font=("Arial", 12, "bold"), relief="raised")
    exit_button.pack(side="bottom", pady=20)

    # Start the Tkinter event loop
    window.mainloop()


string_operations_gui()