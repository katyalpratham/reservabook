# 🛒 Grocery Store Management System

A full-stack web application for managing grocery store products with React frontend and Flask backend.

## 🚀 Quick Start

### Option 1: Automated Setup (Windows)
1. Double-click `start_project.bat`
2. Wait for both servers to start
3. Open your browser to `http://localhost:5173`

### Option 2: Manual Setup

#### Backend Setup
```bash
cd BACKEND
pip install -r requirements.txt
python test_server.py
```

#### Frontend Setup
```bash
cd FRONTEND
npm install
npm run dev
```

## 🌐 Access Points

- **Frontend**: http://localhost:5173
- **Backend API**: http://127.0.0.1:5000
- **API Documentation**: http://127.0.0.1:5000

### Reservabook (HTML + Flask)

- Run with: `run_reservabook.bat`
- HTML opens from your Desktop at `second.html`
- Backend: `http://127.0.0.1:5500`
- Endpoints:
  - `GET /api/services`
  - `GET /api/slots?date=YYYY-MM-DD`
  - `POST /api/bookings`

## 📊 Features

- ✅ View all products
- ✅ Add new products
- ✅ Edit existing products
- ✅ Delete products
- ✅ Real-time updates
- ✅ Responsive design

## 🔧 API Endpoints

- `GET /api/getproducts` - Get all products
- `POST /api/addproduct` - Add new product
- `PUT /api/updateproduct/<id>` - Update product
- `DELETE /api/deleteproduct/<id>` - Delete product

## 🛠️ Technology Stack

### Frontend
- React 19
- Vite
- Tailwind CSS
- Modern ES6+ JavaScript

### Backend
- Python Flask
- Flask-CORS
- MySQL Connector (for database version)

## 📝 Project Structure

```
Grocery Store Management System/
├── BACKEND/
│   ├── test_server.py          # Test server (no database required)
│   ├── server.py               # Production server (with database)
│   ├── products_dao.py         # Database operations
│   ├── sql_connection.py       # Database connection
│   └── requirements.txt        # Python dependencies
├── FRONTEND/
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── utils/             # API utilities
│   │   └── App.jsx            # Main app component
│   ├── package.json           # Node.js dependencies
│   └── vite.config.js         # Vite configuration
└── start_project.bat          # Windows startup script
```

## 🐛 Troubleshooting

### Backend Issues
- Make sure Python 3.7+ is installed
- Install dependencies: `pip install -r BACKEND/requirements.txt`
- Check if port 5000 is available

### MySQL Errors (Reservabook)

- Access denied for user 'root'@'localhost'
  - Ensure the password in `BACKEND/reservabook_db.py` is correct for your MySQL root user
  - Or create a dedicated user and update credentials accordingly

- Unknown database 'reservabook'
  - First run will auto-create the `reservabook` database and schema
  - If creation fails, ensure your MySQL user has `CREATE DATABASE` privilege

- Can't connect to MySQL server on '127.0.0.1:3306'
  - Make sure MySQL service is running (Windows Services → MySQL)
  - Verify port (default 3306); if different, update `reservabook_db.py`

- Table doesn't exist / missing schema
  - The server creates tables on startup via `ensure_schema`
  - Check backend logs for any SQL errors

### Frontend Issues
- Make sure Node.js 16+ is installed
- Install dependencies: `npm install` in FRONTEND folder
- Check if port 5173 is available

### Connection Issues
- Ensure backend is running on port 5000
- Check browser console for errors
- Verify proxy configuration in `vite.config.js`

## 🔄 Development Modes

### Backend Mode
- Uses `server.py` (database-backed)
- Requires MySQL database `gs`
- Configure credentials in `BACKEND/sql_connection.py`

## 📞 Support

If you encounter any issues:
1. Check the console output for error messages
2. Verify all dependencies are installed
3. Ensure ports 5000 and 5173 are available
4. Try restarting both servers

---

**Happy Coding! 🎉**



