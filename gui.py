import customtkinter as ctk
from tkinter import *
import subprocess
import threading  # Import threading for asynchronous progress updates
import time
from CTkMessagebox import CTkMessagebox
from PIL import Image

from PIL import Image, ImageTk


# Create the GUI
app = ctk.CTk()
app.geometry("420x460")
app.minsize(400, 430)  
app.title("Twitter Scraper by Onat")


icon_path = "img/app_png.ico"
icon = Image.open(icon_path)
icon_photo = ImageTk.PhotoImage(icon)
app.tk.call('wm', 'iconphoto', app._w, icon_photo)


ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

def is_integer(text):
    """Validates if the entered text is an integer."""
    try:
        int(text)
        return True
    except ValueError:
        return False

def checkbox_toggle(checked_box):
    """Toggles checkboxes to ensure only one is selected."""
    for box in [checkbox_top, checkbox_regular, checkbox_latest]:
        if box != checked_box:
            box.deselect()

def start_scraping():
    """Gathers input from the interface and initiates scraping (placeholder)."""
    # Placeholder to implement your actual scraping logic based on inputs
    username = textbox_username.get()
    password = textbox_password.get()
    t_count = textbox_t_count.get()
    hashtags = textbox_hashtags.get()
    # hashtags = textbox_hashtags.get().split(",")
    top = checkbox_top.get()
    regular = checkbox_regular.get()
    latest = checkbox_latest.get()

    # Check if a checkbox is selected
    # if not any([top, regular, latest]):
    #     # Display a warning message or prompt the user to select a checkbox
    #     print("Please select a tweet type.")
    #     return
    

    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Tweet Count: {t_count}")
    print(f"Hashtags: {hashtags}")
    print(f"Top Tweets: {top}")
    print(f"Regular Tweets: {regular}")
    print(f"Latest Tweets: {latest}")
    command_string = f"python scraper --user=@{username} --password={password} -t={t_count} -ht={hashtags} "
    if top == 1:
        command_string += "--top" 
    elif latest == 1:
        command_string += "--latest"         
        
    

    # Run scraping in a separate thread to avoid blocking the GUI
    scraping_thread = threading.Thread(target=start_command, args=(command_string,))
    scraping_thread.start()

    
    
    # Replace this with your scraping logic using the retrieved data
    # ...


def start_command(command ):
    try:
        # Create the progress bar
        progress_bar = ctk.CTkProgressBar(master=app)
        progress_bar.pack(pady=10)  

        progress_bar.start()  # Start the progress bar animation

        # Run the scraping process
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()  # Wait for process to finish

        # Handle errors
        if error:
            print("Error occurred during scraping:", error.decode())
            # Display an error message to the user or handle it appropriately
        else:
            print("Scraping finished successfully:", output.decode())
            # Show a success message or take further actions based on output

        # Update progress bar (replace with your actual progress tracking)
        for i in range(100):
            time.sleep(0.1)
            app.after(0, lambda: progress_bar.set(i + 1))  # Schedule update on main thread

    except Exception as e:
        print(f"::HATA=={e}::")
        app.after(0, progress_bar.stop)  # Schedule stop on main thread

    finally:
        progress_bar.stop()  # Stop the progress bar animation
        progress_bar.destroy()  # Destroy the progress bar widget
        CTkMessagebox(title="Info", message="Scraping is complate!")
        # app.after(0, lambda: tkinter.messagebox.showinfo("Scraping Complete", "Scraping has finished successfully!"))
        


    




# User name and password
label_username = ctk.CTkLabel(app, text="Username:")
label_username.pack(pady=10)
textbox_username = ctk.CTkEntry(app)
textbox_username.pack(pady=5)

label_password = ctk.CTkLabel(app, text="Password:")
label_password.pack(pady=10)
textbox_password = ctk.CTkEntry(app, show="*")  # Hide password
textbox_password.pack(pady=5)

# Tweet count (validated to be an integer)
label_t_count = ctk.CTkLabel(app, text="Tweet Count:")
label_t_count.pack(pady=10)
textbox_t_count = ctk.CTkEntry(app, validate="key")
textbox_t_count.pack(pady=5)

# Hashtags
label_hashtags = ctk.CTkLabel(app, text="Hashtags (comma-separated):")
label_hashtags.pack(pady=10)
textbox_hashtags = ctk.CTkEntry(app)
textbox_hashtags.pack(pady=5)

# Options (corrected labels and removed padding)
frame_options = ctk.CTkFrame(app)
frame_options.pack()

# Checkboxes with toggle function
checkbox_top = ctk.CTkCheckBox(frame_options, text="Top Tweets", command=lambda: checkbox_toggle(checkbox_top))
checkbox_top.pack(side="left", pady=10)

checkbox_regular = ctk.CTkCheckBox(frame_options, text="Regular Tweets", command=lambda: checkbox_toggle(checkbox_regular))
checkbox_regular.pack(side="left",pady=10)
checkbox_regular.select()  # Initially select Regular Tweets

checkbox_latest = ctk.CTkCheckBox(frame_options, text="Latest Tweets", command=lambda: checkbox_toggle(checkbox_latest))
checkbox_latest.pack(side="left",pady=10)

# Start button
button = ctk.CTkButton(app, text="Start Scraping", command=start_scraping)
button.pack(pady=16)

# Run the app
app.mainloop()


