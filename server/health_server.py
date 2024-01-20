import flask

from flask import Flask, request
import requests

from server.model.patient import Patient

app = Flask(__name__)

@app.route('/patient/register', methods=['POST'])
def patient_register():
    data = request.get_json()
    msi_card_number = data.get('msi_card_number')
    symptoms = data.get('symptoms')

    prompt = build_prompt(msi_card_number, symptoms)
    
    # send the prompt to the Ollama API
    response = requests.post('https://api.ollama.ai/v1/complete', json={'prompt': prompt})
    generated_text = response.json()

    return {"status": "success"}, 200

@app.route('/patient/complete', methods=['POST'])
def patient_complete():
    data = request.get_json()
    msi_card_number = data.get('msi_card_number')
    symptoms = data.get('symptoms')

    prompt = build_prompt(msi_card_number, symptoms)
    
    # send the prompt to the Ollama API
    response = requests.post('https://api.ollama.ai/v1/complete', json={'prompt': prompt})
    generated_text = response.json()

    return {"status": "success"}, 200

def add_patient_to_queue(patient_id):
    """add a patient to the queue table"""
    patient = Patient.query.get(patient_id)
    if patient is None:
        return None
    queue = Queue(patient_id=patient_id)
    db.session.add(queue)
    db.session.commit()
    return queue    

def build_prompt(msi_card_number, symptoms):
    prompt = f"Patient Information:\n\nMSI Card Number: {msi_card_number}\nSymptoms: {symptoms}\n"
    return prompt

if __name__ == '__main__':
    app.run(debug=True)