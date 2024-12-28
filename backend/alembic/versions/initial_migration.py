"""Initial migration

Revision ID: initial_migration
Create Date: 2024-03-14 12:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from app.models.request import RequestStatus, RequestPriority

# revision identifiers, used by Alembic.
revision = 'initial_migration'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    connection = op.get_bind()
    
    # Проверяем существование enum типов перед их созданием
    result = connection.execute(sa.text(
        "SELECT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'requeststatus');"
    )).scalar()
    if not result:
        request_status = sa.Enum(RequestStatus, name='requeststatus')
        request_status.create(connection, checkfirst=True)

    result = connection.execute(sa.text(
        "SELECT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'requestpriority');"
    )).scalar()
    if not result:
        request_priority = sa.Enum(RequestPriority, name='requestpriority')
        request_priority.create(connection, checkfirst=True)

    # Create employees table
    op.create_table(
        'employees',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('department', sa.String(), nullable=False),
        sa.Column('office', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_employees_id'), 'employees', ['id'], unique=False)
    op.create_index(op.f('ix_employees_last_name'), 'employees', ['last_name'], unique=False)

    # Create requests table
    op.create_table(
        'requests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('employee_id', sa.Integer(), nullable=True),
        sa.Column('department', sa.String(), nullable=False),
        sa.Column('request_type', sa.String(), nullable=False),
        sa.Column('priority', 'requestpriority', nullable=False),
        sa.Column('status', 'requeststatus', nullable=False, server_default="'NEW'"),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_requests_id'), 'requests', ['id'], unique=False)

def downgrade() -> None:
    op.drop_table('requests')
    op.drop_table('employees')
    
    # Drop enum types if they exist
    connection = op.get_bind()
    connection.execute(sa.text('DROP TYPE IF EXISTS requeststatus CASCADE;'))
    connection.execute(sa.text('DROP TYPE IF EXISTS requestpriority CASCADE;'))