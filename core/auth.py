import os, json
from datetime import datetime
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from passlib.hash import pbkdf2_sha256

from .validators import validate_email, is_valid_cpf, only_digits, format_cpf_mask

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data.db")
SESSION_FILE = os.getenv("SESSION_FILE", ".session.json")

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    cpf_masked = Column(String(20), nullable=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Favorite(Base):
    __tablename__ = "favorites"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    serie = Column(String(20), nullable=False)
    item_id = Column(String(100), nullable=False)
    meta = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User")

Base.metadata.create_all(bind=engine)

def _save_session(user_id: int, email: str):
    data = {"user_id": user_id, "email": email, "ts": datetime.utcnow().isoformat()}
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def _clear_session():
    try:
        os.remove(SESSION_FILE)
    except FileNotFoundError:
        pass

def current_user() -> Optional[dict]:
    try:
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def register_user(email: str, password: str, cpf: Optional[str] = None) -> int:
    if not validate_email(email):
        raise ValueError("E-mail inválido.")
    if not password or len(password) < 6:
        raise ValueError("Senha deve ter no mínimo 6 caracteres.")
    cpf_masked = None
    if cpf:
        if not is_valid_cpf(cpf):
            raise ValueError("CPF inválido.")
        cpf_masked = format_cpf_mask(only_digits(cpf))
    pwd_hash = pbkdf2_sha256.hash(password)
    with SessionLocal() as s:
        from sqlalchemy import select
        exists = s.execute(select(User).where(User.email == email)).scalar_one_or_none()
        if exists:
            raise ValueError("E-mail já cadastrado.")
        u = User(email=email, cpf_masked=cpf_masked, password_hash=pwd_hash)
        s.add(u)
        s.commit()
        s.refresh(u)
        _save_session(u.id, u.email)
        return u.id

def login_user(email: str, password: str) -> int:
    with SessionLocal() as s:
        from sqlalchemy import select
        u = s.execute(select(User).where(User.email == email)).scalar_one_or_none()
        if not u or not pbkdf2_sha256.verify(password, u.password_hash):
            raise ValueError("Credenciais inválidas.")
        _save_session(u.id, u.email)
        return u.id

def logout_user():
    _clear_session()

def add_favorite(serie: str, item_id: str, meta: Optional[dict] = None) -> int:
    user = current_user()
    if not user:
        raise ValueError("Faça login para salvar favoritos.")
    import json as _json
    with SessionLocal() as s:
        fav = Favorite(user_id=user["user_id"], serie=serie, item_id=item_id, meta=_json.dumps(meta or {}, ensure_ascii=False))
        s.add(fav)
        s.commit()
        s.refresh(fav)
        return fav.id

def list_favorites(serie: Optional[str] = None):
    user = current_user()
    if not user:
        raise ValueError("Faça login para listar favoritos.")
    import json as _json
    with SessionLocal() as s:
        from sqlalchemy import select
        q = select(Favorite).where(Favorite.user_id == user["user_id"])
        if serie:
            q = q.where(Favorite.serie == serie)
        rows = s.execute(q).scalars().all()
        res = []
        for f in rows:
            try:
                meta = _json.loads(f.meta) if f.meta else {}
            except Exception:
                meta = {}
            res.append({"id": f.id, "serie": f.serie, "item_id": f.item_id, "meta": meta, "created_at": f.created_at.isoformat()})
        return res

def remove_favorite(fav_id: int):
    user = current_user()
    if not user:
        raise ValueError("Faça login para remover favoritos.")
    with SessionLocal() as s:
        from sqlalchemy import select
        f = s.execute(select(Favorite).where(Favorite.id == fav_id, Favorite.user_id == user["user_id"])).scalar_one_or_none()
        if not f:
            raise ValueError("Favorito não encontrado.")
        s.delete(f)
        s.commit()
