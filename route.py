from flask import Blueprint, request, jsonify
from datetime import datetime, date, time
from models import db, Workshop, Registration

api = Blueprint('api', __name__, url_prefix='/api/v1')

def admin_required():
    if request.headers.get('X-Admin-Key') != 'SECRETO_ADMIN_123':
        return False, jsonify({'message': 'Acceso no autorizado. Se requiere clave de administrador.'}), 401
    return True, None, None

@api.route('/workshops', methods=['GET'])
def get_workshops():
    workshops = Workshop.query.filter_by(is_active=True).all()
    
    if admin_required()[0]:
        workshops = Workshop.query.all()
        
    return jsonify([w.to_dict() for w in workshops]), 200

@api.route('/workshops/<int:workshop_id>', methods=['GET'])
def get_workshop(workshop_id):
    workshop = Workshop.query.get(workshop_id)
    if workshop is None or not workshop.is_active:
        return jsonify({'message': 'Taller no encontrado'}), 404
    return jsonify(workshop.to_dict()), 200

@api.route('/workshops', methods=['POST'])
def create_workshop():
    authorized, response, status = admin_required()
    if not authorized:
        return response, status

    data = request.get_json()
    
    if not all(k in data for k in ['name', 'date', 'time', 'location', 'category']):
        return jsonify({'message': 'Faltan campos obligatorios'}), 400

    try:
        new_workshop = Workshop(
            name=data['name'],
            description=data.get('description', ''),
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            time=datetime.strptime(data['time'], '%H:%M').time(),
            location=data['location'],
            category=data['category']
        )
        db.session.add(new_workshop)
        db.session.commit()
        return jsonify(new_workshop.to_dict()), 201
    except ValueError:
        return jsonify({'message': 'Formato de Fecha/Hora incorrecto (use YYYY-MM-DD y HH:MM)'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al crear el taller: {str(e)}'}), 500

@api.route('/workshops/<int:workshop_id>', methods=['PUT'])
def update_workshop(workshop_id):
    authorized, response, status = admin_required()
    if not authorized:
        return response, status
        
    workshop = Workshop.query.get(workshop_id)
    if workshop is None:
        return jsonify({'message': 'Taller no encontrado'}), 404

    data = request.get_json()
    try:
        workshop.name = data.get('name', workshop.name)
        workshop.description = data.get('description', workshop.description)
        if 'date' in data:
            workshop.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        if 'time' in data:
            workshop.time = datetime.strptime(data['time'], '%H:%M').time()

        workshop.location = data.get('location', workshop.location)
        workshop.category = data.get('category', workshop.category)
        workshop.is_active = data.get('is_active', workshop.is_active) 

        db.session.commit()
        return jsonify(workshop.to_dict()), 200
    except ValueError:
        return jsonify({'message': 'Formato de Fecha/Hora incorrecto (use YYYY-MM-DD y HH:MM)'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al actualizar: {str(e)}'}), 500


@api.route('/workshops/<int:workshop_id>', methods=['DELETE'])
def delete_workshop(workshop_id):
    authorized, response, status = admin_required()
    if not authorized:
        return response, status
        
    workshop = Workshop.query.get(workshop_id)
    if workshop is None:
        return jsonify({'message': 'Taller no encontrado'}), 404

    workshop.is_active = False
    db.session.commit()
    return jsonify({'message': f'Taller "{workshop.name}" (ID: {workshop_id}) ha sido cancelado.'}), 200

@api.route('/workshops/<int:workshop_id>/register', methods=['POST'])
def register_student(workshop_id):
    workshop = Workshop.query.get(workshop_id)
    if workshop is None or not workshop.is_active:
        return jsonify({'message': 'Taller no encontrado o cancelado'}), 404

    data = request.get_json()
    if not all(k in data for k in ['student_name', 'student_email']):
        return jsonify({'message': 'Se requiere nombre y correo electrónico del estudiante'}), 400
        
    existing_registration = Registration.query.filter_by(
        workshop_id=workshop_id, 
        student_email=data['student_email']
    ).first()
    
    if existing_registration:
        return jsonify({'message': 'Ya estás registrado en este taller.'}), 409 

    try:
        new_registration = Registration(
            workshop_id=workshop_id,
            student_name=data['student_name'],
            student_email=data['student_email']
        )
        db.session.add(new_registration)
        db.session.commit()
        return jsonify({
            'message': 'Registro exitoso',
            'registration': new_registration.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error de registro: {str(e)}'}), 500
