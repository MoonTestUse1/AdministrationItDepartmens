"""initial migration

Revision ID: initial_migration
Revises: 
Create Date: 2024-01-03 22:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'initial_migration'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Создаем таблицу employees
    op.create_table(
        'employees',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('department', sa.String(), nullable=False),
        sa.Column('office', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_employees_id'), 'employees', ['id'], unique=False)

    # Создаем таблицу requests
    op.create_table(
        'requests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('department', sa.String(), nullable=False),
        sa.Column('request_type', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('priority', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_requests_id'), 'requests', ['id'], unique=False)
    op.create_index(op.f('ix_requests_department'), 'requests', ['department'], unique=False)
    op.create_index(op.f('ix_requests_request_type'), 'requests', ['request_type'], unique=False)
    op.create_index(op.f('ix_requests_status'), 'requests', ['status'], unique=False)

    # Создаем таблицу tokens
    op.create_table(
        'tokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tokens_token'), 'tokens', ['token'], unique=True)
    op.create_index(op.f('ix_tokens_user_id'), 'tokens', ['user_id'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_tokens_user_id'), table_name='tokens')
    op.drop_index(op.f('ix_tokens_token'), table_name='tokens')
    op.drop_table('tokens')

    op.drop_index(op.f('ix_requests_status'), table_name='requests')
    op.drop_index(op.f('ix_requests_request_type'), table_name='requests')
    op.drop_index(op.f('ix_requests_department'), table_name='requests')
    op.drop_index(op.f('ix_requests_id'), table_name='requests')
    op.drop_table('requests')

    op.drop_index(op.f('ix_employees_id'), table_name='employees')
    op.drop_table('employees') 