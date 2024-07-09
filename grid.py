import tkinter as tk
import time

# Initialize main application window
root = tk.Tk()
root.title("Binary Button Grid")
play = False

# Define grid size
rows, cols = 100, 100

# Set maximum window size
max_width = 800
max_height = 600
root.maxsize(max_width, max_height)

# Initialize a 2D list to track button states (0 for off, 1 for on)
button_states = [[0 for _ in range(cols)] for _ in range(rows)]

# Function to check neighbors and print if they have the same state
def transfer_button_states():
    next_gen = [[0 for _ in range(cols)] for _ in range(rows)]

    for r in range(rows):
        for c in range(cols):
            current_state = button_states[r][c]
            neighbors = [
                button_states[r + dr][c + dc]
                for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
                if 0 <= r + dr < rows and 0 <= c + dc < cols
            ]

            if current_state == 1:
                if neighbors.count(1) in [2, 3]:
                    next_gen[r][c] = 1
                else:
                    next_gen[r][c] = 0
            else:
                if neighbors.count(1) == 3:
                    next_gen[r][c] = 1

    redraw_grid(next_gen)

def play_button():
    global play
    play = not play
    play_button_widget.config(text="Stop" if play else "Play")
    if play:
        play_loop()

def play_loop():
    if play:
        transfer_button_states()
        root.after(500, play_loop)  # Schedule the next update in 500 ms (0.5 seconds)

def redraw_grid(new_grid):
    for r in range(rows):
        for c in range(cols):
            button_states[r][c] = new_grid[r][c]
            background = '#FF0000' if new_grid[r][c] == 1 else '#FFFFFF'
            foreground = '#FF0000' if new_grid[r][c] == 1 else '#FFFFFF'
            button_grid[r][c].config(bg=background, fg=foreground)

# Function to create a toggle function for a specific button
def create_toggle_function(row, col):
    def toggle_button():
        current_state = button_states[row][col]
        new_state = 1 - current_state
        button_states[row][col] = new_state
        background = '#FF0000' if new_state == 1 else '#FFFFFF'
        foreground = '#FF0000' if new_state == 1 else '#FFFFFF'
        button_grid[row][col].config(text=str(new_state), bg=background, fg=foreground)
        button_grid[row][col].update_idletasks()
    return toggle_button

# Create a scrollable canvas
canvas = tk.Canvas(root)
canvas.grid(row=0, column=0, sticky='nsew')

# Add scrollbars to the canvas
h_scrollbar = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=canvas.xview)
h_scrollbar.grid(row=1, column=0, sticky='ew')
v_scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
v_scrollbar.grid(row=0, column=1, sticky='ns')

canvas.config(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)

# Create a frame inside the canvas
frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor='nw')

# Create a 2D list to store button widgets
button_grid = [[None for _ in range(cols)] for _ in range(rows)]

# Create buttons and place them in the frame
for r in range(rows):
    for c in range(cols):
        button_grid[r][c] = tk.Checkbutton(
            frame, text="0", width=2, height=1, indicatoron=0, bg='white', activebackground='white',
            selectcolor='white', fg='white', command=create_toggle_function(r, c)
        )
        button_grid[r][c].grid(row=r, column=c, padx=0, pady=0)

# Update the canvas scroll region
frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Create the "Next" button outside the scrollable area
button = tk.Button(
    root, text="Next", command=transfer_button_states, activebackground="blue", activeforeground="white",
    anchor="center", bd=3, bg="lightgray", cursor="hand2", disabledforeground="gray", fg="black",
    font=("Arial", 12), height=2, highlightbackground="black", highlightcolor="green", highlightthickness=2,
    justify="center", overrelief="raised", padx=10, pady=5, width=15, wraplength=100
)
button.grid(row=2, column=0, columnspan=2, pady=10)

# Create the "Play" button outside the scrollable area
play_button_widget = tk.Button(
    root, text="Play", command=play_button, activebackground="blue", activeforeground="white", anchor="center",
    bd=3, bg="lightgray", cursor="hand2", disabledforeground="gray", fg="black", font=("Arial", 12), height=2,
    highlightbackground="black", highlightcolor="green", highlightthickness=2, justify="center", overrelief="raised",
    padx=10, pady=5, width=15, wraplength=100
)
play_button_widget.grid(row=5, column=0, columnspan=2, pady=10)

# Configure grid to expand properly
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Run the application
root.mainloop()
