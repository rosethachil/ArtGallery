from tkinter import ttk
import tkinter as tk
from tkcalendar import DateEntry
from tkinter import messagebox
from datetime import datetime
from db import fetch_data,execute_query

def load_exhibitions_profile(tab):
    style = ttk.Style(tab)
    style.configure("Buttonstyle.TButton", font=('Sitka Text Semibold', 10), background="#D58B73", foreground="#FFFFFF", borderwidth=1)
    style.map("Buttonstyle.TButton", foreground=[("active", "#FFFFFF")])
    style.map("Buttonstyle.TButton", background=[("!active", "#ad7a77"), ("active", "#a83d4c")])
    style.configure("EntryButton.TEntry", font=('Segoe UI Semibold', 12), fieldbackground="#cbb1a0", foreground="#5C4531", bordercolor="#735559", padding=[5, 2])

    tab.grid_columnconfigure(0, weight=1)  # Content frame (artwork details)
    tab.grid_columnconfigure(1, weight=0)  # The second column (add_details_frame) remains fixed width
    tab.grid_columnconfigure(2, weight=0)

    content_frame = tk.Frame(tab, bg="#f8e5dc", borderwidth=2)
    content_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

    exhibition_label = ttk.Label(content_frame, text="Select an Exhibition:", font=('Sitka Text Semibold', 12), background="#fdf3ee")
    exhibition_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    exhibition_details = fetch_data("SELECT exhibition_id, title FROM exhibitions")
    exhibition_names = [f"{details[0]} - {details[1]}" for details in exhibition_details]

    exhibition_dropdown = ttk.Combobox(content_frame, values=exhibition_names, font=('Segoe UI', 12), width=20)
    exhibition_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="w")
    exhibition_dropdown.set("Select an exhibition")
    
    add_details_frame=tk.Frame(tab,bg="#f8e5dc", borderwidth=2)
    add_details_frame.grid(row=0,column=1,sticky="nsew",padx=15,pady=15)
    add_details_frame.grid_rowconfigure(0, weight=0)
    add_details_frame.grid_columnconfigure(0, weight=1)

    Totlist = tk.Frame(content_frame, bg="#fdf3ee")
    Totlist.grid(row=1, column=0, columnspan=2, sticky="nsew")
    canvas = tk.Canvas(Totlist, bg="#fdf3ee", highlightthickness=0)
    canvas.grid(row=0, column=0, sticky="nsew")
    container_frame = tk.Frame(canvas, bg="#fdf3ee")
    canvas.create_window((0, 0), window=container_frame, anchor="nw")
    
    container_frame.grid_rowconfigure(0, weight=1)
    container_frame.grid_columnconfigure(0, weight=1)
    Totlist.grid_rowconfigure(0, weight=1)
    Totlist.grid_columnconfigure(0, weight=1)
    Totlist.grid_columnconfigure(1, weight=0)

    scrollbar = tk.Scrollbar(Totlist, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    def add_exhibition_detail_btn():
        for widget in add_details_frame.winfo_children()[2:]:
            widget.destroy()
        title=ttk.Label(add_details_frame,text="Add New Exhibition details: ",font=('Sitka Text Semibold', 12),background="#f8e5dc")
        title.grid(row=1,column=0,columnspan=2,padx=10,pady=10)

        name=ttk.Label(add_details_frame,text="Enter Name of exhibition: ",font=('Sitka Text Semibold', 12),background="#f8e5dc")
        name.grid(row=2,column=0,padx=10,pady=10)
        enter_name = ttk.Entry(add_details_frame, style="EntryButton.TEntry")
        enter_name.grid(row=2,column=1,padx=10,pady=10)

        start_date=ttk.Label(add_details_frame, text="Start Date:", font=("Sitka Text", 12), background="#f8e5dc")
        start_date.grid(row=3, column=0, padx=10, pady=10, sticky="n")
        start_date_entry = DateEntry(add_details_frame, font=("Sitka Text", 12), date_pattern="dd-mm-yyyy")
        start_date_entry.grid(row=3, column=1, padx=10, pady=10, sticky="n")

        end_date=ttk.Label(add_details_frame, text="End Date:", font=("Sitka Text", 12), background="#f8e5dc")
        end_date.grid(row=4, column=0, padx=10, pady=10, sticky="n")
        end_date_entry = DateEntry(add_details_frame, font=("Sitka Text", 12), date_pattern="dd-mm-yyyy")
        end_date_entry.grid(row=4, column=1, padx=10, pady=10, sticky="n")

        location=ttk.Label(add_details_frame, text="Location:", font=("Sitka Text", 12), background="#f8e5dc")
        location.grid(row=5, column=0, padx=10, pady=10, sticky="n")
        location_entry = ttk.Entry(add_details_frame, style="EntryButton.TEntry")
        location_entry.grid(row=5, column=1, padx=10, pady=10, sticky="n")

        add_exhibition_detail=ttk.Button(add_details_frame,text="Add Exhibition Details",command=lambda:add_exhibition(enter_name,start_date_entry,end_date_entry,location_entry),style="Buttonstyle.TButton")
        add_exhibition_detail.grid(row=6,column=0,columnspan=2,padx=10,pady=10)

    def add_exhibition(enter_name,start_date_entry,end_date_entry,location_entry):
        name = enter_name.get()
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()
        location = location_entry.get()
        try:
            start_date = datetime.strptime(start_date, '%d-%m-%Y').strftime('%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%d-%m-%Y').strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use DD-MM-YYYY.")
            return
        if name and start_date and end_date and location:
            execute_query("INSERT INTO Exhibitions (title, start_date, end_date, location) VALUES (%s, %s, %s, %s)", (name, start_date, end_date, location))
        else:
            messagebox.showerror("Error", "All fields are required")
        enter_name.delete(0, tk.END)
        start_date_entry.delete(0, tk.END)
        end_date_entry.delete(0, tk.END)
        location_entry.delete(0, tk.END)
        for widget in add_details_frame.winfo_children()[2:]:
            widget.forget()
        add_new_btn=ttk.Button(add_details_frame,text="Add Exhibition Detail",command=add_exhibition_detail_btn,style="Buttonstyle.TButton")
        add_new_btn.grid(row=0,column=0,padx=10,pady=10,sticky="nsew")
        add_exhi_detail=ttk.Button(add_details_frame,text="Add new Artwork",command=add_artwork_exhibition_btn,style="Buttonstyle.TButton")
        add_exhi_detail.grid(row=0,column=1,padx=10,pady=10,sticky="nsew")

    def add_artwork_exhibition_(enter_exhi_id,enter_artwork_id):
        exhibition_id = enter_exhi_id.get()
        artwork_id = enter_artwork_id.get()
        if exhibition_id and artwork_id:
            execute_query("INSERT INTO artwork_exhibitions (exhibition_id, artwork_id) VALUES (%s, %s)", (exhibition_id, artwork_id))
        else:
            messagebox.showerror("Error", "All fields are required")
        enter_exhi_id.delete(0, tk.END)
        enter_artwork_id.delete(0, tk.END)
        for widget in canvas.winfo_children()[2:]:
            widget.forget()
        add_new_btn=ttk.Button(add_details_frame,text="Add Exhibition Detail",command=add_exhibition_detail_btn,style="Buttonstyle.TButton")
        add_new_btn.grid(row=0,column=0,padx=10,pady=10,sticky="nsew")
        add_exhi_detail=ttk.Button(add_details_frame,text="Add new Artwork",command=add_artwork_exhibition_btn,style="Buttonstyle.TButton")
        add_exhi_detail.grid(row=0,column=1,padx=10,pady=10,sticky="nsew")

    def display_exhibition_details():
        for widget in canvas.winfo_children()[2:]:
            widget.destroy()
        row=0
        selected_exhibition = exhibition_dropdown.get()
        if not selected_exhibition or selected_exhibition == "Select an exhibition":
            return
        exhibition_id = selected_exhibition.split(" - ")[0]
        exhibition_data = fetch_data("SELECT title, start_date, end_date, location FROM exhibitions WHERE exhibition_id = %s", (exhibition_id,))
        if exhibition_data:
            title, start_date, end_date, location = exhibition_data[0]                
            details_label = ttk.Label(canvas,text=f"Exhibition: {title}\nStart Date: {start_date}\nEnd Date: {end_date}\nLocation: {location}",font=('Palatino Linotype', 12),background="#fbf2ee",justify="left")
            details_label.grid(row=row, column=0, columnspan=2, padx=10, pady=10, sticky="w")
            row=row+1
            artworks = fetch_data("SELECT artworks.title FROM artwork_exhibitions INNER JOIN artworks ON artwork_exhibitions.artwork_id = artworks.id WHERE artwork_exhibitions.exhibition_id = %s", (exhibition_id,))

            if artworks:
                artworks_label = ttk.Label(canvas,text="Artworks:",font=('Palatino Linotype', 12),wraplength=350,background="#fbf2ee")
                artworks_label.grid(row=row, column=0, columnspan=2, padx=10, pady=5, sticky="w")
                row=row+1

                # List all artworks
                for artwork in artworks:
                    artwork_label = ttk.Label(canvas,text=f"- {artwork[0]}",font=('Palatino Linotype', 12),wraplength=350,background="#fbf2ee")
                    artwork_label.grid(row=row, column=0, columnspan=2, padx=10, pady=2, sticky="w")
                    row=row+1
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
        else:
            no_artworks_label = ttk.Label(canvas,text="No artworks found for this exhibition.",font=('Palatino Linotype', 12),background="#fbf2ee")
            no_artworks_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="w")

    def add_artwork_exhibition_btn():
        if add_details_frame.winfo_exists():
            children = add_details_frame.winfo_children()
            if len(children) > 2:
                for widget in children[2:]:
                    widget.destroy()
        title=ttk.Label(add_details_frame,text="Add Artwork to Exhibition: ",font=('Sitka Text Semibold', 12),background="#f8e5dc")
        title.grid(row=1,column=0,columnspan=2,padx=10,pady=10)

        exhibition_id=tk.Label(add_details_frame, text="Exhibition:", font=("Sitka Text", 12), bg="#fdf3ee")
        exhibition_id.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        enter_exhi_id = ttk.Entry(add_details_frame, style="EntryButton.TEntry")
        enter_exhi_id.grid(row=2,column=1,padx=10,pady=10)

        exhibition_details = fetch_data("SELECT exhibition_id, title FROM exhibitions")
        popup_details_exhi=[]
        for details in exhibition_details:
            popup_details_exhi.append(f"{details[0]} - {details[1]}")
        exhibition_box = ttk.Combobox(add_details_frame, values=popup_details_exhi, width=20, font=('Segoe UI', 12))
        exhibition_box.set("Select an exhibition")  # Default text
        exhibition_box.grid(row=3,column=1,pady=10)
        exhibition_box.bind("<<ComboboxSelected>>", lambda e: on_select_exhibition(exhibition_box,enter_exhi_id))

        artwork_id=tk.Label(add_details_frame, text="ArtWork:", font=("Sitka Text", 12), bg="#fdf3ee")
        artwork_id.grid(row=4, column=0, padx=10, pady=5, sticky="e")
        enter_artwork_id = ttk.Entry(add_details_frame, style="EntryButton.TEntry")
        enter_artwork_id.grid(row=4,column=1,padx=10,pady=10)

        artwork_details = fetch_data("SELECT id, title FROM artworks")
        popup_details_artwork=[]
        for details in artwork_details:
            popup_details_artwork.append(f"{details[0]} - {details[1]}")
        artwork_box = ttk.Combobox(add_details_frame, values=popup_details_artwork, width=20, font=('Segoe UI', 12))
        artwork_box.set("Select an artwork")  # Default text
        artwork_box.grid(row=5,column=1,pady=10)
        artwork_box.bind("<<ComboboxSelected>>", lambda e: on_select_artwork(artwork_box,enter_artwork_id,artwork_details))

        add_artwork_exhibition=ttk.Button(add_details_frame,text="Add Artwork to Exhibition",command=lambda:add_artwork_exhibition_(enter_exhi_id,enter_artwork_id),style="Buttonstyle.TButton")
        add_artwork_exhibition.grid(row=6,column=0,columnspan=2,padx=10,pady=10)

    def on_select_exhibition(exhibition_box,enter_exhi_id):
        selected_name = exhibition_box.get()
        for exhibition in exhibition_details:
            if selected_name == f"{exhibition[0]} - {exhibition[1]}":
                enter_exhi_id.delete(0, tk.END)
                enter_exhi_id.insert(0, exhibition[0])
                break

    def on_select_artwork(artwork_box,enter_artwork_id,artwork_details):
        selected_name = artwork_box.get()
        for artwork in artwork_details:
            if selected_name == f"{artwork[0]} - {artwork[1]}":
                enter_artwork_id.delete(0, tk.END)
                enter_artwork_id.insert(0, artwork[0])
                break
    
    exhibition_dropdown.bind("<<ComboboxSelected>>", lambda e: display_exhibition_details())
    canvas.update_idletasks()  # Ensures all geometry changes are applied
    canvas.configure(scrollregion=canvas.bbox("all"))
    container_frame.update_idletasks()  # Updates geometry changes
    canvas.configure(scrollregion=canvas.bbox("all"))
    add_new_btn=ttk.Button(add_details_frame,text="Add Exhibition Detail",command=add_exhibition_detail_btn,style="Buttonstyle.TButton")
    add_new_btn.grid(row=0,column=0,padx=10,pady=10,sticky="nsew")
    add_exhi_detail=ttk.Button(add_details_frame,text="Add new Artwork",command=add_artwork_exhibition_btn,style="Buttonstyle.TButton")
    add_exhi_detail.grid(row=0,column=1,padx=10,pady=10,sticky="nsew")