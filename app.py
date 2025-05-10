
import streamlit as st
from PIL import Image
import plotly.graph_objects as go
import numpy as np

st.title("Longfeather's Minecraft Block Simulator")

uploaded_file = st.file_uploader("Upload a block texture (square image)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Load texture image
    img = Image.open(uploaded_file).convert("RGB")
    img = img.resize((128, 128))  # resize for performance

    # Convert image to NumPy
    img_np = np.asarray(img)

    # Create a cube with textured faces
    fig = go.Figure()

    def textured_face(x, y, z):
        fig.add_trace(go.Surface(
            x=x, y=y, z=z,
            surfacecolor=np.zeros_like(img_np[:, :, 0]),
            cmin=0, cmax=1,
            colorscale=[[0, f'rgb({c[0]},{c[1]},{c[2]})'] for c in img_np[::8, ::8].reshape(-1, 3)],
            showscale=False
        ))

    # Define cube surfaces (3 visible faces)
    x = np.array([[0, 0], [1, 1]])
    y = np.array([[0, 1], [0, 1]])
    z = np.array([[0, 0], [0, 0]])
    textured_face(x, y, z)  # front

    z += 1
    textured_face(x, y, z)  # top

    y += 1
    textured_face(x, y, z)  # side

    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
        ),
        margin=dict(l=0, r=0, t=0, b=0)
    )

    st.plotly_chart(fig, use_container_width=True)
