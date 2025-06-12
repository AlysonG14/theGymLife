from core.configs import settings
from sqlalchemy import Column, Integer, String, Boolean

class AcademiaModel(settings.DBBaseModel):
        __tablename__ = 'academia'
    
        id: int = Column(Integer, primary_key=True, autoincrement=True)
        aparelho: str = Column(String(255))
        variacao: str = Column(String(255))
        carga: bool = Column(Boolean('Livre', 'Crescente'))
        serie: int = Column(Integer)
        repeticao: int = Column(Integer)


