from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import String, Text, Integer, JSON, ForeignKey
import uuid


class Base(DeclarativeBase):
    pass


#  USER
class User(Base):
    __tablename__ = "users"

    id = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    azure_oid = mapped_column(String(255), unique=True)
    email = mapped_column(String(255))
    name = mapped_column(String(255))
    role = mapped_column(String(50), default="user")


#  PROJECT
class Project(Base):
    __tablename__ = "projects"

    id = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = mapped_column(String(255))
    desc = mapped_column(String(1000))
    owner_id = mapped_column(String(36), ForeignKey("users.id"))
    language = mapped_column(String(50))


#  PROJECT MEMBER
class ProjectMember(Base):
    __tablename__ = "project_members"

    project_id = mapped_column(String(36), ForeignKey("projects.id"), primary_key=True)
    user_id = mapped_column(String(36), ForeignKey("users.id"), primary_key=True)
    role = mapped_column(String(50))


#  CONVERSATION
class Conversation(Base):
    __tablename__ = "conversations"

    id = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = mapped_column(String(36), ForeignKey("projects.id"))
    user_id = mapped_column(String(36), ForeignKey("users.id"))
    title = mapped_column(String(500))


#  MESSAGE
class Message(Base):
    __tablename__ = "messages"

    id = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = mapped_column(String(36), ForeignKey("conversations.id"))
    role = mapped_column(String(50))
    content = mapped_column(Text)
    tokens_used = mapped_column(Integer)


#  TOOL EXECUTION
class ToolExecution(Base):
    __tablename__ = "tool_executions"

    id = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    message_id = mapped_column(String(36), ForeignKey("messages.id"))
    tool_name = mapped_column(String(255))
    mcp_server = mapped_column(String(255))
    arguments_json = mapped_column(JSON)
    result_json = mapped_column(JSON)
    duration_ms = mapped_column(Integer)


#  AUDIT LOG
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = mapped_column(String(36), ForeignKey("users.id"))
    action = mapped_column(String(50))
    resource_type = mapped_column(String(50))
    resource_id = mapped_column(String(255))
    metadata_json = mapped_column(JSON)
    ip_address = mapped_column(String(45))
