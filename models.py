from db import db

# Définition du modèle utilisateur
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Définition du modèle de tâche
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120),nullable=False)
    done = db.Column(db.Boolean, default=False)

    # Méthode pour convertir l'objet en dictionnaire
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'done': self.done
        }
