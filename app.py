import streamlit as st
from PIL import Image
import plotly.graph_objects as go
import numpy as np

st.title("Longfeather's Simulatorium Cubed - Custom Textures")

mode = st.radio("Texture mode:", ["Single texture (all sides)", "One texture per face"])

@st.cache_data(show_spinner=False)
def preprocess_image(file):
    img = Image.open(file).convert("RGB")
    return np.array(img.resize((64, 64))) / 255.0

def load_texture(label):
    file = st.file_uploader(f"Upload {label} face texture", type=["png", "jpg", "jpeg"], key=label)
    return preprocess_image(file) if file else None

faces = ["Front", "Back", "Top", "Bottom", "Left", "Right"]
textures = {}

if mode == "Single texture (all sides)":
    tex = load_texture("All")
    if tex is not None:
        textures = {face: tex for face in faces}
elif mode == "One texture per face":
    textures = {face: load_texture(face) for face in faces}

def make_face(x0, x1, y0, y1, z0, z1, axis='z', res=64):
    rng = np.linspace(0, 1, res)
    X, Y = np.meshgrid(rng, rng)
    X = x0 + (x1 - x0) * X
    Y = y0 + (y1 - y0) * Y
    Z = z0 + (z1 - z0) * np.ones_like(X)
    return (X, Y, Z) if axis == 'z' else (X, Z, Y) if axis == 'y' else (Z, X, Y)

if all(texture is not None for texture in textures.values()):
    fig = go.Figure()
    face_specs = [
        ("Front", make_face(0, 1, 0, 1, 0, 0, 'z')),
        ("Back", make_face(0, 1, 0, 1, 1, 1, 'z')),
        ("Top", make_face(0, 1, 1, 1, 0, 1, 'y')),
        ("Bottom", make_face(0, 1, 0, 0, 0, 1, 'y')),
        ("Left", make_face(0, 0, 0, 1, 0, 1, 'x')),
        ("Right", make_face(1, 1, 0, 1, 0, 1, 'x')),
    ]

    for i, (name, (x, y, z)) in enumerate(face_specs):
        tex = textures[name][:, :, i % 3]  # Use R, G, B channels cyclically
        fig.add_trace(go.Surface(
            x=x, y=y, z=z,
            surfacecolor=np.flipud(tex),
            cmin=0, cmax=1,
            colorscale="gray",
            showscale=False
        ))

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
img.resize((64, 64))
        return np.array(img) / 255.0
    return None

textures = {}

if mode == "Single texture (all sides)":
    texture = load_texture("All")
    if texture is not None:
        for face in ["Front", "Back", "Top", "Bottom", "Left", "Right"]:
            textures[face] = texture
elif mode == "One texture per face":
    for face in ["Front", "Back", "Top", "Bottom", "Left", "Right"]:
        textures[face] = load_texture(face)

if all(v is not None for v in textures.values()):
    def make_face(x0, x1, y0, y1, z0, z1, axis='z'):
        res = 64
        rng = np.linspace(0, 1, res)
        X, Y = np.meshgrid(rng, rng)
        X = x0 + (x1 - x0) * X
        Y = y0 + (y1 - y0) * Y
        Z = z0 + (z1 - z0) * np.ones_like(X)

        if axis == 'z':
            return X, Y, Z
        elif axis == 'y':
            return X, Z, Y
        elif axis == 'x':
            return Z, X, Y

    fig = go.Figure()
    faces = [
        ("Front", make_face(0, 1, 0, 1, 0, 0, 'z')),
        ("Back", make_face(0, 1, 0, 1, 1, 1, 'z')),
        ("Top", make_face(0, 1, 1, 1, 0, 1, 'y')),
        ("Bottom", make_face(0, 1, 0, 0, 0, 1, 'y')),
        ("Left", make_face(0, 0, 0, 1, 0, 1, 'x')),
        ("Right", make_face(1, 1, 0, 1, 0, 1, 'x')),
    ]

    for i, (name, (x, y, z)) in enumerate(faces):
        tex = textures[name]
        channel = tex[:, :, i % 3]
        fig.add_trace(go.Surface(
            x=x, y=y, z=z,
            surfacecolor=np.flipud(channel),
            cmin=0, cmax=1,
            colorscale="gray",
            showscale=False
        ))

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
