import tkinter as tk
from tkinter import ttk
from artists_profile import load_artist_profile
from artworks import load_artworks
from exhibitions import load_exhibitions_profile

root = tk.Tk()
print(root)
root.title("Digital Art Gallery")
root.geometry("960x750")
root.config(bg="#735559")

style = ttk.Style()
style.theme_use('default')  # Ensure you are using a style that allows customizations
style.configure("TNotebook",background="#8e5c66", borderwidth=0,)
style.configure("TNotebook.Tab",background="#8e5c66",foreground="#e2c1b2",padding=(10, 10),font=('Dutch801 XBd BT', 12))
style.map("TNotebook.Tab",background=[("selected", "#e2c1b2")],foreground=[("selected", "#3c2c2e")],)

root.grid_rowconfigure(1, weight=3)   
root.grid_columnconfigure(0, weight=1) 

heading = tk.Label(root, text="Digital Art Gallery",font=('Imprint MT Shadow', 22),bg="#735559",fg="#f8e5dc")
heading.grid(row=0,column=0,padx=30,pady=(10,5),sticky="n")

notebook = ttk.Notebook(root, style="TNotebook")
notebook.grid(row=1, column=0, padx=15, pady=10, sticky="nsew")

artist_tab = tk.Frame(notebook, bg="#f8e5dc",padx=5,pady=5)
notebook.add(artist_tab,text="Artist Profiles")
load_artist_profile(artist_tab)

artwork_tab = tk.Frame(notebook, bg="#f8e5dc",padx=5,pady=5)
notebook.add(artwork_tab, text="Artwork Gallery")
load_artworks(artwork_tab)

exhibitions_tab = tk.Frame(notebook, bg="#f8e5dc",padx=10,pady=10)
notebook.add(exhibitions_tab, text="Exhibitions")
load_exhibitions_profile(exhibitions_tab)


root.mainloop()