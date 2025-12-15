from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Workshop(db.Model):
    __tablename__ = 'workshop'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True) 
    
    registrations = db.relationship('Registration', backref='workshop', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
       
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'date': str(self.date), 
            'time': str(self.time), 
            'location': self.location,
            'category': self.category,
            'is_active': self.is_active
        }

class Registration(db.Model):
    __tablename__ = 'registration'
    
    id = db.Column(db.Integer, primary_key=True)
    workshop_id = db.Column(db.Integer, db.ForeignKey('workshop.id'), nullable=False)
    
    student_name = db.Column(db.String(150), nullable=False)
    student_email = db.Column(db.String(255), nullable=False)
    
    registration_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def to_dict(self):
        return {
            'id': self.id,
            'workshop_id': self.workshop_id,
            'student_name': self.student_name,
            'student_email': self.student_email,
            'registration_date': str(self.registration_date)
        }
