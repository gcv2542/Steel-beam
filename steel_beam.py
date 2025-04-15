import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Streamlit page config
st.set_page_config(page_title="Steel Beam Designer AI", page_icon="🧱")
st.title("🧱 Steel Beam Design Calculator")

# Sidebar for input
st.sidebar.header("Input Parameters")
span = st.sidebar.number_input("Span (m)", min_value=1.0, step=0.5)
load_type = st.sidebar.selectbox("Load Type", ["Uniformly Distributed Load (UDL)", "Point Load"])
load_value = st.sidebar.number_input("Load Magnitude (kN or kN/m)", min_value=0.0, step=1.0)
material = st.sidebar.selectbox("Material Grade", ["A36", "A992"])
modulus_elasticity = 200_000  # MPa (assumed same for both for simplicity)

# Material yield strength (MPa)
fy_values = {"A36": 250, "A992": 345}
fy = fy_values[material]

# Perform calculations
if st.button("Calculate Design"):
    st.subheader("Design Summary")
    
    if load_type == "Uniformly Distributed Load (UDL)":
        w = load_value * 1e3  # Convert kN/m to N/m
        M_max = (w * (span**2)) / 8  # Nm
        V_max = (w * span) / 2       # N
    else:
        P = load_value * 1e3  # Convert kN to N
        M_max = (P * span) / 4
        V_max = P / 2

    phi = 0.9  # resistance factor
    S_required = M_max / (phi * fy * 1e6)  # m^3
    S_required_mm3 = S_required * 1e9      # mm^3

    st.write(f"**Maximum Bending Moment:** {M_max/1e3:.2f} kNm")
    st.write(f"**Maximum Shear Force:** {V_max/1e3:.2f} kN")
    st.write(f"**Required Section Modulus:** {S_required_mm3:.2f} mm³")
    
    st.info("Compare this with standard W-sections from AISC Manual.")

    # Diagrams (optional)
    fig, ax = plt.subplots()
    x = np.linspace(0, span, 100)
    if load_type == "Uniformly Distributed Load (UDL)":
        moment = w * x * (span - x) / 2
    else:
        moment = np.where(x <= span/2, P * x / 2, P * (span - x) / 2)
    ax.plot(x, moment/1e3, label="Bending Moment (kNm)", color='blue')
    ax.set_xlabel("Beam Length (m)")
    ax.set_ylabel("Moment (kNm)")
    ax.grid(True)
    st.pyplot(fig)

    st.success("Design calculation completed.")

st.markdown("---")
st.caption("Developed by ChatGPT for structural engineering tasks.")



            