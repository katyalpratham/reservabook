from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
from reservabook_db import get_connection, ensure_schema

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

conn = get_connection()
ensure_schema(conn)

def _price_to_str(cents: int) -> str:
    return f"${cents/100:.0f}" if cents % 100 == 0 else f"${cents/100:.2f}"

@app.route("/api/services", methods=["GET"])
def services():
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT code, name, duration_min, price_cents FROM services ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    return jsonify([
        {
            "code": r["code"],
            "name": r["name"],
            "duration_min": r["duration_min"],
            "price": _price_to_str(r["price_cents"]),
        } for r in rows
    ])

@app.route("/api/slots", methods=["GET"])
def slots():
    # generate 30-min slots 09:00 - 17:00, minus existing bookings for date
    date_str = request.args.get("date")  # YYYY-MM-DD
    if not date_str:
        return jsonify({"error": "Missing date (YYYY-MM-DD)"}), 400
    try:
        day = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    # fetch booked times
    cur = conn.cursor()
    cur.execute("SELECT booking_time FROM bookings WHERE booking_date=%s", (date_str,))
    booked = {t for (t,) in cur.fetchall()}
    cur.close()

    start = day.replace(hour=9, minute=0)
    end = day.replace(hour=17, minute=0)
    out = []
    now = datetime.now()
    t = start
    while t <= end:
        label = t.strftime("%I:%M %p").lstrip("0")
        # disable past slots if same day
        is_past = (t < now and t.date() == now.date())
        if label not in booked:
            out.append({"time": label, "available": not is_past})
        t += timedelta(minutes=30)
    return jsonify(out)

@app.route("/api/bookings", methods=["POST"])
def create_booking():
    data = request.get_json(silent=True) or {}
    required = ["service", "date", "time", "first_name", "last_name", "email", "phone"]
    missing = [k for k in required if not data.get(k)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    # normalize
    try:
        date_obj = datetime.strptime(data["date"], "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date"}), 400

    cur = conn.cursor()
    # ensure service exists
    cur.execute("SELECT 1 FROM services WHERE code=%s", (data["service"],))
    if cur.fetchone() is None:
        cur.close()
        return jsonify({"error": "Unknown service"}), 400

    # ensure not double-booked
    cur.execute(
        "SELECT 1 FROM bookings WHERE booking_date=%s AND booking_time=%s",
        (date_obj.isoformat(), data["time"]),
    )
    if cur.fetchone() is not None:
        cur.close()
        return jsonify({"error": "Time slot already booked"}), 409

    cur.execute(
        """
        INSERT INTO bookings (service_code, booking_date, booking_time, first_name, last_name, email, phone, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            data["service"],
            date_obj.isoformat(),
            data["time"],
            data["first_name"].strip(),
            data["last_name"].strip(),
            data["email"].strip(),
            data["phone"].strip(),
            (data.get("notes") or "").strip() or None,
        ),
    )
    cur.execute("SELECT LAST_INSERT_ID()")
    (booking_id,) = cur.fetchone()
    cur.close()

    return jsonify({"message": "Booking confirmed", "booking_id": booking_id})

@app.route("/", methods=["GET"])
def health():
    return jsonify({
        "message": "Reservabook API running",
        "endpoints": ["GET /api/services", "GET /api/slots?date=YYYY-MM-DD", "POST /api/bookings"],
    })

if __name__ == "__main__":
    print("🚀 Reservabook backend starting on http://127.0.0.1:5500")
    app.run(host="127.0.0.1", port=5500, debug=True)


