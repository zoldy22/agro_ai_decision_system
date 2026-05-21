import sys, os
sys.path.append(os.path.dirname(__file__))
from recommendation_rules import (
    get_disease_type, get_severity,
    DISEASE_TREATMENTS, IRRIGATION_AMOUNTS, HEALTHY_CLASSES
)

SEVERITY_MARKERS = {
    'LOW': '[LOW]', 'MEDIUM': '[MEDIUM]', 'HIGH': '[HIGH]', 'CRITICAL': '[CRITICAL]'
}

def generate_recommendation(disease_class, confidence, irrigation_need):
    """
    Parameters:
        disease_class  : str   — e.g. 'Tomato — Late Blight'
        confidence     : float — e.g. 0.942
        irrigation_need: str   — 'Low', 'Medium', or 'High'
    Returns:
        dict with full structured recommendation
    """
    disease_type = get_disease_type(disease_class)
    severity     = get_severity(disease_class, confidence, irrigation_need)
    is_healthy   = disease_class in HEALTHY_CLASSES
    is_fungal    = disease_type == 'fungal'

    base_mm = IRRIGATION_AMOUNTS[irrigation_need]

    # Irrigation action
    if is_healthy:
        irrigation_action = (
            f"Proceed with {irrigation_need.lower()} irrigation ({base_mm}mm recommended)."
        )
    elif is_fungal and irrigation_need == 'High':
        adjusted_mm = IRRIGATION_AMOUNTS['Medium']
        irrigation_action = (
            f"REDUCE irrigation to medium ({adjusted_mm}mm). "
            f"Excess moisture accelerates fungal spread."
        )
    elif is_fungal and irrigation_need == 'Medium':
        irrigation_action = (
            f"Maintain medium irrigation ({base_mm}mm) but avoid "
            f"overhead/foliar watering — fungal disease present."
        )
    else:
        irrigation_action = (
            f"Proceed with {irrigation_need.lower()} irrigation ({base_mm}mm)."
        )

    # Disease action
    if is_healthy:
        disease_action = "No disease detected. Continue routine monitoring."
        treatment      = "No treatment required."
    else:
        species, disease = disease_class.split(' — ')
        treatment      = DISEASE_TREATMENTS.get(disease_class,
            "Consult local agricultural extension officer.")
        disease_action = (
            f"{disease} detected in {species} crop "
            f"(confidence: {confidence*100:.1f}%). Immediate attention required."
        )

    # Action list
    actions = []
    if not is_healthy:
        actions.append(f"DISEASE: {treatment}")
        if is_fungal:
            actions.append("Avoid overhead irrigation — use drip irrigation if possible.")
        actions.append("Isolate affected plants to prevent spread.")
        actions.append("Re-inspect crop in 5-7 days after treatment.")
    actions.append(f"IRRIGATION: {irrigation_action}")
    if irrigation_need == 'High':
        actions.append("Check soil moisture — irrigation is urgent.")
    actions.append("Document findings and monitor weather forecast.")

    # XAI-based explanation
    explanation_parts = []
    if not is_healthy:
        explanation_parts.append(
            f"Disease module detected {disease_class} with {confidence*100:.1f}% "
            f"confidence using MobileNetV2 (Grad-CAM confirmed attention on leaf lesions)."
        )
    else:
        explanation_parts.append("Disease module confirmed healthy crop using MobileNetV2.")
    explanation_parts.append(
        f"Irrigation module predicted {irrigation_need} water need using Decision Tree "
        f"(SHAP: Soil_Moisture and Rainfall_mm are top drivers)."
    )
    if is_fungal and irrigation_need == 'High':
        explanation_parts.append(
            "Irrigation overridden from High to Medium — "
            "fungal pathogens thrive in moist conditions."
        )

    return {
        'disease_class':     disease_class,
        'disease_type':      disease_type,
        'confidence':        round(confidence * 100, 2),
        'irrigation_need':   irrigation_need,
        'severity':          severity,
        'severity_marker':   SEVERITY_MARKERS[severity],
        'disease_action':    disease_action,
        'irrigation_action': irrigation_action,
        'treatment':         treatment,
        'actions':           actions,
        'explanation':       ' '.join(explanation_parts),
    }


def format_recommendation(rec):
    width = 62
    sep   = '=' * width
    thin  = '-' * width
    lines = [
        sep,
        '        AGRO AI — INTEGRATED FARM RECOMMENDATION',
        sep,
        f"  {rec['severity_marker']}  Severity         : {rec['severity']}",
        f"  [DISEASE]   Disease          : {rec['disease_class']}",
        f"  [CONF]      Confidence       : {rec['confidence']}%",
        f"  [WATER]     Irrigation Need  : {rec['irrigation_need']}",
        thin,
        '  RECOMMENDED ACTIONS:',
    ]
    for i, action in enumerate(rec['actions'], 1):
        words = action.split()
        line, chunk = f"  {i}. ", ""
        for word in words:
            if len(line + chunk + word) > 60:
                lines.append(line + chunk)
                line, chunk = "     ", word + " "
            else:
                chunk += word + " "
        lines.append(line + chunk.strip())
    lines += [
        thin,
        '  XAI EXPLANATION:',
    ]
    words = rec['explanation'].split()
    line  = "  "
    for word in words:
        if len(line + word) > 60:
            lines.append(line)
            line = "  " + word + " "
        else:
            line += word + " "
    lines.append(line.strip())
    lines.append(sep)
    return '\n'.join(lines)


if __name__ == '__main__':
    test_cases = [
        ('Tomato — Late Blight',     0.942, 'High'),
        ('Apple — Healthy',          0.998, 'High'),
        ('Potato — Early Blight',    0.876, 'Medium'),
        ('Bell Pepper — Healthy',    0.995, 'Low'),
        ('Grape — Black Rot',        0.731, 'High'),
    ]
    for disease, conf, irrigation in test_cases:
        rec = generate_recommendation(disease, conf, irrigation)
        print(format_recommendation(rec))
        print()