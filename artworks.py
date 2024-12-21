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
    artwork_frame.grid(row=0, column=0, sticky="nsew")

    tab.grid_rowconfigure(0, weight=1)
    tab.grid_columnconfigure(0, weight=1)

    canvas = tk.Canvas(artwork_frame, bg="#f8e5dc", highlightthickness=0)
    canvas.grid(row=0, column=0, sticky="nsew")

    scrollbar = tk.Scrollbar(artwork_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")

    canvas.configure(yscrollcommand=scrollbar.set)
    artwork_frame.grid_rowconfigure(0, weight=1)
    artwork_frame.grid_columnconfigure(0, weight=1)

    Totlist = tk.Frame(canvas, bg="#f8e5dc")
    canvas.create_window((0, 0), window=Totlist, anchor="nw")

    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    def refresh():
        row=1
        for widget in Totlist.winfo_children():
            widget.destroy()
        artists = fetch_data("SELECT * FROM Artists")
        artworks = fetch_data("SELECT * FROM Artworks")
        ArtWorkImages=fetch_data("SELECT * FROM images")
        if not artworks:
            tk.Label(Totlist, text="No artwork found", font=('Lucida Sans Typewriter', 10), bg="#fbf2ee").grid(row=row,column=0, columnspan=3, sticky="ew")
            row+=1
        for artist in artists:
            for artwork in artworks:
                artwork_id = artwork[0]
                tk.Label(Totlist,text=f"Artwork ID: {artwork[0]}",font=('Palatino Linotype', 12),bg="#fbf2ee").grid(row=row,column=0,sticky="ew")
                row+=1
                tk.Label(Totlist, text=f"Art Work Title: {artwork[2]}", font=('Palatino Linotype', 14),bg="#fbf2ee").grid(row=row,column=0,sticky="ew")
                row+=1
                if ArtWorkImages and ArtWorkImages[0]: 
                    img_path = ArtWorkImages[0][2]
                    try:
                        img = Image.open(img_path)
                        img = img.resize((200, 200))
                        img_tk = ImageTk.PhotoImage(img)
                        image_label = tk.Label(Totlist, image=img_tk, bg="#fbf2ee")
                        image_label.image = img_tk
                        image_label.grid(row=row, column=0, pady=5)
                        row+=1
                    except Exception as e:
                        tk.Label(Totlist, text="Error loading image: {e}",font=('Lucida Sans Typewriter', 10), bg="#fbf2ee").grid(row=row,column=0, columnspan=3, sticky="ew")
                        row+=1
                else:
                    tk.Label(Totlist, text="No valid image path found in the database.",font=('Lucida Sans Typewriter', 10), bg="#fbf2ee").grid(row=row,column=0, columnspan=3, sticky="ew")
                    row+=1

                tk.Label(Totlist, text=f"Artist Name: {artist[1]}", font=('Palatino Linotype', 14),bg="#fbf2ee").grid(row=row,column=0,sticky="ew")
                row+=1
                tk.Label(Totlist, text=f"Year: {artwork[3]}", font=('Palatino Linotype', 14),bg="#fbf2ee").grid(row=row,column=0,sticky="ew")
                row+=1
                delete_btn = ttk.Button(Totlist, text="Delete", style="Buttonstyle.TButton", command=lambda artist_id=artwork_id: delete_artwork(artwork_id))
                delete_btn.grid(row=row,column=0, padx=10, pady=5)
                edit_btn = ttk.Button(Totlist, text="Edit", style="Buttonstyle.TButton", command=lambda artist_id=artwork_id: edit_artwork_details(artist_id))
                edit_btn.grid(row=row,column=1, padx=10, pady=5)

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

    refresh()
