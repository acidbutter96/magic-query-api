"""create user table

Revision ID: d36f91b5f863
Revises: 
Create Date: 2022-05-18 18:39:35.494974

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'd36f91b5f863'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """ 
        username: str
        first_name: str
        last_name: str
        password: str
        created_at: datetime
        updated_at: datetime

    """
    op.create_table('users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(10), nullable=False),
        sa.Column('first_name', sa.String(20), nullable=False),
        sa.Column('last_name', sa.String(20), nullable=False),
        sa.Column('password', sa.String(60), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
    )


def downgrade():
    op.drop_table('users')
