import streamlit as st
import schemdraw
import schemdraw.elements as elm

st.set_page_config(layout="wide")

st.title("Simulador interactivo de circuitos eléctricos")

st.write(
    "Bienvenido al Simulador interactivo de circuitos eléctricos! "
    "Esta aplicacion permite construir y experimentar con un circuito eléctrico simple. "
    "Podés ajustar los valores de los componentes y ver como se comporta el circuito en tiempo real. "
    "El objetivo es aprender los fundamentos de circuitos eléctricos de manera interactiva."
)

st.header("Parámetros del circuito")

col1, col2 = st.columns(2)

max_pS = 2.0
r1 = 100.0
r2 = 200.0
max_p3 = 5.0

with col1:
    voltage = st.slider(f"Fuente de tensión variable (V), potencia máxima {max_pS} (W)", min_value=0.0, max_value=50.0, value=12.0, step=0.1)
    r3 = st.slider("Resistencia Variable (Ω)", min_value=0.0, max_value=1000.0, value=300.0)
with col2:
    max_p1 = st.slider(f"Resistor 1 {r1} Ω, Potencia máxima tolerada V * I (W)", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
    max_p2 = st.slider(f"Resistor 2 {r2} Ω, Potencia máxima tolerada V * I (W)", min_value=0.0, max_value=10.0, value=2.0, step=0.1)

total_resistance = (r1 + r2 + r3)
# To prevent division by zero if all resistances are 0
try:
    total_current = voltage / total_resistance
except Exception as e:
    total_current = (max_pS / voltage) * 100.0 # Short circuit current

v1 = total_current * r1
v2 = total_current * r2
v3 = total_current * r3

pS = voltage * total_current
p1 = v1 * total_current
p2 = v2 * total_current
p3 = v3 * total_current

st.header("Datos en tiempo real")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Corriente total", f"{total_current:.2f} A")
    st.metric("Potencia entregada", f"{pS:.2f} W")

with col2:
    st.metric("Caída de tensión R1", f"{v1:.2f} V")
    st.metric("Caída de tensión R2", f"{v2:.2f} V")
    st.metric("Caída de tensión R3", f"{v3:.2f} V")

with col3:
    st.metric("Disipación de potencia R1", f"{p1:.2f} W")
    st.metric("Disipación de potencia R2", f"{p2:.2f} W")
    st.metric("Disipación de potencia R3", f"{p3:.2f} W")

with col4:
    schemdraw.theme('oceans16')
    with schemdraw.Drawing() as d:
        d.config(unit=4)
        d += elm.SourceV().label(f'{voltage}V').color('red' if pS > max_pS else 'black')
        d += elm.Resistor().right().label(f'{r1}Ω').color('red' if p1 > max_p1 else 'black')
        d += elm.Resistor().down().label(f'{r2}Ω').color('red' if p2 > max_p2 else 'black')
        d += elm.Resistor().left().label(f'{r3}Ω').color('red' if p3 > max_p3 else 'black')
        d += elm.Line().up().to((0,0))

        # Get the SVG data from the drawing
        svg_data = d.get_imagedata('svg')

        # Decode the SVG bytes into a string before displaying
        st.image(svg_data.decode("utf-8"), caption="Circuito de corriente continua", width="content")
