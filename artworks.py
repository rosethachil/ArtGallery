from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from db import fetch_data,execute_query

def load_artworks(tab):
    style = ttk.Style(tab)
    style.configure("Buttonstyle.TButton",font=('Sitka Text Semibold', 10),background="#D58B73",foreground="#FFFFFF", borderwidth=1)
    style.map("Buttonstyle.TButton",foreground=[("active", "#FFFFFF")])
    style.map("Buttonstyle.TButton", background=[("!active", "#ad7a77"), ("active", "#a83d4c")])
    style.configure("EntryButton.TEntry",font=('Segoe UI Semibold', 12),fieldbackground="#cbb1a0",foreground="#5C4531",bordercolor="#735559",padding=[5, 2] )
    
    artwork_frame = tk.Frame(tab, bg="#f8e5dc",borderwidth=2)
    artwork_frame.grid(row=1, column=0, sticky="nsew")

    tab.grid_rowconfigure(1, weight=1)
    tab.grid_columnconfigure(0, weight=1)

    canvas = tk.Canvas(artwork_frame, bg="#f8e5dc", highlightthickness=0)
    canvas.grid(row=0, column=0, sticky="nsew")

    scrollbar = tk.Scrollbar(artwork_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    canvas.configure(yscrollcommand=scrollbar.set)

    Totlist = tk.Frame(canvas, bg="#f8e5dc")
    canvas.create_window((0, 0), window=Totlist, anchor="nw")

    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    def refresh():
        for widget in artwork_frame.winfo_children():
            widget.destroy()

        query = """
            SELECT Artworks.id, Artworks.title, Artworks.year, Artists.name, Artworks.image_path
            FROM Artworks
            JOIN Artists ON Artworks.artist_id = Artists.id
        """

        try:
            artwork_data = fetch_data(query)

            if not artwork_data:
                tk.Label(artwork_frame, text="No artworks found.", font=("Sitka Text", 12)).pack()
                return
            row = 0
            for artwork_id, title, year, artist_name, image_path in artwork_data:
            # Artwork details
                details_text = f"ID: {artwork_id}, Title: {title}, Year: {year}, Artist: {artist_name}"
                tk.Label(artwork_frame, text=details_text, font=("Sitka Text", 12), bg="#f8e5dc").grid(row=row, column=0, columnspan=2, sticky="w", padx=10, pady=5)
                try:
                    img = Image.open(image_path)
                    img = img.resize((150, 150), Image.ANTIALIAS)
                    img_tk = ImageTk.PhotoImage(img)
                    img_label = tk.Label(artwork_frame, image=img_tk, bg="#f8e5dc")
                    img_label.image = img_tk 
                    img_label.grid(row=row, column=2, padx=10, pady=5)
                except Exception:
                    tk.Label(artwork_frame, text="Image not found", font=("Sitka Text", 10), bg="#f8e5dc").grid(row=row, column=2, padx=10, pady=5)
                delete_btn = ttk.Button(
                    artwork_frame,
                    text="Delete",
                    command=lambda artwork_id=artwork_id: delete_artwork(artwork_id)
                )
                delete_btn.grid(row=row, column=3, padx=10)
                edit_btn = ttk.Button(
                    artwork_frame,
                    text="Edit",
                    command=lambda artwork_id=artwork_id: edit_artwork_details(artwork_id)
                )
                edit_btn.grid(row=row, column=4, padx=10)
                row += 1

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while refreshing: {e}")

    
    def create_add_btn():
        name=ttk.Label(tab,text="Enter Name: ",font=('Sitka Text Semibold', 12),background="#f8e5dc")
        name.grid(row=1,column=0,padx=10,pady=10)
        enter_name = ttk.Entry(tab, style="EntryButton.TEntry")
        enter_name.grid(row=1,column=1,padx=10,pady=10)

        bio=ttk.Label(tab,text="Enter Bio: ",font=('Sitka Text Semibold', 12),background="#f8e5dc")
        bio.grid(row=1,column=2,padx=10,pady=10)
        enter_bio=ttk.Entry(tab,style="EntryButton.TEntry")
        enter_bio.grid(row=1,column=3,padx=10,pady=10)

        add_button=ttk.Button(tab,text="Add Artist Details",style="Buttonstyle.TButton")
        add_button.grid(row=1,column=4,padx=10,pady=10)
    
    def delete_artwork(id):
        if id:
            execute_query("DELETE FROM Artworks WHERE id = (%s)", (id,))
            execute_query("DELETE FROM images WHERE artwork_id = (%s)", (id,))
            refresh()

    def edit_artwork_details(id):
        if not id:
            return
        artwork = fetch_data("SELECT * FROM Artworks WHERE id = %s", (id,))
        if not artwork:
            messagebox.showerror("Error", "Artwork not found!")
            return
        artwork = artwork[0]
        edit_window = tk.Toplevel()
        edit_window.title("Edit Artwork Details")
        edit_window.geometry("400x300")
        edit_window.configure(bg="#f8e5dc")

        tk.Label(edit_window, text="Edit Artwork Details", font=("Palatino Linotype", 16), bg="#f8e5dc").pack(pady=10)

        tk.Label(edit_window, text="Title:", font=("Sitka Text", 12), bg="#f8e5dc").pack()
        title_entry = ttk.Entry(edit_window, style="EntryButton.TEntry")
        title_entry.insert(0, artwork[2])
        title_entry.pack(pady=5)

        tk.Label(edit_window, text="Year:", font=("Sitka Text", 12), bg="#f8e5dc").pack()
        year_entry = ttk.Entry(edit_window, style="EntryButton.TEntry")
        year_entry.insert(0, artwork[3])
        year_entry.pack(pady=5)

        tk.Label(edit_window, text="Image Path:", font=("Sitka Text", 12), bg="#f8e5dc").pack()
        image_entry = ttk.Entry(edit_window, style="EntryButton.TEntry")
        image_data = fetch_data("SELECT path FROM images WHERE artwork_id = %s", (id,))
        if image_data:
            image_entry.insert(0, image_data[0][0]) 
        image_entry.pack(pady=5)

        def save_changes():
            new_title = title_entry.get()
            new_year = year_entry.get()
            new_image = image_entry.get()
            
            try:
                if new_title:
                    execute_query("UPDATE Artworks SET title = %s WHERE id = %s", (new_title, id))
                if new_year:
                    execute_query("UPDATE Artworks SET year = %s WHERE id = %s", (new_year, id))

                if new_image:
                    existing_image = fetch_data("SELECT * FROM images WHERE artwork_id = %s", (id,))
                    if existing_image:
                        execute_query("UPDATE images SET path = %s WHERE artwork_id = %s", (new_image, id))
                    else:
                        execute_query("INSERT INTO images (artwork_id, path) VALUES (%s, %s)", (id, new_image))
                
                messagebox.showinfo("Success", "Artwork details updated successfully!")
                edit_window.destroy()
                refresh()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        save_btn = ttk.Button(edit_window, text="Save Changes", style="Buttonstyle.TButton", command=save_changes)
        save_btn.pack(pady=20)

    add_new_btn=ttk.Button(tab,text="Add new Artwork",command=create_add_btn,style="Buttonstyle.TButton")
    add_new_btn.grid(row=0,column=1,padx=10,pady=10,sticky="nw")
    add_new_btn=ttk.Button(tab,text="Add new Artwork",command=create_add_btn,style="Buttonstyle.TButton")
    add_new_btn.grid(row=0,column=2,padx=10,pady=10,sticky="nw")
    refresh()
