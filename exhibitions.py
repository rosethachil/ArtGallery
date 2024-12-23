from tkinter import ttk
import tkinter as tk
from tkcalendar import DateEntry
from tkinter import messagebox
from db import fetch_data,execute_query

def load_exhibitions_profile(tab):
    style = ttk.Style(tab)
    style.configure("Buttonstyle.TButton", font=('Sitka Text Semibold', 10), background="#D58B73", foreground="#FFFFFF", borderwidth=1)
    style.map("Buttonstyle.TButton", foreground=[("active", "#FFFFFF")])
    style.map("Buttonstyle.TButton", background=[("!active", "#ad7a77"), ("active", "#a83d4c")])
    style.configure("EntryButton.TEntry", font=('Segoe UI Semibold', 12), fieldbackground="#cbb1a0", foreground="#5C4531", bordercolor="#735559", padding=[5, 2])

    content_frame = tk.Frame(tab, bg="#f8e5dc", borderwidth=2)
    content_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
    add_details_frame=tk.Frame(tab,bg="#f8e5dc", borderwidth=2)
    add_details_frame.grid(row=0,column=1,sticky="nsew",padx=15,pady=15)

    canvas = tk.Canvas(content_frame, bg="#fdf3ee", highlightthickness=0)
    canvas.grid(row=0, column=0, sticky="nsew")
    container_frame = tk.Frame(canvas, bg="#fdf3ee")
    canvas.create_window((0, 0), window=container_frame, anchor="n")
    container_frame.grid_rowconfigure(0, weight=1)
    container_frame.grid_columnconfigure(0, weight=1)

    Totlist = tk.Frame(container_frame, bg="#fdf3ee")
    Totlist.grid(row=0, column=0, padx=20, pady=20)
    scrollbar = tk.Scrollbar(content_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    title=ttk.Label(add_details_frame,text="Add New Exhibition details: ",font=('Sitka Text Semibold', 12),background="#f8e5dc")
    title.grid(row=0,column=0,padx=10,pady=10)

    name=ttk.Label(add_details_frame,text="Enter Name of exhibition: ",font=('Sitka Text Semibold', 12),background="#f8e5dc")
    name.grid(row=1,column=0,padx=10,pady=10)
    enter_name = ttk.Entry(add_details_frame, style="EntryButton.TEntry")
    enter_name.grid(row=1,column=1,padx=10,pady=10)

    start_date=ttk.Label(add_details_frame, text="Start Date:", font=("Sitka Text", 12), background="#f8e5dc")
    start_date.grid(row=2, column=0, padx=10, pady=10, sticky="n")
    start_date_entry = DateEntry(add_details_frame, font=("Sitka Text", 12), date_pattern="dd-mm-yyyy")
    start_date_entry.grid(row=2, column=1, padx=10, pady=10, sticky="n")

    end_date=ttk.Label(add_details_frame, text="End Date:", font=("Sitka Text", 12), background="#f8e5dc")
    end_date.grid(row=3, column=0, padx=10, pady=10, sticky="n")
    end_date_entry = DateEntry(add_details_frame, font=("Sitka Text", 12), date_pattern="dd-mm-yyyy")
    end_date_entry.grid(row=3, column=1, padx=10, pady=10, sticky="n")

    location=ttk.Label(add_details_frame, text="Location:", font=("Sitka Text", 12), background="#f8e5dc")
    location.grid(row=4, column=0, padx=10, pady=10, sticky="n")
    location_entry = ttk.Entry(add_details_frame, font=("Sitka Text", 12))
    location_entry.grid(row=4, column=1, padx=10, pady=10, sticky="n")

    title=ttk.Label(add_details_frame,text="Add Artwork to Exhibition: ",font=('Sitka Text Semibold', 12),background="#f8e5dc")
    title.grid(row=6,column=0,padx=10,pady=10)

    exhibition_id=tk.Label(add_details_frame, text="Exhibition:", font=("Sitka Text", 12), bg="#fdf3ee")
    exhibition_id.grid(row=7, column=0, padx=10, pady=5, sticky="e")
    enter_exhi_id = ttk.Entry(add_details_frame, style="EntryButton.TEntry")
    enter_exhi_id.grid(row=7,column=1,padx=10,pady=10)

    exhibition_details = fetch_data("SELECT exhibition_id, title FROM Artists")
    for details in exhibition_details:
        popup_details=f"{details[0]} - {details[1]}"
    exhibition_box = ttk.Combobox(add_details_frame, values=popup_details, width=20, font=('Segoe UI', 12))
    exhibition_box.set("Select an exhibition")  # Default text
    exhibition_box.grid(row=8,column=1,pady=10)

    artwork_id=tk.Label(add_details_frame, text="ArtWork:", font=("Sitka Text", 12), bg="#fdf3ee")
    artwork_id.grid(row=9, column=0, padx=10, pady=5, sticky="e")
    enter_artwork_id = ttk.Entry(add_details_frame, style="EntryButton.TEntry")
    enter_artwork_id.grid(row=9,column=1,padx=10,pady=10)

    artwork_details = fetch_data("SELECT id, title FROM Artists")
    for details in artwork_details:
        popup_details=f"{details[0]} - {details[1]}"
    artwork_box = ttk.Combobox(add_details_frame, values=popup_details, width=20, font=('Segoe UI', 12))
    artwork_box.set("Select an exhibition")  # Default text
    artwork_box.grid(row=10,column=1,pady=10)

    def on_select_exhibition():
        selected_name = exhibition_box.get()
        for exhibition in exhibition_details:
            if selected_name == f"{exhibition[0]} - {exhibition[1]}":
                enter_exhi_id.delete(0, tk.END)
                enter_exhi_id.insert(0, exhibition[0])
                break

    def on_select_artwork():
        selected_name = artwork_box.get()
        for artwork in artwork_details:
            if selected_name == f"{artwork[0]} - {artwork[1]}":
                enter_artwork_id.delete(0, tk.END)
                enter_artwork_id.insert(0, artwork[0])
                break
    
    exhibition_box.bind("<<ComboboxSelected>>", lambda e: on_select_exhibition())
    artwork_box.bind("<<ComboboxSelected>>", lambda e: on_select_artwork())

    def add_exhibition_detail():
        name = enter_name.get()
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()
        location = location_entry.get()
        if name and start_date and end_date and location:
            execute_query("INSERT INTO Exhibitions (name, start_date, end_date, location) VALUES (%s, %s, %s, %s)", (name, start_date, end_date, location))
            refresh_list()
        else:
            messagebox.showerror("Error", "All fields are required")
        enter_name.delete(0, tk.END)
        start_date_entry.delete(0, tk.END)
        end_date_entry.delete(0, tk.END)
        location_entry.delete(0, tk.END)

    def refresh_list():
        for widget in Totlist.winfo_children():
            widget.destroy()
        exhibitions = fetch_data("SELECT * FROM Exhibitions")

    def add_artwork_exhibition():
        exhibition_id = enter_exhi_id.get()
        artwork_id = enter_artwork_id.get()
        if exhibition_id and artwork_id:
            execute_query("INSERT INTO artwork_exhibitions (exhibition_id, artwork_id) VALUES (%s, %s)", (exhibition_id, artwork_id))
            refresh_list()
        else:
            messagebox.showerror("Error", "All fields are required")
        enter_exhi_id.delete(0, tk.END)
        enter_artwork_id.delete(0, tk.END)

    add_new_btn=ttk.Button(add_details_frame,text="Add new Artwork",command=add_exhibition_detail,style="Buttonstyle.TButton")
    add_new_btn.grid(row=5,column=0,padx=10,pady=10,sticky="nsew")
    add_exhi_detail=ttk.Button(add_details_frame,text="Add Exhibition Detail",command=add_artwork_exhibition,style="Buttonstyle.TButton")
    add_exhi_detail.grid(row=11,column=0,padx=10,pady=10,sticky="nsew")