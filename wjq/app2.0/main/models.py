from main import db

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(255), nullable=False)
    line_number = db.Column(db.Integer, nullable=False)
    line_text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<File {self.file_path}, line {self.line_number}>'