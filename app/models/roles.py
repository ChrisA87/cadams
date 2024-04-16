from .. import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    @staticmethod
    def insert_roles():
        for id, name in enumerate(['user', 'moderator', 'admin'], 1):
            role = Role.query.filter_by(name=name).first()
            if role is None:
                role = Role(name=name, id=id)
                db.session.add(role)
                db.session.commit()

    def __repr__(self):
        return f"<Role {self.name} ({self.id})>"
