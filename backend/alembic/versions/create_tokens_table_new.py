"""create tokens table

Revision ID: create_tokens_table_new
Revises: merge_heads
Create Date: 2024-01-03 17:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'create_tokens_table_new'
down_revision = 'merge_heads'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('tokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('access_token', sa.String(), nullable=False),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tokens_access_token'), 'tokens', ['access_token'], unique=True)
    op.create_index(op.f('ix_tokens_id'), 'tokens', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_tokens_id'), table_name='tokens')
    op.drop_index(op.f('ix_tokens_access_token'), table_name='tokens')
    op.drop_table('tokens') 