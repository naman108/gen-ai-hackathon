from json import JSONDecodeError
import json
import zmq
from flask import Flask, request
import requests

from medibot.server.model.patient import Patient
from medibot.server.model.queue_entry import Queue

app = Flask(__name__)

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

base_prompt = """you are a screening agent, you're responsible for deciding peoples order in the emergency 
room queue. 
The patient symptoms description is: %s

your output must be follow the json schema
{
    "description": "your reasoning for the priority of the patient",
    "priority": "the numerical priority of the patient from 1-5"
}
do not give any further information.
"""

def build_prompt(symptoms):
    prompt = str(base_prompt, symptoms)
    return prompt

def request_llm(symptoms) -> dict:
    """request a response from the Ollama API"""
    prompt = build_prompt(symptoms)
    response = requests.post('http://127.0.0.1/api/generate', params={"prompt": prompt, "model": "medllama2"})
    try:
        generated_text = response.json()
    except JSONDecodeError:
        response = requests.post('http://127.0.0.1/api/generate', params={"prompt": prompt, "model": "medllama2"})
        generated_text = response.json()

    return generated_text

def add_patient_to_queue(queue_info: dict, patient: Patient):
    """add a patient to the queue table"""

    # create a queue entry
    queue_entry = Queue(patient=patient, priority=queue_info['priority'], description=queue_info['description'])

    if len(patient_index[queue_info['priority']])>0:
        resolve_patient_conflict(patient, queue_info)

    else:
        patient_index.append(queue_entry)

def resolve_patient_conflict(queue_entry: Queue, queue_info: dict):
    """resolve a patient conflict"""
    conflicting_queue = patient_index[queue_info['priority']]

    # send a notification to the nurse
    decision = send_nurse_notification(queue_entry, conflicting_queue, queue_info['priority'])

    conflicting_queue.insert(decision['index'], queue_entry)
    
def send_nurse_notification(queue_entry: Queue, conflicting_queue: list, priority: int) -> dict:
    """send a notification to the nurse"""
    socket.send_string(json.dumps({"patient": queue_entry, "priority": priority, "conflicting_queue": conflicting_queue}))
    return socket.recv_json()

@app.route('/nurse/conflict', methods=['GET'])


@app.route('/patient', methods=['POST'])
def patient_register():
    data = request.get_json()
    msi_card_number = data.get('msi_card_number')
    symptoms = data.get('symptoms')

    # send the prompt to the Ollama API
    resp = request_llm(symptoms)

    # get the patient from the queue
    patient = Patient.query.filter_by(msi=msi_card_number).first()

    add_patient_to_queue(resp, patient)

    return {"status": "success"}, 200

@app.route('/patient', methods=['DELETEs'])
def patient_complete():
    pass

if __name__ == '__main__':
    app.run(debug=True)