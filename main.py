from flask import Flask, redirect, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect, FlaskForm
from flask_csp.csp import csp_header
from flask_cors import CORS
import logging
from userManagement import signup
from wtforms import StringField, SubmitField
from flask_wtf.csrf import CSRFError

# Setup app and logging
app = Flask(__name__)
app.secret_key = b"_53oi3uriq9pifpff;apl"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/User/OneDrive/Documents/robotclaw/final3/databaseFiles/database.db'

# Initialize SQLAlchemy and CSRFProtect
db = SQLAlchemy()
db.init_app(app)  # This ensures that SQLAlchemy is properly initialized with the app

csrf = CSRFProtect(app)
CORS(app)

# Setup logging
app_log = logging.getLogger(__name__)
logging.basicConfig(filename="security_log.log", encoding="utf-8", level=logging.DEBUG, format="%(asctime)s %(message)s")

# Example Form using Flask-WTF
class DiaryEntryForm(FlaskForm):
    project = StringField('Project Name')
    start_time = StringField('Start Time')
    end_time = StringField('End Time')
    repo = StringField('Repository Link')
    developer_notes = StringField('Developer Notes')
    submit = SubmitField('Submit')

# Route Definitions
@app.route("/index", methods=["GET"])
def root():
    return redirect("/", 302)

@app.route("/", methods=["POST", "GET"])
@csp_header({
    "base-uri": "'self'",
    "default-src": "'self'",
    "style-src": "'self'",
    "script-src": "'self'",
    "img-src": "'self' data:",
    "media-src": "'self'",
    "font-src": "'self'",
    "object-src": "'self'",
    "child-src": "'self'",
    "connect-src": "'self'",
    "worker-src": "'self'",
    "report-uri": "/csp_report",
    "frame-ancestors": "'none'",
    "form-action": "'self'",
    "frame-src": "'none'",
})
def index():
    return render_template("/index.html")

@app.route("/privacy.html", methods=["GET"])
def privacy():
    return render_template("/privacy.html")

@app.route("/signup", methods=["POST"])
def signup_route():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    signup(username, password)
    return jsonify({"message": f"User '{username}' signed up successfully!"}), 201

@app.route("/search", methods=["POST", "GET"])
def search():
    form = DiaryEntryForm()  # Ensure the form object is created and passed to the template
    search_field = request.form['search_field']
    search_term = request.form['search_term']

    # Make sure to use the DiaryEntry model for querying
    if search_field == 'developer_name':
        search_results = db.session.query(DiaryEntry).filter(DiaryEntry.developer_name.contains(search_term)).all()
    elif search_field == 'project_name':
        search_results = db.session.query(DiaryEntry).filter(DiaryEntry.project_name.contains(search_term)).all()
    elif search_field == 'diary_entry_time':
        search_results = db.session.query(DiaryEntry).filter(DiaryEntry.diary_entry_time.contains(search_term)).all()
    elif search_field == 'total_time_worked':
        # Check if the search_term is a valid float
        try:
            search_results = db.session.query(DiaryEntry).filter(DiaryEntry.total_time_worked == float(search_term)).all()
        except ValueError:
            search_results = []  # Or you can handle the error differently

    return render_template('form.html', form=form, search_results=search_results)

@app.route("/form", methods=["POST", "GET"])
def form():
    form = DiaryEntryForm()  # Initialize the form
    form_data = None  # Default value in case of GET request

    if form.validate_on_submit():
        project_name = form.project.data
        start_time = form.start_time.data
        end_time = form.end_time.data
        repo = form.repo.data
        developer_notes = form.developer_notes.data
        developer_name = 'Developer'
        diary_entry_time = '2025-02-05 12:00:00'
        total_time_worked = 5.0 

        new_entry = DiaryEntry(
            project_name=project_name,
            start_time=start_time,
            end_time=end_time,
            repo=repo,
            developer_notes=developer_notes,
            developer_name=developer_name,
            diary_entry_time=diary_entry_time,
            total_time_worked=total_time_worked
        )
        db.session.add(new_entry)
        db.session.commit()

        form_data = {
            'project_name': project_name,
            'start_time': start_time,
            'end_time': end_time,
            'repo': repo,
            'developer_notes': developer_notes,
            'developer_name': developer_name,
            'diary_entry_time': diary_entry_time,
            'total_time_worked': total_time_worked
        }

    return render_template('form.html', form=form, form_data=form_data)


class DiaryEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    repo = db.Column(db.String(100))
    developer_notes = db.Column(db.String(500))
    developer_name = db.Column(db.String(100))
    diary_entry_time = db.Column(db.DateTime)
    total_time_worked = db.Column(db.Float)

    def __repr__(self):
        return f'<DiaryEntry {self.id}>'

# Create tables within app context
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
