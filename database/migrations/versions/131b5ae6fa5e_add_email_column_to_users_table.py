"""add email column to users table

Revision ID: 131b5ae6fa5e
Revises: 5500e38686c0
Create Date: 2022-05-19 03:47:05.835862

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '131b5ae6fa5e'
down_revision = '5500e38686c0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.String(length=100), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'email')
    # ### end Alembic commands ###