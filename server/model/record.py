from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Record(db.Model):
    __tablename__ = 'records'

    record_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))

    def __repr__(self):
        return f"<Record record_id={self.record_id}>"
