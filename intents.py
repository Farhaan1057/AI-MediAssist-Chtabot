import re

INTENT_PATTERNS = {
    "emergency": [
        r"\b(heart attack|stroke|can't breathe|cannot breathe|unconscious|overdose|"
        r"suicide|kill myself|dying|chest pain|severe bleeding|seizure|choking)\b"
    ],
    "symptom_check": [
        r"\b(fever|headache|cough|pain|ache|nausea|vomiting|dizzy|dizziness|fatigue|"
        r"rash|swelling|bleeding|infection|sore throat|runny nose|symptoms?)\b"
    ],
    "medication_info": [
        r"\b(medicine|medication|drug|pill|tablet|dosage|dose|side effect|prescription|"
        r"paracetamol|ibuprofen|antibiotic|painkiller|aspirin)\b"
    ],
    "mental_health": [
        r"\b(anxiety|depression|stress|panic|mental health|sleep|insomnia|sad|"
        r"lonely|overwhelmed|therapy|therapist|psychiatrist|mood)\b"
    ],
    "first_aid": [
        r"\b(burn|cut|wound|bandage|fracture|broken bone|sprain|first aid|bite|sting)\b"
    ],
    "general": []
}

EMERGENCY_RESPONSE = (
    "This sounds like a medical emergency. "
    "Please call emergency services (115 in Pakistan / 911 in US) immediately "
    "or go to the nearest emergency room right away. "
    "Do not wait — get help now."
)

def detect_intent(message: str) -> str:
    message_lower = message.lower()
    for intent, patterns in INTENT_PATTERNS.items():
        if intent == "general":
            continue
        for pattern in patterns:
            if re.search(pattern, message_lower):
                return intent
    return "general"

def is_emergency(message: str) -> bool:
    return detect_intent(message) == "emergency"
