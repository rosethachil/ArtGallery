# Digital Art Gallery 🎨

A user-friendly digital platform to explore artist profiles, artworks, and exhibitions. This desktop application leverages Python's Tkinter library for the GUI and MySQL for database management.

---

## Features 🖌️
- **Artist Profiles**: Add, edit, search, and delete artist details.
- **Artwork Gallery**: View and manage artwork details.
- **Exhibitions**: Explore upcoming and past exhibitions.
- Intuitive and customizable GUI.

---
## Table of Contents 📜
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)


## Installation 🔧

### Install Dependencies
1. Ensure you have Python installed (version 3.7 or higher recommended).  
2. Install the required Python library by running:  
   ```bash
   pip install mysql-connector-python


3. Set Up the Database
4. Install MySQL if it is not already installed on your system.
5. For installation instructions, visit MySQL Downloads.
6. Log in to MySQL using the command line:
    ```bash
    mysql -u root -p
7. Create the database: 
    ```bash
    CREATE DATABASE ArtGalleryDB;
8. Import the database schema using the provided database_dump.sql file:
    ```bash 
    mysql -u root -p ArtGalleryDB < database_dump.sql

9. Verify the database setup matches the application requirements:
    Artists Table: Includes fields id, name, and bio.
    Artworks Table: Includes fields id, name, artist_id, and description.
    Exhibitions Table: Links artworks and exhibitions.

### Usage 🎯
1. Launch the app by running: 
    ```bash
    python app.py
2. Navigate through the application tabs to manage artists, artworks, and exhibitions.
3. Add images to the images/ folder to associate them with artworks.

### Project Structure 🗂️
    ```bash
    📦 Digital Art Gallery
    ├── app.py                # Main application entry point
    ├── artists_profile.py    # Artist profile management logic
    ├── artworks.py           # Artwork managment logic
    ├── exhibitions.py        # Exhibition management logic
    ├── db.py                 # Database connection and queries
    ├── database_dump.sql     # Database schema and initial setup
    ├── images/               # Directory to store artwork images
    └── README.md             # Project documentation
