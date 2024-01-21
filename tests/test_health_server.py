from medibot.server.health_server import request_llm, add_patient_to_queue


def test_request_llm():
    """test the request_llm function"""
    symptoms = "current symptoms are coughing and a sore throat, the patient is 15 years old with no past medical history."
    resp = request_llm(symptoms)
    assert resp['priority'] == 1

def test_add_patient_to_queue():
    """test the add_patient_to_queue function"""

    add_patient_to_queue({"priority": 4, "description": "I have a cough."}, )