import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import ipywidgets as widgets
from IPython.display import display

# --- Bloch vector conversion ---
def bloch_vector(theta, phi):
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    return np.array([x, y, z])

# --- Plotting function ---
def plot_bloch_sphere(vec_a, vec_b, label_b):
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Bloch sphere
    u, v = np.mgrid[0:2*np.pi:100j, 0:np.pi:100j]
    x = np.cos(u) * np.sin(v)
    y = np.sin(u) * np.sin(v)
    z = np.cos(v)
    ax.plot_surface(x, y, z, color='lightblue', alpha=0.1)

    # Axes
    for axis in [(1,0,0), (0,1,0), (0,0,1)]:
        ax.quiver(0, 0, 0, *axis, color='gray', linewidth=0.5)

    # Vectors
    ax.quiver(0, 0, 0, *vec_a, color='blue', linewidth=2)
    ax.text(*vec_a * 1.1, '|0⟩', color='blue', fontsize=12)

    ax.quiver(0, 0, 0, *vec_b, color='red', linewidth=2)
    ax.text(*vec_b * 1.1, label_b, color='red', fontsize=12)

    # Angle cosine
    cos_angle = np.dot(vec_a, vec_b)
    ax.set_title(f'Inner Product ⟨0|ψ⟩ ≈ {cos_angle:.2f}', fontsize=14)

    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.tight_layout()
    plt.show()

# --- Main interactive logic ---
theta_slider = widgets.FloatSlider(value=60, min=0, max=180, step=1, description='θ (deg)')
phi_slider = widgets.FloatSlider(value=45, min=0, max=360, step=1, description='ϕ (deg)')
state_label = widgets.Label(value='|ψ⟩')

def update_plot(theta_deg, phi_deg):
    theta = np.deg2rad(theta_deg)
    phi = np.deg2rad(phi_deg)
    vec_a = bloch_vector(0, 0)  # |0⟩
    vec_b = bloch_vector(theta, phi)
    plot_bloch_sphere(vec_a, vec_b, state_label.value)

# --- Preset state handlers ---
preset_buttons = widgets.ToggleButtons(
    options=[
        ('|0⟩', (0, 0)),
        ('|1⟩', (180, 0)),
        ('|+⟩', (90, 0)),
        ('|–⟩', (90, 180)),
        ('|i⟩', (90, 90)),
        ('|–i⟩', (90, 270))
    ],
    description='Presets:',
    button_style=''
)

def on_preset_change(change):
    if change['name'] == 'value':
        label, (θ, φ) = change['new']
        theta_slider.value = θ
        phi_slider.value = φ
        state_label.value = label

preset_buttons.observe(on_preset_change, names='value')

# --- Display ---
ui = widgets.VBox([
    preset_buttons,
    theta_slider,
    phi_slider
])
out = widgets.interactive_output(update_plot, {
    'theta_deg': theta_slider,
    'phi_deg': phi_slider
})

display(ui, out)
