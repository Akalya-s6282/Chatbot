from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class PendingVerification(Base):
    __tablename__ = 'pending_verifications'

    id = Column(Integer, primary_key=True)
    discord_user_id = Column(String, unique=True)
    code = Column(String)

# Database setup
engine = create_engine('sqlite:///verifications.db')  # or use PostgreSQL/MySQL
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
