# Agronomic rules for combining irrigation + disease outputs

FUNGAL_DISEASES = [
    'Apple — Apple Scab', 'Apple — Cedar Apple Rust',
    'Cherry — Powdery Mildew', 'Corn (Maize) — Cercospora Leaf Spot',
    'Corn (Maize) — Northern Leaf Blight', 'Grape — Black Rot',
    'Grape — Esca (Black Measles)', 'Grape — Leaf Blight',
    'Potato — Early Blight', 'Potato — Late Blight',
    'Strawberry — Leaf Scorch', 'Tomato — Early Blight',
    'Tomato — Late Blight', 'Tomato — Septoria Leaf Spot',
    'Tomato — Yellow Leaf Curl Virus',
]

BACTERIAL_DISEASES = [
    'Apple — Black Rot', 'Bell Pepper — Bacterial Spot',
    'Corn (Maize) — Common Rust', 'Peach — Bacterial Spot',
    'Tomato — Bacterial Spot',
]

HEALTHY_CLASSES = [
    'Apple — Healthy', 'Bell Pepper — Healthy', 'Cherry — Healthy',
    'Corn (Maize) — Healthy', 'Grape — Healthy', 'Peach — Healthy',
    'Potato — Healthy', 'Strawberry — Healthy', 'Tomato — Healthy',
]

DISEASE_TREATMENTS = {
    'Apple — Apple Scab':                  'Apply captan or myclobutanil fungicide. Remove infected leaves.',
    'Apple — Black Rot':                   'Prune infected branches. Apply copper-based bactericide.',
    'Apple — Cedar Apple Rust':            'Apply fungicide at bud break. Remove nearby cedar trees if possible.',
    'Bell Pepper — Bacterial Spot':        'Apply copper-based spray. Avoid overhead irrigation.',
    'Cherry — Powdery Mildew':             'Apply sulfur-based fungicide. Improve air circulation.',
    'Corn (Maize) — Cercospora Leaf Spot': 'Apply strobilurin fungicide. Rotate crops next season.',
    'Corn (Maize) — Common Rust':          'Apply propiconazole fungicide if severe. Monitor spread.',
    'Corn (Maize) — Northern Leaf Blight': 'Apply fungicide at early stages. Use resistant varieties next season.',
    'Grape — Black Rot':                   'Apply mancozeb or myclobutanil. Remove mummified berries.',
    'Grape — Esca (Black Measles)':        'No cure — remove and destroy infected wood. Apply wound sealant.',
    'Grape — Leaf Blight':                 'Apply copper fungicide. Improve canopy ventilation.',
    'Peach — Bacterial Spot':              'Apply copper spray during dormancy. Avoid wetting foliage.',
    'Potato — Early Blight':               'Apply chlorothalonil fungicide. Remove lower infected leaves.',
    'Potato — Late Blight':                'Apply mancozeb immediately. Destroy infected plants.',
    'Strawberry — Leaf Scorch':            'Apply myclobutanil fungicide. Remove infected leaves.',
    'Tomato — Bacterial Spot':             'Apply copper bactericide. Use disease-free seeds next season.',
    'Tomato — Early Blight':               'Apply chlorothalonil. Mulch around base to prevent soil splash.',
    'Tomato — Late Blight':                'Apply mancozeb or chlorothalonil immediately. High spread risk.',
    'Tomato — Septoria Leaf Spot':         'Apply fungicide. Remove lower leaves. Avoid overhead watering.',
    'Tomato — Yellow Leaf Curl Virus':     'No cure — remove infected plants. Control whitefly vectors.',
}

IRRIGATION_AMOUNTS = {'Low': 15, 'Medium': 30, 'High': 50}

def get_disease_type(disease_class):
    if disease_class in HEALTHY_CLASSES:   return 'healthy'
    elif disease_class in FUNGAL_DISEASES: return 'fungal'
    elif disease_class in BACTERIAL_DISEASES: return 'bacterial'
    else: return 'unknown'

def get_severity(disease_class, confidence, irrigation_need):
    if disease_class in HEALTHY_CLASSES:
        return 'MEDIUM' if irrigation_need == 'High' else 'LOW'
    if confidence >= 0.90:
        return 'CRITICAL' if irrigation_need == 'High' else 'HIGH'
    elif confidence >= 0.70: return 'MEDIUM'
    else: return 'LOW'
    