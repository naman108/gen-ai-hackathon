from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Queue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer)
    urgency_number = db.Column(db.Integer)
    patient_id = db.Column(db.Integer)

    def __init__(self, order, urgency_number, patient_id):
        self.order = order
        self.urgency_number = urgency_number
        self.patient_id = patient_id
