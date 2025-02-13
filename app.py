import streamlit as st
import math
import numpy as np

# Dropdown to select Horizontal or Vertical
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
        centripetal_force = calculate_centripetal_force(mass, velocity, radius)
        st.write(f"Centripetal Force: **{centripetal_force:.2f} N**")

    elif calculation_option == "Centripetal Acceleration":
        centripetal_acceleration = calculate_centripetal_acceleration(velocity, radius)
        st.write(f"Centripetal Acceleration: **{centripetal_acceleration:.2f} m/s²**")

    elif calculation_option == "Gravitational Force":
        gravitational_force = calculate_gravitational_force(mass)
        st.write(f"Gravitational Force: **{gravitational_force:.2f} N**")

    elif calculation_option == "Normal Force":
        if "Banked" in case_option:
            normal_force = calculate_normal_force(mass, angle)
        else:
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
        radius = st.sidebar.number_input("Radius (m)", min_value=0.1, value=5.0)
        velocity = st.sidebar.number_input("Tangential Velocity (m/s)", min_value=0.0, value=5.0)
        acceleration = calculate_centripetal_acceleration(velocity, radius)
        st.write(f"Centripetal Acceleration: {acceleration:.2f} m/s²")

    # Continue with other calculations as per the original code for Vertical...

