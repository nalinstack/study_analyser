import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="CrashGuard Dashboard",
    page_icon="🚗",
    layout="wide",
)

# ---------------- AUTO REFRESH ----------------
st_autorefresh(interval=3000, limit=None, key="dashboard_refresh")

# ---------------- CUSTOM CSS ----------------
st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(135deg, #0f172a, #111827, #1e293b);
            color: white;
        }

        .main-title {
            font-size: 2.7rem;
            font-weight: 800;
            color: #f8fafc;
            margin-bottom: 0.2rem;
        }

        .subtitle {
            font-size: 1rem;
            color: #94a3b8;
            margin-bottom: 1.5rem;
        }

        .card {
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.25);
            backdrop-filter: blur(10px);
            margin-bottom: 20px;
        }

        .metric-title {
            font-size: 0.95rem;
            color: #cbd5e1;
            margin-bottom: 5px;
        }

        .metric-value {
            font-size: 1.7rem;
            font-weight: 700;
            color: #ffffff;
        }

        .status-safe {
            padding: 12px 18px;
            border-radius: 14px;
            background: rgba(34,197,94,0.15);
            border: 1px solid rgba(34,197,94,0.4);
            color: #bbf7d0;
            font-weight: 700;
            text-align: center;
            font-size: 1.05rem;
        }

        .status-alert {
            padding: 12px 18px;
            border-radius: 14px;
            background: rgba(239,68,68,0.16);
            border: 1px solid rgba(239,68,68,0.45);
            color: #fecaca;
            font-weight: 700;
            text-align: center;
            font-size: 1.05rem;
        }

        .small-note {
            color: #94a3b8;
            font-size: 0.9rem;
        }

        .footer-text {
            text-align: center;
            color: #94a3b8;
            margin-top: 20px;
            font-size: 0.9rem;
        }

        div.stButton > button {
            border-radius: 12px;
            border: none;
            padding: 0.65rem 1rem;
            font-weight: 700;
            background: linear-gradient(90deg, #2563eb, #7c3aed);
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- HEADER ----------------
st.markdown('<div class="main-title">🚗 CrashGuard Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Real-time IoT accident detection and emergency response monitoring system</div>',
    unsafe_allow_html=True,
)

# ---------------- BACKEND API ----------------
backend_url = "http://127.0.0.1:5000/latest-alert"

default_data = {
    "status": "Safe",
    "latitude": 13.0827,
    "longitude": 80.2707,
    "vehicle_id": "CG-101",
    "last_update": "Live",
    "severity": "Low"
}

try:
    response = requests.get(backend_url, timeout=3)
    if response.status_code == 200:
        data = response.json()
    else:
        data = default_data
except Exception:
    data = default_data

status = data.get("status", "Safe")
latitude = data.get("latitude", 13.0827)
longitude = data.get("longitude", 80.2707)
vehicle_id = data.get("vehicle_id", "CG-101")
last_update = data.get("last_update", "Live")
severity = data.get("severity", "Low")

maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"

# ---------------- TOP METRICS ----------------
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(
        f"""
        <div class="card">
            <div class="metric-title">Vehicle ID</div>
            <div class="metric-value">{vehicle_id}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m2:
    st.markdown(
        f"""
        <div class="card">
            <div class="metric-title">System Update</div>
            <div class="metric-value">{last_update}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m3:
    st.markdown(
        f"""
        <div class="card">
            <div class="metric-title">Severity</div>
            <div class="metric-value">{severity}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m4:
    system_state = "ACTIVE" if status != "Safe" else "MONITORING"
    st.markdown(
        f"""
        <div class="card">
            <div class="metric-title">Mode</div>
            <div class="metric-value">{system_state}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------- MAIN LAYOUT ----------------
left, right = st.columns([1.1, 1.2])

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("System Status")

    if status.lower() == "safe":
        st.markdown('<div class="status-safe">✅ No Accident Detected</div>', unsafe_allow_html=True)
        st.markdown("<p class='small-note'>Vehicle conditions are normal and continuously monitored.</p>", unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-alert">🚨 Accident Detected</div>', unsafe_allow_html=True)
        st.markdown("<p class='small-note'>Emergency alert triggered and sent to the backend monitoring system.</p>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Alert Information")
    st.write(f"**Status:** {status}")
    st.write(f"**Latitude:** {latitude}")
    st.write(f"**Longitude:** {longitude}")
    st.write(f"**Severity:** {severity}")

    st.link_button("📍 Open in Google Maps", maps_link)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("System Summary")
    st.write("- MPU6050 monitors motion, tilt, and impact conditions.")
    st.write("- GPS provides the live accident location.")
    st.write("- Backend processes alerts and updates dashboard.")
    st.write("- Cloud integration can trigger SMS alerts.")
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📍 Live Location")
    st.map({"lat": [latitude], "lon": [longitude]})
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Recent Alert Log")
    st.dataframe(
        [
            {
                "Vehicle ID": vehicle_id,
                "Status": status,
                "Severity": severity,
                "Latitude": latitude,
                "Longitude": longitude,
                "Update": last_update,
            }
        ],
        use_container_width=True,
        hide_index=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- MANUAL DEMO CONTROLS ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("Demo Controls")
st.caption("Use this section only for hackathon demonstration when backend/hardware is unavailable.")

demo_col1, demo_col2 = st.columns(2)

with demo_col1:
    st.info("The current dashboard primarily reads from the backend API.")

with demo_col2:
    st.success("UI is ready for integration with Member 2 backend and Member 1 ESP32 data flow.")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown(
    '<div class="footer-text">CrashGuard • IoT-Based Smart Accident Detection and Emergency Response System</div>',
    unsafe_allow_html=True,
)
