# University Project: Vaccination Appointment App (Python/Kivy)

This repository contains the code and documentation for my 3rd-year individual project in the module **Advanced Topics in Computer Science (CN6008_1)**. The project focuses on building a functional, cross-platform prototype for managing COVID-19 vaccination bookings.

Repository Files:
-------

1. **vaccination_app.py**
   - The main application script built with the **Kivy framework**.
   - Features a modular architecture using **ScreenManager** with four distinct screens: Login, Center Selection, Appointment Scheduling, and Center Management.
   - Implements core logic for:
     • **Input Validation:** Restricts input to English characters and specific email domains like @gmail.com, @yahoo.com, and @outlook.com.
     • **Dynamic Scheduling:** Calculates available dates for the next 10 business days, automatically excluding weekends.
     • **Data Persistence:** Generates unique `.txt` records for each booking, stored locally for traceability.

2. **bookings/**
   - A local directory that serves as a lightweight storage system for appointment records.
   - Each file contains the user's email, appointment date, time, and selected vaccination center.

3. **Project Documentation**
   - Full technical report including **UML Use Case** and **Activity Diagrams**.
   - Includes project management artifacts such as **WBS (Work Breakdown Structure)** and **Gantt Charts**.

How to Run:
------------------

Prerequisites:
- Python 3.8+
- Install the required UI framework:
  `pip install kivy`

Run:
---------
Open the terminal and run:
> python vaccination_app.py