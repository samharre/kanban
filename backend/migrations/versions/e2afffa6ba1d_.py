"""empty message

Revision ID: e2afffa6ba1d
Revises: 1ddd98f6e82b
Create Date: 2020-10-20 20:31:34.161147

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2afffa6ba1d'
down_revision = '1ddd98f6e82b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'phase', ['title'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'phase', type_='unique')
    # ### end Alembic commands ###
