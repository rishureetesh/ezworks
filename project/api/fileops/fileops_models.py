from project import db
from sqlalchemy.dialects.mysql import INTEGER

class File(db.Model):
    __tablename__ = "EZ_files"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug_id = db.Column(db.String(255), nullable=False, index=True)
    uploaded_by = db.Column(db.String(255), nullable=False)
    file_uuid = db.Column(db.String(255), nullable=False, index=True)


    def __init__(self, name, slug_id, uploaded_by, file_uuid):
        self.name = name
        self.slug_id = slug_id
        self.uploaded_by = uploaded_by
        self.file_uuid = file_uuid

    def create(self):
        db.session.add(self)
        db.session.commit()
        return