import os, json
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data.db")
engine = create_engine(DATABASE_URL, echo=False, future=True, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

class HistoryModel(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    event = Column(String(50), nullable=False)
    serie = Column(String(20), nullable=True)
    payload = Column(Text, nullable=True)

Base.metadata.create_all(bind=engine)

class History:
    def __init__(self):
        self._Session = SessionLocal

    def save(self, event: str, serie: str = None, payload: dict | None = None):
        with self._Session() as s:
            rec = HistoryModel(
                event=event,
                serie=serie,
                payload=json.dumps(payload or {}, ensure_ascii=False),
            )
            s.add(rec)
            s.commit()

    def query(self, event: str | None = None, serie: str | None = None, since: datetime | None = None):
        with self._Session() as s:
            q = s.query(HistoryModel)
            if event:
                q = q.filter(HistoryModel.event == event)
            if serie:
                q = q.filter(HistoryModel.serie == serie)
            if since:
                q = q.filter(HistoryModel.created_at >= since)
            return [{
                "id": r.id,
                "created_at": r.created_at.isoformat(),
                "event": r.event,
                "serie": r.serie,
                "payload": json.loads(r.payload or "{}")
            } for r in q.order_by(HistoryModel.created_at.desc()).all()]
