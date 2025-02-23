from flask import Flask
from database import engine, Session, Base
from controllers.Auth import auth_bp
from controllers.Dashboard import dashboard_bp
from controllers.AddGrades import add_grades_bp
from controllers.SubjectController import subject_bp  # Importamos o novo controller
from flask_login import LoginManager
from models.User import User
from models.Subject import Subject
from models.Enrollment import Enrollment  # Para criar a tabela no BD
# ... seus outros imports (models etc.) ...

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta'

# Cria as tabelas (incluindo a nova Enrollment)
Base.metadata.create_all(engine)

# Se quiser, você pode criar algumas disciplinas padrão:
subjects = ['Matemática', 'Português', 'História', 'Ciências', 'Física']
for subject_name in subjects:
    session = Session()
    existing_subject = session.query(Subject).filter_by(name=subject_name).first()
    if not existing_subject:
        subject = Subject(name=subject_name)
        session.add(subject)
        session.commit()
    session.close()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    session = Session()
    user = session.query(User).get(int(user_id))
    session.close()
    return user

# Registra todos os blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(add_grades_bp)
app.register_blueprint(subject_bp)

if __name__ == "__main__":
    app.run(debug=True)
