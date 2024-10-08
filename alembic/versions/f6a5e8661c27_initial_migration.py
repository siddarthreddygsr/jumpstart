"""Initial migration

Revision ID: f6a5e8661c27
Revises:
Create Date: 2024-09-21 02:16:58.452939

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f6a5e8661c27'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('id', sa.String(), nullable=False))
    op.add_column('users', sa.Column('name', sa.String(), nullable=False))
    op.add_column('users', sa.Column('email', sa.String(), nullable=False))
    op.add_column('users', sa.Column('hashed_password', sa.String(), nullable=False))
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    # ### end Alembic commands ###op.add_column('users', sa.Column('name', sa.String(), nullable=False))


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_column('users', 'hashed_password')
    op.drop_column('users', 'email')
    op.drop_column('users', 'name')
    op.drop_column('users', 'id')
    # ### end Alembic commands ###
