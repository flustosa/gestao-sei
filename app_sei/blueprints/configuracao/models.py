from app_sei.app import db


class Config(db.Model):
    __tablename__ = "configuracao"
    id = db.Column(db.Integer, primary_key=True)
    sigla_orgao = db.Column(db.String, nullable=False)
    orgao = db.Column(db.String, nullable=False)
    sigla_sistema = db.Column(db.String, nullable=False)
    unidade_bloqueio = db.Column(db.String, nullable=False)
    valida_processo = db.Column(db.Boolean, default=True)
    token = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Configuracao: {self.sigla_orgao}"

    def get_id(self):
        return self.id
