import tkinter as tk
import socket
import sys

def quit_game():
    window.destroy()  # Use destroy() to properly close the window

def start_game():
    # Clear existing widgets
    for widget in window.winfo_children():
        widget.destroy()
    
    # Create and display new widgets for the game view
    game_label = tk.Label(window, text="Game Started!", font=("Helvetica", 24))
    game_label.grid(row=0, column=0, columnspan=2, pady=20) #span across both columns

    # Add game-specific widgets here (e.g., buttons, input fields)
    port_number_label = tk.Label(window, text="PORT Number:")
    ip_addr_label = tk.Label(window, text="IP address of server:")
    port_number_label.grid(row=1, column=0, sticky="w", padx = 5, pady = 5)
    ip_addr_label.grid(row=2, column=0, sticky="w", padx = 5, pady = 5)

    global host, port, HEADER, FORMAT, SERVER, conn
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    port_number_entry = tk.Entry(window)
    ip_address_server_entry = tk.Entry(window)

    port_number_entry.insert(0, str(port)) # Insert the port number into the entry
    ip_address_server_entry.insert(0, socket.gethostbyname(socket.gethostname())) #insert the ip into the entry

    port_number_entry.grid(row=1, column=1, padx = 5, pady = 5)
    ip_address_server_entry.grid(row=2, column=1, padx = 5, pady = 5)

    back_button = tk.Button(window, text = "Back to Main Menu", command = main_menu)
    back_button.grid(row = 3, column = 0, columnspan = 2, pady = 10) #back button on the bottom

def main_menu():
    # Clear existing widgets
    for widget in window.winfo_children():
        widget.destroy()

    # Create and display main menu widgets
    main_label = tk.Label(window, text="Rock Paper Scissors", font=("Helvetica", 46))
    start_game_btn = tk.Button(window, text="Start", font=("Helvetica", 20), command=start_game)
    quit_btn = tk.Button(window, text="Quit", font=("Helvetica", 20), command=quit_game)

    main_label.pack()
    start_game_btn.pack()
    quit_btn.pack()

window = tk.Tk()
window.title("Rock Paper Scissors - Socket edition")

# Initialize the main menu
main_menu()

tk.mainloop()