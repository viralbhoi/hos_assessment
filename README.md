# HOS Navigator 🚚

**Automated ELD Logs & Route Optimization**

HOS Navigator is a full-stack application designed to automate Hours of Service (HOS) compliance for commercial truck drivers. By inputting trip details, the system calculates the optimal route, simulates the trip against strict FMCSA regulations, and automatically generates pixel-perfect, downloadable daily log sheets.

## ✨ Features

- **Route Optimization:** Accurately calculates trip distance, drive time, and route polylines using OSRM.
- **FMCSA Compliance Engine:** Automatically simulates mandatory 30-minute breaks, 10-hour sleeper berth periods, 34-hour restarts, and fuel stops based on the 11/14/70-hour rules.
- **Pixel-Perfect Log Generation:** Dynamically draws duty status graphs and text onto high-resolution blank FMCSA paper log templates.
- **Interactive Mapping:** Visualizes the entire route and pinpoints exact locations for fuel stops and mandatory rest breaks using Leaflet.
- **Premium UI/UX:** Built with an Apple HIG-inspired dark mode interface (true OLED blacks, tight typography, and subtle micro-interactions).
- **PDF Export:** Packages the generated daily logs into a clean, downloadable landscape PDF for immediate carrier submission.

## 🛠 Tech Stack

**Frontend:**

- React.js
- Tailwind CSS (Apple HIG customized)
- React Leaflet (Interactive mapping)
- jsPDF (Client-side document generation)

**Backend:**

- Python / Django REST Framework
- Pillow (PIL) for advanced image processing
- OSRM (Open Source Routing Machine) API

---

## 🧠 Approach Used to Complete the Task

Building this system required solving three distinct engineering challenges: routing, compliance simulation, and programmatic document generation.

### 1. Routing & Geocoding

Instead of relying on simple point-to-point math, the backend integrates with **OSRM**. When a user inputs their origin, pickup, and destination, the system geocodes the text into coordinates and fetches the actual road distances, estimated durations, and a highly detailed polyline for the frontend map.

### 2. Custom HOS Simulation Engine

To ensure compliance, a custom state-machine was built in Python (`hos_engine.py`). The engine takes the total trip miles and simulates a truck moving at an average speed. It constantly evaluates state variables against FMCSA rules:

- Tracks a 14-hour daily driving window and an 11-hour driving cap.
- Triggers a 30-minute Off-Duty break if driving exceeds 8 consecutive hours.
- Injects mandatory 10-hour Sleeper Berth rests.
- Monitors the 70-hour/8-day rolling cycle, injecting 34-hour resets when necessary.
- Calculates precise "mile marks" for each event to plot them back onto the map.

### 3. Pixel-Perfect Image Generation

Generating the classic paper logs required high precision. Using **Python Pillow (PIL)**, the system takes the output array from the HOS engine and maps it to specific `X` and `Y` pixel coordinates on a high-resolution blank log template.

- **Grid Rendering:** Time is divided into pixels (Midnight to Midnight) to accurately draw the thick blue duty-status lines.
- **Decoupled Alignment:** The text generation (cities, dates, mileages, and column totals) was completely decoupled from the graph's grid logic, allowing the system to place text squarely on the pre-printed underlines and inside designated bounding boxes for a production-grade visual output.

---

## 🚀 Local Setup

### Backend (Python/Django)

1. Navigate to the `backend` directory.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the server: `python manage.py runserver` (Defaults to `127.0.0.1:8000`)

### Frontend (React)

1. Navigate to the `frontend` directory.
2. Install dependencies: `npm install`
3. Start the development server: `npm run dev`
