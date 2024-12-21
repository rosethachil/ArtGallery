from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from db import fetch_data,execute_query

def load_artworks(tab):
    # Button and frame styles
    style = ttk.Style(tab)
    style.configure("Buttonstyle.TButton", font=('Sitka Text Semibold', 10), background="#D58B73", foreground="#FFFFFF", borderwidth=1)
    style.map("Buttonstyle.TButton", foreground=[("active", "#FFFFFF")])
    style.map("Buttonstyle.TButton", background=[("!active", "#ad7a77"), ("active", "#a83d4c")])
    style.configure("EntryButton.TEntry", font=('Segoe UI Semibold', 12), fieldbackground="#cbb1a0", foreground="#5C4531", bordercolor="#735559", padding=[5, 2])

    # Container frame for dynamic content
    content_frame = tk.Frame(tab, bg="#f8e5dc", borderwidth=2)
    content_frame.grid(row=0, column=0, columnspan=1, sticky="nsew", padx=15, pady=15)

    tab.grid_rowconfigure(0, weight=1)  # Allow row 0 to expand
    tab.grid_columnconfigure(0, weight=1)  # Allow column 0 to expand

    # Create a canvas for scrollable content
    canvas = tk.Canvas(content_frame, bg="#fdf3ee", highlightthickness=0)
    canvas.grid(row=0, column=0, sticky="nsew")  # Stretch the canvas to fill the frame

    # Add a scrollbar for the canvas
    scrollbar = tk.Scrollbar(content_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")  # Place scrollbar on the right
    canvas.configure(yscrollcommand=scrollbar.set)

    # Ensure content_frame allows its child widgets to resize
    content_frame.grid_rowconfigure(0, weight=1)  # Make row 0 of content_frame stretch
    content_frame.grid_columnconfigure(0, weight=1)

    Totlist = tk.Frame(canvas, bg="#f8e5dc")
    canvas.create_window((0, 0), window=Totlist, anchor="nw")
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    add_details_frame=tk.Frame(tab,bg="#f8e5dc", borderwidth=2)
    add_details_frame.grid(row=0,column=3,columnspan=2,sticky="nsew",padx=15,pady=15)
    tab.grid_columnconfigure(3, weight=1)

    title=ttk.Label(add_details_frame,text="Enter Title of Art Work: ",font=('Sitka Text Semibold', 12),background="#f8e5dc")
    title.grid(row=0,column=0,padx=10,pady=10)
    enter_title = ttk.Entry(add_details_frame, style="EntryButton.TEntry")
    enter_title.grid(row=0,column=1,padx=10,pady=10)

    year=ttk.Label(add_details_frame,text="Enter Year: ",font=('Sitka Text Semibold', 12),background="#f8e5dc")
    year.grid(row=1,column=0,padx=10,pady=10)
    enter_year = ttk.Entry(add_details_frame, style="EntryButton.TEntry")
    enter_year.grid(row=1,column=1,padx=10,pady=10)

    artist_id=ttk.Label(add_details_frame,text="Enter Artist ID: ",font=('Sitka Text Semibold', 12),background="#f8e5dc")
    artist_id.grid(row=2,column=0,padx=10,pady=10)
    enter_id = ttk.Entry(add_details_frame, style="EntryButton.TEntry")
    enter_id.grid(row=2,column=1,padx=10,pady=10)
    artist_details=fetch_data("SELECT id, name FROM Artists")
    artist_names=[artist[1] for artist in artist_details]
    combobox = ttk.Combobox(add_details_frame, values=artist_names, width=20, font=('Segoe UI', 12))
    combobox.set("Select an artist")  # Default text
    combobox.grid(pady=10)

    def on_select(event):
    # Get the selected artist name from the combobox
        selected_name = combobox.get()
    
    # Find the corresponding artist ID for the selected name
        for artist in artist_details:
            if artist[1] == selected_name:  # artist[1] is the name
                artist_id = artist[0]  # artist[0] is the ID
                enter_id.delete(0, tk.END)  # Clear the entry box
                enter_id.insert(0, str(artist_id))  # Insert the ID into the entry box
                break

    combobox.bind("<<ComboboxSelected>>", on_select)

    pic=ttk.Label(add_details_frame,text="Select Picture ",font=('Sitka Text Semibold', 12),background="#f8e5dc")
    pic.grid(row=4,column=0,padx=10,pady=10)
    enter_pic = ttk.Entry(add_details_frame, style="EntryButton.TEntry")
    enter_pic.grid(row=4,column=1,padx=10,pady=10)

    def select_picture():
        file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])

        if file_path:
        # Display the selected file path in the entry box
            enter_pic.delete(0, tk.END)
            enter_pic.insert(0, file_path)

    select_pic=ttk.Button(add_details_frame,text="Select Picture",command=select_picture,style="Buttonstyle.TButton")
    select_pic.grid(row=4,column=2,padx=10,pady=10,sticky="nw")

    def add_artwork_detail():
        title=enter_title.get()
        year=enter_year.get()
        artist_id=enter_id.get()
        image_path=enter_pic.get()
        artwork_id=execute_query("INSERT INTO Artworks (title,artist_id,year) VALUES (%s, %s,%s) RETURNING id", (title,artist_id,year))
        execute_query("INSERT INTO images (artwork_id,image_path) VALUES (%s,%s)", (artwork_id,image_path))

    add_new_btn=ttk.Button(add_details_frame,text="Add new Artwork",command=add_artwork_detail,style="Buttonstyle.TButton")
    add_new_btn.grid(row=5,column=0,padx=10,pady=10,sticky="nsew")