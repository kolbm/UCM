import streamlit as st
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO
import math
import numpy as np

# Load and display the image from GitHub
image_url = "https://raw.githubusercontent.com/kolbm/UCM/refs/heads/main/title.JPG"  # Replace with actual URL
response = requests.get(image_url)

st.sidebar.title("Circular Motion Calculator")

# Display the image above the dropdown
if response.status_code == 200:
    try:
        image = Image.open(BytesIO(response.content))
        st.image(image, caption="App Title", use_column_width=True)
    except UnidentifiedImageError:
        st.error("The image could not be loaded. Please check the file format.")
else:
    st.error("Failed to load the image. Please check the URL.")

# Dropdown for selecting Horizontal or Vertical mode
app_option = st.sidebar.selectbox("Choose App Mode:", ["Horizontal", "Vertical"])

if app_option == "Horizontal":
    st.title("Horizontal Circular Motion Calculator")

    # Function definitions for horizontal motion
    def calculate_centripetal_force(mass, velocity, radius):
        return mass * velocity**2 / radius

    def calculate_centripetal_acceleration(velocity, radius):
        return velocity**2 / radius

    def calculate_normal_force(mass, angle_deg, gravitational_acceleration=10):
        angle_rad = math.radians(angle_deg)
        return mass * gravitational_acceleration / math.cos(angle_rad)

    def calculate_gravitational_force(mass, gravitational_acceleration=10):
        return mass * gravitational_acceleration

    st.sidebar.header("Input Values")
    case_option = st.sidebar.selectbox(
        "Choose a scenario:",
        ["Banked without Friction (μ = 0, θ ≠ 0)", "Banked with Friction (μ ≠ 0, θ ≠ 0)", "Unbanked with Friction (μ ≠ 0, θ = 0)"]
    )

    mass = st.sidebar.number_input("Mass of the car (kg)", min_value=0.1, value=1000.0)
    radius = st.sidebar.number_input("Radius of the curve (m)", min_value=1.0, value=50.0)
    velocity = st.sidebar.number_input("Velocity of the car (m/s)", min_value=1.0, value=30.0)

    if case_option == "Banked without Friction (μ = 0, θ ≠ 0)":
        angle = st.sidebar.number_input("Angle of the banked curve (degrees)", min_value=0.0, max_value=90.0, value=30.0)

    elif case_option == "Banked with Friction (μ ≠ 0, θ ≠ 0)":
        angle = st.sidebar.number_input("Angle of the banked curve (degrees)", min_value=0.0, max_value=90.0, value=30.0)
        coefficient_of_friction = st.sidebar.number_input("Coefficient of Static Friction (μ_s)", min_value=0.0, value=0.5)

    elif case_option == "Unbanked with Friction (μ ≠ 0, θ = 0)":
        coefficient_of_friction = st.sidebar.number_input("Coefficient of Static Friction (μ_s)", min_value=0.0, value=0.5)

    calculation_option = st.sidebar.selectbox(
        "Select What to Calculate:",
        ["Centripetal Force", "Centripetal Acceleration", "Gravitational Force", "Normal Force"]
    )

    st.subheader(f"Results for: {case_option} - {calculation_option}")

    if calculation_option == "Centripetal Force":
        st.latex(r"F_c = \frac{m v^2}{r}")
        centripetal_force = calculate_centripetal_force(mass, velocity, radius)
        st.write(f"Centripetal Force: **{centripetal_force:.2f} N**")

    elif calculation_option == "Centripetal Acceleration":
        st.latex(r"a_c = \frac{v^2}{r}")
        centripetal_acceleration = calculate_centripetal_acceleration(velocity, radius)
        st.write(f"Centripetal Acceleration: **{centripetal_acceleration:.2f} m/s²**")

    elif calculation_option == "Gravitational Force":
        st.latex(r"F_g = m \cdot g")
        gravitational_force = calculate_gravitational_force(mass)
        st.write(f"Gravitational Force: **{gravitational_force:.2f} N**")

    elif calculation_option == "Normal Force":
        if "Banked" in case_option:
            st.latex(r"F_N = \frac{m \cdot g}{\cos(\theta)}")
            normal_force = calculate_normal_force(mass, angle)
        else:
            st.latex(r"F_N = m \cdot g")
            normal_force = calculate_gravitational_force(mass)
        st.write(f"Normal Force: **{normal_force:.2f} N**")

else:
    st.title("Vertical Loop Motion Calculator")

    def calculate_centripetal_acceleration(v, r):
        return v**2 / r

    def calculate_tangential_velocity(a, r):
        return np.sqrt(a * r)

    def calculate_radius(v, a):
        return v**2 / a

    def calculate_centripetal_force(m, v, r):
        return m * v**2 / r

    def calculate_gravitational_force(m, g=10):
        return m * g

    def calculate_normal_force_bottom(m, v, r, g=10):
        return m * (v**2 / r + g)

    def calculate_normal_force_top(m, v, r, g=10):
        return m * (v**2 / r - g)

    st.sidebar.header("Input Parameters")
    loop_position = st.sidebar.selectbox("Select Loop Position:", ["Top of the Loop", "Bottom of the Loop"])
    calculation_type = st.sidebar.selectbox(
        "What would you like to solve for:",
        ["Centripetal Acceleration", "Tangential Velocity", "Radius of the Loop", "Centripetal Force", "Normal/Tension Force", "Gravitational Force"]
    )

    if calculation_type == "Centripetal Acceleration":
        st.latex(r"a_c = \frac{v^2}{r}")
        radius = st.sidebar.number_input("Radius (m)", min_value=0.1, value=5.0)
        velocity = st.sidebar.number_input("Tangential Velocity (m/s)", min_value=0.0, value=5.0)
        acceleration = calculate_centripetal_acceleration(velocity, radius)
        st.write(f"Centripetal Acceleration: {acceleration:.2f} m/s²")

    elif calculation_type == "Tangential Velocity":
        st.latex(r"v_T = \sqrt{a_c \cdot r}")
        acceleration = st.sidebar.number_input("Centripetal Acceleration (m/s²)", min_value=0.1, value=5.0)
        radius = st.sidebar.number_input("Radius (m)", min_value=0.1, value=5.0)
        velocity = calculate_tangential_velocity(acceleration, radius)
        st.write(f"Tangential Velocity: {velocity:.2f} m/s")

    elif calculation_type == "Radius of the Loop":
        st.latex(r"r = \frac{v^2}{a_c}")
        velocity = st.sidebar.number_input("Tangential Velocity (m/s)", min_value=0.0, value=5.0)
        acceleration = st.sidebar.number_input("Centripetal Acceleration (m/s²)", min_value=0.1, value=5.0)
        radius = calculate_radius(velocity, acceleration)
        st.write(f"Radius of the Loop: {radius:.2f} m")
