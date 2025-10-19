# City-Alert-App

City Alert is a Python–Kivy mobile app that enables citizens to report and visualize nearby crimes or suspicious activities.
It uses HERE Maps, Geocoder, and Plyer APIs to collect, display, and locally store incidents with time and location data — empowering safer, connected neighborhoods.

🚀 Features

Quick Crime Reporting — Report an incident by entering description, location, and category.

Real-Time Map View — View crime markers around your live position.

Category Selector — Choose crime type (theft, vandalism, assault, etc.) via toggle buttons.

Local Data Storage — All reports are saved locally in crime.txt for persistence.

Instant Marker Updates — Submitted reports appear as map markers for all entries.

Search and Location Update — Built-in search and “current location” refresh button.

🧠 How the Code Works
🎯 Main Structure

Framework: Kivy (UI + Screen Management)

File: cityalert.py — contains all screens, logic, and layout (KV language embedded).

Screens:

SignInScreen — User enters name and phone number (saved locally).

MapScreen — Displays HERE Map, shows markers for all crimes.

Reportscreen — Used for reporting new incidents with date, time, and location.

CrimeReportScreen — Lets users select crime type.

Report — Confirmation screen for successful submission.

🧩 Core Logic

Local Storage:
User data → user_data.txt
Reports → crimereport/crime.txt (each line stores [crime, description, lat, lon]).

Map Handling:
Uses kivy.garden.mapview.MapView and MapMarker for visualization.
HERE Maps API handles geocoding (text search → coordinates).

Marker Popups:
When users tap a map marker, a popup displays crime type and description.

Location Fetch:
Uses geocoder.ip('me') to detect approximate location.

Threads & GPS:
Background threads handle blinking markers and GPS tracking safely.

⚙️ Installation & Setup
1️⃣ Install Dependencies

Make sure you have Python 3.9+ installed.
Then run this in terminal or command prompt:

pip install kivy kivy-garden requests geocoder plyer
garden install mapview

2️⃣ Add Project Files

Ensure all assets are in the same directory:

cityalert.py
CityAlert.png
icon.jpg
alert1.png
back.png
c_location.png


These image files are used for background, buttons, and markers.
Map tiles and cache are handled automatically by Kivy Garden’s MapView.

3️⃣ Run the App
python cityalert.py


The window (324x576 px) opens — designed for a mobile-style interface.
You’ll first sign in → view map → add or view reports.
