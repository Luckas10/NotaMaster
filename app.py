from flask import Flask
from database import engine, Session, Base
from controllers.Auth import auth_bp
from controllers.Dashboard import dashboard_bp
from controllers.AddGrades import add_grades_bp
from flask_login import LoginManager
from models.User import User
from models.Subject import Subject

# Registra o blueprint para o controlador de adição de notas

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta'

# Criar o banco de dados, se necessário
Base.metadata.create_all(engine)

subjects = ['Matemática', 'Português', 'História', 'Ciências', 'Física']

for subject_name in subjects:
    session = Session()
    # Verifica se a disciplina já existe no banco de dados
    existing_subject = session.query(Subject).filter_by(name=subject_name).first()
    if not existing_subject:
        # Só adiciona a disciplina se ela não existir
        subject = Subject(name=subject_name)
        session.add(subject)
        session.commit()
    session.close()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    session = Session()  # Inicia a sessão
    user = session.query(User).get(int(user_id))
    session.close()  # Fecha a sessão depois de usá-la
    return user

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(add_grades_bp)

if __name__ == "__main__":
    app.run(debug=True)
