"""empty message

Revision ID: a27c12adf22b
Revises: f231c3358d57
Create Date: 2019-05-08 07:41:02.507558

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a27c12adf22b'
down_revision = 'f231c3358d57'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'User', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'User', type_='unique')
    # ### end Alembic commands ###
