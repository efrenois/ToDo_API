from flask import Flask, jsonify, request, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from db import db

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"   # Configuration de la base SQLite
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialisation de la base de données
db.init_app(app)

from models import Task, User

# Configuration de l'authentification JWT
app.config["JWT_SECRET_KEY"] = "test_authentification"  # À changer en production
jwt = JWTManager(app)


@app.before_request
def create_tables():
    db.create_all()

##################################### ROUTES API #####################################
# Lire toutes les tâches
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

# Lire une tâche spécifique 
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Tâche non trouvée'}), 404
    return jsonify(task.to_dict())

# Créer une nouvelle tâche
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'Titre manquant'}), 400
    new_task = Task(title=data['title'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201

# Mettre à jour une tâche existante 
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return jsonify({'error': 'Tâche non trouvée'}), 404
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.done = data.get('done', task.done)
    db.session.commit()
    return jsonify(task.to_dict())

# Supprimer une tâche
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Tâche non trouvée"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Tâche supprimée"})

# Ajouter un utilisateur (inscription)
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data: 
        return jsonify({"error": "username et password requis"}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Utilisateur déjà existant"}), 400
    
    hashed_password = generate_password_hash(data['password'])
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Utilisateur créé"}), 201

# Supprimer un utilisateur
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Utilisateur non trouvé"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Utilisateur supprimé"})

# Authentification utilisateur (login)
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
    if not user or not check_password_hash(user.password, data.get('password')):
        return jsonify({"error": "Identifiants invalides"}), 401
    
    # Génération du token d'accès
    token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": token})

####################################### INTERFACE GRAPHIQUE #####################################
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
