from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Boolean, Integer, PrimaryKeyConstraint

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False)
    lastname: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    followers = relationship(
        "Follower", foreign_keys="[Follower.user_to_id]", back_populates="followed")

    following = relationship(
        "Follower", foreign_keys="[Follower.user_from_id]", back_populates="follower")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "Name": self.firstname
            # do not serialize the password, its a security breach
        }


class Follower(db.Model):
    user_from_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False)
    user_to_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False)

    __table_args__ = (PrimaryKeyConstraint('user_from_id', 'user_to_id'),)

    follower = relationship("User", foreign_keys=[
                            user_from_id], back_populates="following")
    followed = relationship("User", foreign_keys=[
                            user_to_id], back_populates="followers")


class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    author = relationship("User", back_populates="posts")
    comments = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan")
    media = relationship("Media", back_populates="post",
                         cascade="all, delete-orphan")


class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(200), nullable=False)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

    def serializeComment(self):
        return {
            "id": self.id,
            "comment": self.comment_text,
            "author": self.author_id,
            "commented_post": self.post_id
            # do not serialize the password, its a security breach
        }


class Media(db.Model):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String(20), nullable=False)
    url: Mapped[str] = mapped_column(String(100), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

    post = relationship("Post", back_populates="media")
