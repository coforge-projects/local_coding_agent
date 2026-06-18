from sqlalchemy.orm import DeclarativeBase

from sqlalchemy import String ,  Text , Integer , JSON , ForeignKey

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column
import uuid


class Base(DeclarativeBase):
    pass




class User(Base):
    __tablename__ = "users"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    azure_oid = mapped_column(String, unique=True)
    email = mapped_column(String)
    name = mapped_column(String)
    role = mapped_column(String, default="user")


class Project (Base):
    __tablename__ = "projects"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = mapped_column(String)
    desc = mapped_column(String)
    owner_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    language = mapped_column(String)
 

class ProjectMember(Base):
    __tablename__ = "project_members"

    project_id = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id") , primary_key=True)
    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id") , primary_key=True)
    role  = mapped_column(String)


class Conversation(Base):
    __tablename__ = "conversations"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id"))
    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id") )
    title  = mapped_column(String)


class Message (Base):
    __tablename__ = "messages"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id") )
    role = mapped_column(String)
    content = mapped_column(Text)
    tokens_used = mapped_column(Integer)


class ToolExecution (Base):
    __tablename__ = "tool_executions"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    message_id = mapped_column(UUID(as_uuid=True) , ForeignKey("messages.id"))
    tool_name = mapped_column(String)
    mcp_server = mapped_column(String)
    arguments_json = mapped_column(JSON)
    result_json = mapped_column(JSON)
    duration_ms = mapped_column(Integer)


class AuditLog (Base):
    __tablename__ = "audit_logs"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    action = mapped_column(String)
    resource_type = mapped_column(String)
    resource_id = mapped_column(String)
    metadata_json = mapped_column(JSON)
    ip_address = mapped_column(String)


