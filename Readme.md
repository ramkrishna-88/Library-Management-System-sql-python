# Library Management System (Python + Tkinter + MySQL)

A GUI-based Library Management System built using Python Tkinter for the frontend and MySQL for the backend database.
This application allows users to Add, Search, Update, Delete, and View book records in an interactive desktop interface.

---
## Table of Contents

- <a href="#Features">Features</a>
- <a href="#Technologies Used">Technologies Used</a>
- <a href="#Project Structure">Project Structure</a>
- <a href="#Install & Setup">Install & Setup</a>
- <a href="#Database Setup">Database Setup</a>
- <a href="#Configure Datebase Connection">Configure Datebase Connection</a>
- <a href="#Run the Application">Run the Application</a>
- <a href="#Application Interface">Application Interface</a>
- <a href="#Future Enhancements">Future Enhancements</a>
- <a href="#Author">Author</a>

---
<h2><a class="anchor" id=" Features"></a>Features</h2>

- Add new books with title, author, genre, and status
- Search books by title, author, genre, or status
- Update existing book records
- Delete book records by ID
- View all books in a table format
- User-friendly Tkinter GUI with styled buttons and tables

---
<h2><a class="anchor" id="Technologies Used"></a>Technologies Used</h2>

- Python 3.x
- Tkinter (GUI)
- MySQL
- PyMySQL (Python-MySQL Connector)
- ttk Treeview (for table display)

---
<h2><a class="anchor" id="Project Structure"></a>Project Structure</h2>

library-management-system/
│
├── 📄 README.md
├── 📄 Requirements.txt
├── 📄 library_app.py
│
├── 📂 database/
│   └── 📄 librarydb.sql
│
├── 📂 assets/
│   ├── 📄 screenshots/
│   │   ├── main_window.png
│   │   ├── add_book.png
│   │   ├── search_book.png
│   │   └── update_book.png
│   │
│   └── 📄 icons/
│       └── app_icon.ico
│
├── 📂 docs/
│   └── 📄 project_report.pdf
│
└── 📄 .gitignore

---
<h2><a class="anchor" id="Install & Setup"></a>Install & Setup</h2>

- Clone the Repository
    git clone https://github.com/your-username/library-management-system.git
    cd library-management-system

-  Install Required Modules
    pip install pymysql
(Tkinter comes pre-installed with Python on Windows)

---
<h2><a class="anchor" id="Database Setup"></a>Database Setup</h2>

CREATE DATABASE librarydb;

USE librarydb;

CREATE TABLE books (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255),
    author VARCHAR(255),
    genre VARCHAR(100),
    status VARCHAR(50)
);

---
<h2><a class="anchor" id="Configure Datebase Connection"></a>Configure Datebase Connection</h2>

self.con = pymysql.connect(
    host="localhost",
    user="root",
    passwd="Ram@1234",
    database="librarydb"
)

---
<h2><a class="anchor" id="Run the Application"></a>Run the Application</h2>

python library_app.py

---
<h2><a class="anchor" id="Application Interface"></a>Application Interface</h2>

- Left Panel: Navigation Buttons
- Right Panel: Book Records Table
- Popup Forms: Add, Search, Update, Delete Operations

---
<h2><a class="anchor" id="Future Enhancements"></a>Future Enhancements</h2>

- User Login System
- Book Issue/Return Tracking
- Export Data to Excel/PDF
- Web-based Version

---
## Author

Ram Krishna
Email: ramkrishna000888@gmail.com
Linkeddin: https://www.linkedin.com/in/ramkrishna000/