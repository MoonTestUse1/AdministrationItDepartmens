"""update tokens table

Revision ID: update_tokens_table
Revises: 
Create Date: 2024-01-03 21:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'update_tokens_table'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Удаляем старую таблицу tokens если она существует
    op.drop_table('tokens', if_exists=True)
    
    # Создаем новую таблицу tokens с правильной структурой
    op.create_table(
        'tokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tokens_id'), 'tokens', ['id'], unique=False)
    op.create_index(op.f('ix_tokens_token'), 'tokens', ['token'], unique=True)
    op.create_index(op.f('ix_tokens_user_id'), 'tokens', ['user_id'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_tokens_user_id'), table_name='tokens')
    op.drop_index(op.f('ix_tokens_token'), table_name='tokens')
    op.drop_index(op.f('ix_tokens_id'), table_name='tokens')
    op.drop_table('tokens') 