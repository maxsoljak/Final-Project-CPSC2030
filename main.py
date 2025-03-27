from flask import Flask, render_template, request, redirect, url_for, session
import hashlib
from abc import ABC, abstractmethod

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Abstract Base Class for Users
class User(ABC):
    def __init__(self, username, password):
        self.username = username
        self.password_hash = self._hash_password(password)
    
    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    @abstractmethod
    def get_role(self):
        pass

# Job Seeker Class
class JobSeeker(User):
    def __init__(self, username, password, school, graduation_year, internship_experience, strengths, work_style):
        super().__init__(username, password)
        self.school = school
        self.graduation_year = graduation_year
        self.internship_experience = internship_experience
        self.strengths = strengths
        self.work_style = work_style
    
    def get_role(self):
        return "Job Seeker"

# Employer Class
class Employer(User):
    def __init__(self, username, password, company_name, looking_for, expectations, team_culture):
        super().__init__(username, password)
        self.company_name = company_name
        self.looking_for = looking_for
        self.expectations = expectations
        self.team_culture = team_culture
    
    def get_role(self):
        return "Employer"

# Resume Analyzer (AI Processing Placeholder)
class ResumeAnalyzer:
    def analyze(self, experience):
        return f"Analyzing experience: {experience}"

# Job Listing Class
class JobListing:
    def __init__(self, title, company, required_skills):
        self.title = title
        self.company = company
        self.required_skills = required_skills

# Job Matcher Class
class JobMatcher:
    def match(self, job_seeker, job_listings):
        matches = []
        for job in job_listings:
            score = len(set(job.required_skills) & set(job_seeker.strengths))
            matches.append((job, score))
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches

# Database Manager (Storage System)
class DatabaseManager:
    def __init__(self):
        self.users = []
        self.jobs = []
    
    def add_user(self, user):
        self.users.append(user)
    
    def add_job(self, job):
        self.jobs.append(job)
    
    def get_users(self):
        return self.users
    
    def get_jobs(self):
        return self.jobs

db = DatabaseManager()

@app.route('/')
def home():
    username = session.get('username')
    role = None
    if username:
        for user in db.get_users():
            if user.username == username:
                role = user.get_role()
                break
    return render_template('index.html', username=username, role=role)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        
        if role == 'Job Seeker':
            return redirect(url_for('job_seeker_form', username=username, password=password))
        else:
            return redirect(url_for('employer_form', username=username, password=password))

    return render_template('register.html')

@app.route('/job_seeker_form', methods=['GET', 'POST'])
def job_seeker_form():
    if request.method == 'POST':
        username = request.args.get('username')
        password = request.args.get('password')
        school = request.form['school']
        graduation_year = request.form['graduation_year']
        internship_experience = request.form['internship_experience']
        strengths = request.form.getlist('strengths')
        work_style = request.form['work_style']

        user = JobSeeker(username, password, school, graduation_year, internship_experience, strengths, work_style)
        db.add_user(user)
        session['username'] = username
        return redirect(url_for('home'))

    return render_template('job_seeker_form.html')

@app.route('/employer_form', methods=['GET', 'POST'])
def employer_form():
    if request.method == 'POST':
        username = request.args.get('username')
        password = request.args.get('password')
        company_name = request.form['company_name']
        looking_for = request.form['looking_for']
        expectations = request.form['expectations']
        team_culture = request.form['team_culture']

        user = Employer(username, password, company_name, looking_for, expectations, team_culture)
        db.add_user(user)
        session['username'] = username
        return redirect(url_for('home'))

    return render_template('employer_form.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        for user in db.get_users():
            if user.username == username and user.password_hash == hashlib.sha256(password.encode()).hexdigest():
                session['username'] = username
                return redirect(url_for('home'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)

