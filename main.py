from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @abstractmethod
    def get_role(self):
        pass

class JobSeeker(User):
    def __init__(self, username, password, experience):
        super().__init__(username, password)
        self.experience = experience

    def get_role(self):
        return "Job Seeker"

class Employer(User):
    def __init__(self, username, password, company_name):
        super().__init__(username, password)
        self.company_name = company_name

    def get_role(self):
        return "Employer"

class ResumeAnalyzer: # I will be adding AI that will analzye persons stregnths 
    def analyze(self, experience):
        return f"(Analyzed experience): {experience}"

