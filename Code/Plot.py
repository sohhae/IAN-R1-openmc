import openmc

# ===== Ventanas y tamaños coherentes con tu modelo =====
POOL_RADIUS        = 100.0   # cm
REFLECTOR_XY_HALF  = 30.0    # cm
REFLECTOR_HEIGHT   = 80.0    # cm

# ===== Corte XY a una z donde TODAS las CR tengan B4C =====
Z_PLOT = 35.0  # cm (ajusta si cambias inserciones)

# --- Cargar materiales desde materials.xml para poder colorear por material ---
mats = openmc.Materials.from_xml()  # requiere materials.xml generado por tu main

def find_mat(name_substr: str):
    """Devuelve el material cuyo nombre contiene name_substr (case-insensitive)."""
    s = name_substr.lower()
    for m in mats:
        if m.name and s in m.name.lower():
            return m
    return None

# Intentar encontrar por nombre tal como los defines en tu main:
m_h2o      = find_mat("Light water") or find_mat("water")
m_air      = find_mat("Air")
m_fuel     = find_mat("TRIGA fuel")
m_b4c      = find_mat("B4C")
m_ss304    = find_mat("Stainless Steel")
m_graphite = find_mat("Graphite")
m_concrete = find_mat("Concrete")

# Diccionario de colores por material (RGB 0-255)
mat_colors = {}
if m_h2o:      mat_colors[m_h2o]      = (150, 200, 255)  # agua (celeste)
if m_air:      mat_colors[m_air]      = (235, 235, 235)  # **aire (gris muy claro, CONTRASTE con agua)**
if m_fuel:     mat_colors[m_fuel]     = (255, 160,   0)  # combustible (naranja)
if m_b4c:      mat_colors[m_b4c]      = ( 20,  20,  20)  # B4C (negro)
if m_ss304:    mat_colors[m_ss304]    = (175, 175, 175)  # acero 304 (gris)
if m_graphite: mat_colors[m_graphite] = (120, 120, 120)  # grafito
if m_concrete: mat_colors[m_concrete] = (210, 180, 140)  # concreto

plots = []

# 1) Vista completa de la piscina (XY) en Z_PLOT
p_pool = openmc.Plot()
p_pool.filename = "pool_xy"
p_pool.basis    = "xy"
p_pool.width    = (2*POOL_RADIUS, 2*POOL_RADIUS)
p_pool.pixels   = (1200, 1200)
p_pool.level    = 0
p_pool.origin   = (0.0, 0.0, Z_PLOT)
p_pool.color_by = "material"
if mat_colors:  # solo si encontramos materiales
    p_pool.colors = mat_colors
plots.append(p_pool)

# 2) Zoom del bloque/núcleo (XY) en Z_PLOT
p_core = openmc.Plot()
p_core.filename = "core_xy"
p_core.basis    = "xy"
p_core.width    = (2*REFLECTOR_XY_HALF*1.10, 2*REFLECTOR_XY_HALF*1.10)  # 10% margen
p_core.pixels   = (1400, 1400)
p_core.level    = 0
p_core.origin   = (0.0, 0.0, Z_PLOT)
p_core.color_by = "material"
if mat_colors:
    p_core.colors = mat_colors
plots.append(p_core)

# 3) Corte lateral XZ del bloque
p_xz = openmc.Plot()
p_xz.filename = "core_xz"
p_xz.basis    = "xz"
p_xz.width    = (2*REFLECTOR_XY_HALF*1.10, REFLECTOR_HEIGHT*1.10)
p_xz.pixels   = (1400, 1400)
p_xz.level    = 0
p_xz.origin   = (0.0, 0.0, 0.0)
p_xz.color_by = "material"
if mat_colors:
    p_xz.colors = mat_colors
plots.append(p_xz)


p_yz = openmc.Plot()
p_yz.filename = "core_yz"
p_yz.basis    = "yz"
p_yz.width    = (2*REFLECTOR_XY_HALF*1.10, REFLECTOR_HEIGHT*1.10)
p_yz.pixels   = (1400, 1400)
p_yz.level    = 0
p_yz.origin   = (0.0, 0.0, 0.0)
p_yz.color_by = "material"
if mat_colors:
    p_yz.colors = mat_colors
plots.append(p_yz)


openmc.Plots(plots).export_to_xml()
openmc.plot_geometry()

print("✅ Generado: pool_xy.png, core_xy.png, core_xz.png, core_yz.png")
print(f"   (corte XY en z = {Z_PLOT} cm; aire coloreado en gris muy claro)")
