from typing import Optional
import datetime

from sqlalchemy import DateTime, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
        UniqueConstraint('email', name='users_email_unique')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(Text, nullable=False)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))

    career_paths: Mapped[list['CareerPaths']] = relationship('CareerPaths', back_populates='user')
    certificates: Mapped[list['Certificates']] = relationship('Certificates', back_populates='user')
    experiences: Mapped[list['Experiences']] = relationship('Experiences', back_populates='user')
    projects: Mapped[list['Projects']] = relationship('Projects', back_populates='user')
    resumes: Mapped[list['Resumes']] = relationship('Resumes', back_populates='user')
    ai_enhanced_experience: Mapped[list['AiEnhancedExperience']] = relationship('AiEnhancedExperience', back_populates='user')
    topics: Mapped[list['Topics']] = relationship('Topics', back_populates='user')


class CareerPaths(Base):
    __tablename__ = 'career_paths'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='career_paths_user_id_users_id_fk'),
        PrimaryKeyConstraint('id', name='career_paths_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    resume_lang: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))

    user: Mapped['Users'] = relationship('Users', back_populates='career_paths')
    topics: Mapped[list['Topics']] = relationship('Topics', back_populates='career_path')


class Certificates(Base):
    __tablename__ = 'certificates'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='certificates_user_id_users_id_fk'),
        PrimaryKeyConstraint('id', name='certificates_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    resume_lang: Mapped[str] = mapped_column(Text, nullable=False)
    certificate: Mapped[dict] = mapped_column(JSONB, nullable=False)

    user: Mapped['Users'] = relationship('Users', back_populates='certificates')


class Experiences(Base):
    __tablename__ = 'experiences'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='experiences_user_id_users_id_fk'),
        PrimaryKeyConstraint('id', name='experiences_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    resume_lang: Mapped[str] = mapped_column(Text, nullable=False)
    experience: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))

    user: Mapped['Users'] = relationship('Users', back_populates='experiences')
    ai_enhanced_experience: Mapped[list['AiEnhancedExperience']] = relationship('AiEnhancedExperience', back_populates='experience_')
    topics: Mapped[list['Topics']] = relationship('Topics', back_populates='experience')


class Projects(Base):
    __tablename__ = 'projects'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='projects_user_id_users_id_fk'),
        PrimaryKeyConstraint('id', name='projects_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    resume_lang: Mapped[str] = mapped_column(Text, nullable=False)
    project: Mapped[dict] = mapped_column(JSONB, nullable=False)

    user: Mapped['Users'] = relationship('Users', back_populates='projects')


class Resumes(Base):
    __tablename__ = 'resumes'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='resumes_user_id_users_id_fk'),
        PrimaryKeyConstraint('id', name='resumes_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    resume_lang: Mapped[str] = mapped_column(Text, nullable=False)
    contact: Mapped[dict] = mapped_column(JSONB, nullable=False)
    skills: Mapped[dict] = mapped_column(JSONB, nullable=False)
    languages: Mapped[dict] = mapped_column(JSONB, nullable=False)
    interests: Mapped[dict] = mapped_column(JSONB, nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(Text)

    user: Mapped['Users'] = relationship('Users', back_populates='resumes')


class AiEnhancedExperience(Base):
    __tablename__ = 'ai_enhanced_experience'
    __table_args__ = (
        ForeignKeyConstraint(['experience_id'], ['experiences.id'], ondelete='CASCADE', name='ai_enhanced_experience_experience_id_experiences_id_fk'),
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='ai_enhanced_experience_user_id_users_id_fk'),
        PrimaryKeyConstraint('id', name='ai_enhanced_experience_pkey'),
        Index('one_enhance_per_exp', 'user_id', 'experience_id', postgresql_include=[], unique=True)
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    experience_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    resume_lang: Mapped[str] = mapped_column(Text, nullable=False)
    experience: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))

    experience_: Mapped['Experiences'] = relationship('Experiences', back_populates='ai_enhanced_experience')
    user: Mapped['Users'] = relationship('Users', back_populates='ai_enhanced_experience')


class Topics(Base):
    __tablename__ = 'topics'
    __table_args__ = (
        ForeignKeyConstraint(['career_path_id'], ['career_paths.id'], ondelete='CASCADE', name='topics_career_path_id_career_paths_id_fk'),
        ForeignKeyConstraint(['experience_id'], ['experiences.id'], ondelete='CASCADE', name='topics_experience_id_experiences_id_fk'),
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='topics_user_id_users_id_fk'),
        PrimaryKeyConstraint('id', name='topics_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    career_path_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    experience_id: Mapped[int] = mapped_column(Integer, nullable=False)
    resume_lang: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    topic: Mapped[Optional[str]] = mapped_column(Text)

    career_path: Mapped['CareerPaths'] = relationship('CareerPaths', back_populates='topics')
    experience: Mapped['Experiences'] = relationship('Experiences', back_populates='topics')
    user: Mapped['Users'] = relationship('Users', back_populates='topics')
