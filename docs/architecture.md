# PiCompliance - Architecture

PiCompliance is a tool that checks the security of a network or a set of devices and displays the results live on a web dashboard.

This document describes the project structure and the data flow between components.

---

## 1. Main Components

### Raspberry Pi (pi-scripts)
- Runs security scans: detects devices, open ports, default passwords.
- Sends detected data to the backend via API (HTTP Post / WebSocket).

### Backend (Python / FastAPI)
- Receives data from the Pi and stores it in a database.
- Provides APIs for the frontend (e.g., GET /devices, GET /alerts).

### Frontend (Angular)
- Receives data from the backend.
- Displays a live dashboard: device table, visual alerts, and charts.

---

## 2. Data Flow

[ Raspberry Pi ] ---> (HTTP POST / WebSocket) ---> [ Backend Python ] ---> (REST API) ---> [ Frontend Angular ]


- The Pi sends scanned data to the backend.
- The backend stores and exposes the data via REST API.
- The frontend consumes the API and displays the live dashboard.

---

## 3. Project Folder Structure

PiCompliance/
├─ pi-scripts/ # Scripts running on Raspberry Pi
├─ backend/ # Python backend (FastAPI / Flask)
├─ frontend/ # Angular dashboard
├─ docs/ # Documentation and architecture
└─ tests/ # Unit tests or simulations


