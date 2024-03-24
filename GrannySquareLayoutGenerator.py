import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
import math
import random

def generate_pattern():
    try:
        grid_width = int(grid_width_var.get())
        grid_height = int(grid_height_var.get())
        max_neighbors = int(max_neighbors_var.get())
        
        if grid_width <= 0 or grid_height <= 0:
            raise ValueError("Grid dimensions must be positive integers.")
        if max_neighbors < 0:
            raise ValueError("Max similar color neighbors cannot be negative.")

        total_squares = grid_width * grid_height
        pattern = []

        # Collect squares with their colors
        squares = []
        for color, quantity_var in color_quantities.items():
            quantity = quantity_var.get()
            if not quantity.isdigit() or int(quantity) < 0:
                raise ValueError("Please enter a valid non-negative number for all quantities.")
            squares.extend([color_vars[color].get()] * int(quantity))

        if len(squares) < total_squares:
            messagebox.showinfo("Info", "Not enough squares for the full grid. Filling as much as possible.")
            total_squares = len(squares)

        # Generate the pattern with the constraint
        pattern = create_constrained_pattern(squares, grid_width, grid_height, max_neighbors, is_random.get())
        # Update the canvas size and clear previous squares
        canvas.config(width=square_size*grid_width, height=square_size*grid_height)
        canvas.delete("square")

        # Draw the new pattern
        for i, color in enumerate(pattern):
            row, col = divmod(i, grid_width)
            canvas.create_rectangle(
                col*square_size, row*square_size,
                (col+1)*square_size, (row+1)*square_size,
                outline="black", fill=color, tags="square"
            )
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def create_constrained_pattern(squares, width, height, max_neighbors, is_random):
    # Count the occurrences of each color
    color_counts = {color: squares.count(color) for color in set(squares)}
    # Identify the most common color
    most_common_color = max(color_counts, key=color_counts.get)
    
    # Remove the most common color from the list and sort the remaining colors by their counts (descending)
    secondary_colors = [(color, count) for color, count in color_counts.items() if color != most_common_color]
    secondary_colors.sort(key=lambda x: -x[1])
    
    # Initialize the pattern list
    pattern = []
    
    # Track the current index for secondary colors
    sec_index = 0
    # Calculate the total number of squares
    total_squares = width * height
    
    for i in range(total_squares):
        # Place the most common color in every other spot
        if i % 2 == 0:
            pattern.append(most_common_color)
        else:
            # Alternate through the secondary colors
            if secondary_colors:
                current_color, current_count = secondary_colors[sec_index]
                pattern.append(current_color)
                current_count -= 1
                # Update the count or move to the next color if this one is exhausted
                if current_count > 0:
                    secondary_colors[sec_index] = (current_color, current_count)
                else:
                    secondary_colors.pop(sec_index)
                    # Adjust sec_index if we removed an element
                    sec_index = sec_index % len(secondary_colors) if secondary_colors else 0
            else:
                # If we run out of secondary colors, fill with the most common color
                pattern.append(most_common_color)

            # Move to the next secondary color for the next iteration
            sec_index = (sec_index + 1) % len(secondary_colors) if secondary_colors else 0

    return pattern






    # The rest of the function remains unchanged, return the portion of squares based on the grid size
    return squares[:width*height]

def choose_color(button, color_var):
    color, hex_color = colorchooser.askcolor()
    if color:
        color_var.set(hex_color)  # Store the hexadecimal color string
        button.config(bg=hex_color)  # Update the button's background color to the chosen color

# Basic settings
colors = ["Color 1", "Color 2", "Color 3"]
color_quantities = {}
color_vars = {}  # Stores color strings
square_size = 30  # Size of each square in pixels

# Set up the GUI
root = tk.Tk()
root.title("Granny Square Pattern Generator")

frame = ttk.Frame(root)
frame.pack(padx=10, pady=10)

# Grid dimensions inputs
ttk.Label(frame, text="Grid Width:").grid(row=0, column=0)
grid_width_var = tk.StringVar(value="10")  # Default value
ttk.Entry(frame, textvariable=grid_width_var).grid(row=0, column=1)

ttk.Label(frame, text="Grid Height:").grid(row=1, column=0)
grid_height_var = tk.StringVar(value="10")  # Default value
ttk.Entry(frame, textvariable=grid_height_var).grid(row=1, column=1)

# Max similar color neighbors input
ttk.Label(frame, text="Max Similar Color Neighbors:").grid(row=2, column=0)
max_neighbors_var = tk.StringVar(value="2")  # Default value
ttk.Entry(frame, textvariable=max_neighbors_var).grid(row=2, column=1)

# Add a variable to store the pattern type choice (True for random, False for repeating)
is_random = tk.BooleanVar(value=True)  # Default to True for random pattern

# Add a checkbox for the user to choose the pattern type
pattern_type_checkbutton = ttk.Checkbutton(frame, text="Random Pattern", variable=is_random, onvalue=True, offvalue=False)
pattern_type_checkbutton.grid(row=5, column=0, columnspan=2, sticky="w")

# Adjust the row indices for the subsequent controls to account for the new checkbox
# Note: You might need to adjust the starting index for the loop below if other elements have been added above


# Color inputs
for i, color_name in enumerate(colors, start=3):
    ttk.Label(frame, text=f"{color_name} Squares:").grid(row=i*2, column=0)
    quantity = tk.StringVar()
    ttk.Entry(frame, textvariable=quantity).grid(row=i*2, column=1)
    color_quantities[color_name] = quantity

    color_var = tk.StringVar()
    color_button = tk.Button(frame, text="Choose Color")  # Changed to tk.Button
    color_button.grid(row=i*2+1, column=0, columnspan=2)
    color_button.config(command=lambda button=color_button, var=color_var: choose_color(button, var))
    color_vars[color_name] = color_var

# Generate Pattern button
ttk.Button(frame, text="Generate Pattern", command=generate_pattern).grid(row=(len(colors)*2)+8, columnspan=2, pady=10)

canvas = tk.Canvas(root)
canvas.pack()

root.mainloop()
