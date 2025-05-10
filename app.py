
import streamlit as st
from PIL import Image
import plotly.graph_objects as go
import numpy as np

st.title("Longfeather's Minecraft Block Simulatorium")

uploaded_file = st.file_uploader("Upload a thingy (square PNG or JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    img = img.resize((64, 64))  # Resize for consistency

    st.image(img, caption="Uploaded Texture", use_column_width=False)

    # Normalize texture
    img_np = np.array(img) / 255.0

    # Create 3D surface texture map for 3 cube faces
    def make_face(x0, x1, y0, y1, z, axis='z'):
        X, Y = np.meshgrid(np.linspace(x0, x1, img_np.shape[1]), np.linspace(y0, y1, img_np.shape[0]))
        Z = np.full_like(X, z)
        if axis == 'z':
            return X, Y, Z
        elif axis == 'y':
            return X, Z, Y
        elif axis == 'x':
            return Z, X, Y

    fig = go.Figure()

    # Front face (z = 0)
    x, y, z = make_face(0, 1, 0, 1, 0, axis='z')
    fig.add_trace(go.Surface(x=x, y=y, z=z, surfacecolor=np.flipud(img_np[:, :, 0]), cmin=0, cmax=1,
                             colorscale="gray", showscale=False))

    # Top face (y = 1)
    x, y, z = make_face(0, 1, 0, 1, 1, axis='y')
    fig.add_trace(go.Surface(x=x, y=y, z=z, surfacecolor=np.flipud(img_np[:, :, 1]), cmin=0, cmax=1,
                             colorscale="gray", showscale=False))

    # Right face (x = 1)
    x, y, z = make_face(0, 1, 0, 1, 1, axis='x')
    fig.add_trace(go.Surface(x=x, y=y, z=z, surfacecolor=np.flipud(img_np[:, :, 2]), cmin=0, cmax=1,
                             colorscale="gray", showscale=False))

    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode="cube"
        ),
        margin=dict(l=0, r=0, t=0, b=0),
    )

    st.plotly_chart(fig, use_container_width=True)
