import streamlit as st
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO
import math
import numpy as np
import plotly.graph_objects as go

# Load and display the image from GitHub
image_url = "https://github.com/kolbm/UCM/blob/main/title.jpg"  # Replace with actual URL
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
    st.warning("Failed to load the image. Please check the URL.")

# Dropdown for selecting Horizontal or Vertical mode
app_option = st.sidebar.selectbox("Choose App Mode:", ["Horizontal Circular Motion", "Vertical Loop Motion"])

if app_option == "Horizontal Circular Motion":
    st.title("Horizontal Circular Motion Calculator")

    def calculate_centripetal_force(mass, velocity, radius):
        return mass * velocity**2 / radius

    def calculate_centripetal_acceleration(velocity, radius):
        return velocity**2 / radius

    # Sidebar inputs for Horizontal Motion
    mass = st.sidebar.number_input("Mass (kg)", min_value=0.1, value=1000.0)
    radius = st.sidebar.number_input("Radius of the curve (m)", min_value=1.0, value=50.0)
    velocity = st.sidebar.number_input("Velocity (m/s)", min_value=1.0, value=30.0)

    # Plot: Centripetal Force vs Velocity
    def plot_centripetal_force_vs_velocity(mass, radius):
        velocities = np.linspace(0, 50, 100)
        forces = mass * velocities**2 / radius
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=velocities, y=forces, mode='lines', name='Centripetal Force'))
        fig.update_layout(
            title="Centripetal Force vs. Velocity",
            xaxis_title="Velocity (m/s)",
            yaxis_title="Centripetal Force (N)",
            template="plotly_white"
        )
        st.plotly_chart(fig)

    st.subheader("Centripetal Force vs. Velocity Plot")
    plot_centripetal_force_vs_velocity(mass, radius)

    # Display results for calculations
    st.subheader("Calculation Results")
    centripetal_force = calculate_centripetal_force(mass, velocity, radius)
    centripetal_acceleration = calculate_centripetal_acceleration(velocity, radius)
    st.write(f"Centripetal Force: **{centripetal_force:.2f} N**")
    st.write(f"Centripetal Acceleration: **{centripetal_acceleration:.2f} m/s²**")

elif app_option == "Vertical Loop Motion":
    st.title("Vertical Loop Motion Calculator")

    def calculate_centripetal_force(mass, velocity, radius):
        return mass * velocity**2 / radius

    # Sidebar inputs for Vertical Loop Motion
    mass = st.sidebar.number_input("Mass (kg)", min_value=0.1, value=1.0)
    radius = st.sidebar.number_input("Radius of the loop (m)", min_value=0.1, value=5.0)
    velocity = st.sidebar.number_input("Velocity (m/s)", min_value=0.0, value=5.0)

    # Plot: Forces Around the Vertical Loop
    def plot_vertical_loop_forces(mass, radius, velocity):
        positions = np.linspace(0, 2 * np.pi, 100)
        normal_forces = mass * (velocity**2 / radius + 10 * np.cos(positions))
        gravitational_forces = mass * 10

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=positions, y=normal_forces, mode='lines', name='Normal Force'))
        fig.add_trace(go.Scatter(x=positions, y=np.full_like(positions, gravitational_forces), mode='lines', name='Gravitational Force'))
        fig.update_layout(
            title="Forces Around the Vertical Loop",
            xaxis_title="Position (radians)",
            yaxis_title="Force (N)",
            template="plotly_white"
        )
        st.plotly_chart(fig)

    st.subheader("Forces Around the Vertical Loop")
    plot_vertical_loop_forces(mass, radius, velocity)

    # Display results for calculations
    centripetal_force = calculate_centripetal_force(mass, velocity, radius)
    st.write(f"Centripetal Force: **{centripetal_force:.2f} N**")
