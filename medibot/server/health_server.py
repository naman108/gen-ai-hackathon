from json import JSONDecodeError
import json
from string import Template
import zmq
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from .model import db
import requests
from medibot.server.model.patient import Patient
from medibot.server.model.record import Record

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:\Users\Natha Paquette\Documents\work\TMF\Schema-Parser\MODA_OpenAPI\gen-ai-hackathon\test.db'

db.init_app(app)


from medibot.server.model.queue_entry import Queue

with app.app_context():
    db.create_all()

ctx = zmq.Context()
socket = ctx.socket(zmq.PAIR)

conflicts = []

patient_index = [
    [],
    [],
    [],
    [],
    []
]

base_prompt = Template("""<s>[INST] <<SYS>>
You are a medical assistant tasked with prioritizing patients in the emergency room.
Please ensure that your responses are socially unbiased.
Priroity should be decided on the following framework:

1: Life-threatening – Your heart has stopped or you’ve experienced life-threatening trauma
 
2: Emergency – You have symptoms of a heart attack or stroke, not conscious, having a lot of trouble breathing, or bleeding severely
 
3: Urgent – You have a head injury, deep cut, chest pain (unrelated to known heart issue), serious infection, urgent mental health concern
 
4: Less urgent – You have a sprain or break, cuts, pain in back, arm or legs
 
5: Not urgent – You have a sore throat, ear infection, minor cuts or bumps, prescription refill

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.
If you don't know the answer, please don't share false information.
<</SYS>>
Input: {{"symptoms": "$symptoms"}}
Output the answer in JSON in the following format: {{"priority": patient_priority, "description": reasoning_for_patient_priority}}. Only output JSON

[/INST]
""")


def build_prompt(symptoms):
    prompt = base_prompt.substitute(symptoms=symptoms)
    return prompt

def request_llm(symptoms) -> dict:
    """request a response from the Ollama API"""
    prompt = build_prompt(symptoms)
    response = requests.post('http://127.0.0.1:11434/api/generate',
                             json={"prompt": prompt, "model": "medllama2", "stream": False, "format": "json"})
    try:
        generated_dict = json.loads(response.json()["response"])
    except JSONDecodeError:
        response = requests.post(
            'http://127.0.0.1:11434/api/generate', params={"prompt": prompt, "model": "medllama2"})
        generated_dict = json.loads(response.json()["response"])

    return generated_dict


def add_patient_to_queue(queue_info: dict, patient: Patient):
    """add a patient to the queue table"""

    # create a queue entry
    queue_entry = Queue(
        patient=patient, priority=queue_info['priority'], description=queue_info['description'])

    if len(patient_index[int(queue_info['priority'])]) > 0:
        resolve_patient_conflict(patient, queue_info)

    else:
        patient_index[int(queue_info['priority'])].append(queue_entry)

    return get_patient_priority(queue_entry)

def get_patient_priority(queue_entry: Queue) -> int:
    """get the patient's priority"""
    priority_index = patient_index[queue_entry.priority]
    return priority_index.index(queue_entry) + 1

def resolve_patient_conflict(queue_entry: Queue, queue_info: dict):
    """resolve a patient conflict"""
    conflicting_queue = patient_index[queue_info['priority']]

    # send a notification to the nurse
    decision = send_nurse_notification(
        queue_entry, conflicting_queue, queue_info['priority'])

    conflicting_queue.insert(decision['index'], queue_entry)


def send_nurse_notification(queue_entry: Queue, conflicting_queue: list, priority: int) -> dict:
    """send a notification to the nurse"""
    socket.send_string(json.dumps(
        {"patient": queue_entry, "priority": priority, "conflicting_queue": conflicting_queue}))
    return socket.recv_json()

@app.route('/patient', methods=['POST'])
def patient_register():
    data = request.get_json()
    msi_card_number = data.get('msi_card_number')
    symptoms = data.get('symptoms')

    # send the prompt to the Ollama API
    resp = request_llm(symptoms)

    # get the patient from the queue
    patient = Patient.query.filter_by(msi=msi_card_number).first()

    queue_position = add_patient_to_queue(resp, patient)

    return {
        "priority": resp['priority'],
        "queue_position": queue_position
    }, 200


@app.route('/patient', methods=['DELETE'])
def patient_complete():
    pass


if __name__ == '__main__':
    app.run(debug=True)
