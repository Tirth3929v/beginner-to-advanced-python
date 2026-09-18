"""
Day 69: Relational Database Models Architecture
Implements bidirectional One-to-Many relationships with SQLAlchemy 2.0 ORM:
1. User (Parent) <---> BlogPost (Child)
2. User (Parent) <---> Comment (Child)
3. BlogPost (Parent) <---> Comment (Child)
"""

from typing import List
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, ForeignKey


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Relationship: User -> BlogPosts (One-to-Many)
    posts: Mapped[List["BlogPost"]] = relationship("BlogPost", back_populates="author", cascade="all, delete-orphan")

    # Relationship: User -> Comments (One-to-Many)
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="comment_author", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User #{self.id}: {self.name} ({self.email})>"


class BlogPost(db.Model):
    __tablename__ = "blog_posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

    # Foreign Key -> User.id
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    author: Mapped["User"] = relationship("User", back_populates="posts")

    # Relationship: BlogPost -> Comments (One-to-Many)
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="parent_post", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<BlogPost #{self.id}: {self.title}>"


class Comment(db.Model):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[str] = mapped_column(String(100), nullable=False)

    # Foreign Key -> User.id
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    comment_author: Mapped["User"] = relationship("User", back_populates="comments")

    # Foreign Key -> BlogPost.id
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("blog_posts.id"), nullable=False)
    parent_post: Mapped["BlogPost"] = relationship("BlogPost", back_populates="comments")

    def __repr__(self) -> str:
        return f"<Comment #{self.id} on Post #{self.post_id} by User #{self.author_id}>"
