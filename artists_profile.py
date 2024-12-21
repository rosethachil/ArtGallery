from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from db import fetch_data,execute_query

def load_artist_profile(tab):
    frame = tk.Frame(tab, bg="#fbf2ee",borderwidth=2)
    frame.grid(row=0, rowspan=15, column=0, columnspan=3, pady=15, padx=15, sticky="nsew")

    canvas = tk.Canvas(frame, bg="#fbf2ee", highlightthickness=0,height=500)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    Totlist = tk.Frame(canvas, bg="#fbf2ee")
    canvas.create_window((0, 0), window=Totlist, anchor="nw")

    style = ttk.Style(tab)
    style.configure("Buttonstyle.TButton",font=('Sitka Text Semibold', 10),background="#D58B73",foreground="#FFFFFF", borderwidth=1)
    style.map("Buttonstyle.TButton",foreground=[("active", "#FFFFFF")])
    style.map("Buttonstyle.TButton", background=[("!active", "#ad7a77"), ("active", "#a83d4c")])
    style.configure("EntryButton.TEntry",font=('Segoe UI Semibold', 12),fieldbackground="#cbb1a0",foreground="#5C4531",bordercolor="#735559",padding=[5, 2] )

    def create_add_btn():
        clear_row(1, tab)
        clear_row(2, tab)
        clear_row(3, tab)
        name=ttk.Label(tab,text="Enter Name: ",font=('Sitka Text Semibold', 12),background="#f8e5dc")
        name.grid(row=1,column=7,padx=10,pady=10)
        enter_name = ttk.Entry(tab, style="EntryButton.TEntry")
        enter_name.grid(row=1,column=8,padx=10,pady=10)

        bio=ttk.Label(tab,text="Enter Bio: ",font=('Sitka Text Semibold', 12),background="#f8e5dc")
        bio.grid(row=2,column=7,padx=10,pady=10)
        enter_bio=ttk.Entry(tab,style="EntryButton.TEntry")
        enter_bio.grid(row=2,column=8,padx=10,pady=10)

        add_button=ttk.Button(tab,text="Add Artist Details",style="Buttonstyle.TButton",command=lambda:add_artist(enter_name,enter_bio))
        add_button.grid(row=3,column=7,padx=10,pady=10)
        
    def add_artist(enter_name,enter_bio):
        name = enter_name.get()
        bio = enter_bio.get()
        if name:
            execute_query("INSERT INTO Artists (name, bio) VALUES (%s, %s)", (name, bio))
            refresh_list()
        else:
            messagebox.showerror("Error", "Name is required")
        enter_name.delete(0,tk.END)
        enter_bio.delete(0,tk.END)

    def create_search_btn():
        clear_row(1, tab)
        clear_row(2, tab)
        clear_row(3, tab)
        name=ttk.Label(tab,text="Enter Name: ",font=('Sitka Text Semibold', 12),background="#f8e5dc")
        name.grid(row=1,column=7,padx=10,pady=10)
        enter_name=ttk.Entry(tab,style="EntryButton.TEntry")
        enter_name.grid(row=1,column=8,padx=10,pady=10)
        search_btn=ttk.Button(tab,text="Find Artist details",style="Buttonstyle.TButton",command=lambda: search_artist(enter_name))
        search_btn.grid(row=2,column=7,padx=10,pady=10)

    def search_artist(enter_name):
        row=1
        name=enter_name.get()
        for widget in Totlist.winfo_children():
            widget.destroy()
        if name:
            artists = fetch_data("SELECT * FROM artists WHERE name = %s", (name,))
            if artists:
                for artist in artists:
                    artist_id = artist[0]
                    row=row+1
                    tk.Label(Totlist,text=f"Artist ID: {artist[0]}",font=('Palatino Linotype', 12),bg="#fbf2ee").grid(row=row,column=0,columnspan=3,sticky="ew")
                    row=row+1
                    tk.Label(Totlist, text=f"Name: {artist[1]}", font=('Palatino Linotype', 14),bg="#fbf2ee").grid(row=row,column=0,columnspan=3,sticky="ew")
                    delete_btn = ttk.Button(Totlist, text="Delete", style="Buttonstyle.TButton", command=lambda artist_id=artist_id: delete_artist(artist_id))
                    delete_btn.grid(row=row,column=4, padx=10, pady=5)
                    row=row+1
                    tk.Label(Totlist, text=f"Bio: {artist[2]}", font=('Palatino Linotype', 12),bg="#fbf2ee").grid(row=row,column=0,columnspan=3,sticky="ew")
                    edit_btn = ttk.Button(Totlist, text="Edit", style="Buttonstyle.TButton", command=lambda artist_id=artist_id: edit_details(artist_id))
                    edit_btn.grid(row=row,column=4, padx=10, pady=5)
                    row=row+1
                    tk.Label(Totlist, text="-"*50,bg="#fbf2ee").grid(row=row,column=0,columnspan=3,sticky="ew")
            else:
                messagebox.showinfo("No Results", f"No artist found with the name '{name}'")
                refresh_list()
        else:
            messagebox.showerror("Incomplete Data","No Name Entered!!'")
        enter_name.delete(0,tk.END)

    def refresh_list():
        row=1
        for widget in Totlist.winfo_children():
            widget.destroy()
        artists = fetch_data("SELECT * FROM Artists")
        if not artists:
            tk.Label(Totlist, text="No artists found", font=('Lucida Sans Typewriter', 10), bg="#fbf2ee").grid(row=row,column=0, columnspan=3, sticky="ew")
        for artist in artists:
            artist_id = artist[0]
            row=row+1
            tk.Label(Totlist,text=f"Artist ID: {artist[0]}",font=('Palatino Linotype', 12),bg="#fbf2ee").grid(row=row,column=0,columnspan=3,sticky="ew")
            row=row+1
            tk.Label(Totlist, text=f"Name: {artist[1]}", font=('Palatino Linotype', 14),bg="#fbf2ee").grid(row=row,column=0,columnspan=3,sticky="ew")
            delete_btn = ttk.Button(Totlist, text="Delete", style="Buttonstyle.TButton", command=lambda artist_id=artist_id: delete_artist(artist_id))
            delete_btn.grid(row=row,column=4, padx=10, pady=5)
            row=row+1
            tk.Label(Totlist, text=f"Bio: {artist[2]}", font=('Palatino Linotype', 12),bg="#fbf2ee").grid(row=row,column=0,columnspan=3,sticky="ew")
            edit_btn = ttk.Button(Totlist, text="Edit", style="Buttonstyle.TButton", command=lambda artist_id=artist_id: edit_details(artist_id))
            edit_btn.grid(row=row,column=4, padx=10, pady=5)
            row=row+1
            tk.Label(Totlist, text="-"*50,bg="#fbf2ee").grid(row=row,column=0,columnspan=3,sticky="ew")

    def edit_details(id):
        if id:
            clear_row(1, tab)
            clear_row(2, tab)
            clear_row(3, tab)
            name=ttk.Label(tab,text="Enter edited Name: ",font=('Sitka Text Semibold', 12),background="#f8e5dc")
            name.grid(row=1,column=7,padx=10,pady=10)
            enter_name = ttk.Entry(tab, style="EntryButton.TEntry")
            enter_name.grid(row=1,column=8,padx=10,pady=10)

            bio=ttk.Label(tab,text="Enter edited Bio: ",font=('Sitka Text Semibold', 12),background="#f8e5dc")
            bio.grid(row=2,column=7,padx=10,pady=10)
            enter_bio=ttk.Entry(tab,style="EntryButton.TEntry")
            enter_bio.grid(row=2,column=8,padx=10,pady=10)

            add_button=ttk.Button(tab,text="Edit Artist Details",style="Buttonstyle.TButton",command=lambda:edit_database(id,enter_name,enter_bio))
            add_button.grid(row=3,column=7,padx=10,pady=10)

    def edit_database(id,enter_name=None,enter_bio=None):
        name=enter_name.get()
        bio=enter_bio.get()
        if name and bio:
            execute_query("UPDATE Artists SET name = %s WHERE id= %s",(name,id))
            execute_query("UPDATE Artists SET bio = %s WHERE id= %s",(bio,id))
            enter_name.delete(0,tk.END)
            enter_bio.delete(0,tk.END)
            refresh_list()
        elif name:
            execute_query("UPDATE Artists SET name = %s WHERE id= %s",(name,id))
            enter_name.delete(0,tk.END)
            refresh_list()
        elif bio:
            execute_query("UPDATE Artists SET bio = %s WHERE id= %s",(bio,id))
            enter_bio.delete(0,tk.END)
            refresh_list()
        else:
            return

    def clear_row(row, tab):
        for widget in tab.grid_slaves():
            if widget.grid_info()["row"] == row:
                widget.destroy()

    def delete_artist(id):
        if id:
            execute_query("DELETE FROM Artists WHERE id = (%s)", (id,))
            refresh_list()


    refresh_list()
    add_new_btn=ttk.Button(tab,text="Add new Artist",command=create_add_btn,style="Buttonstyle.TButton")
    add_new_btn.grid(row=0,column=7,padx=10,pady=10,sticky="nw")
    search_artist_btn=ttk.Button(tab,text="Search Artist",command=create_search_btn,style="Buttonstyle.TButton")
    search_artist_btn.grid(row=0,column=8,padx=10,pady=10,sticky="nw")
