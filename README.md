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


## Installation 🔧

### Install Dependencies
1. Ensure you have Python installed (version 3.7 or higher recommended).  
2. Install the required Python library by running:  
   ```bash
   pip install mysql-connector-python


3. Set Up the Database
Install MySQL if it is not already installed on your system.
For installation instructions, visit MySQL Downloads.
Log in to MySQL using the command line: mysql -u root -p
Create the database: CREATE DATABASE ArtGalleryDB;
Import the database schema using the provided database_dump.sql file: mysql -u root -p ArtGalleryDB < database_dump.sql

Verify the database setup matches the application requirements:
Artists Table: Includes fields id, name, and bio.
Artworks Table: Includes fields id, name, artist_id, and description.
Exhibitions Table: Links artworks and exhibitions.