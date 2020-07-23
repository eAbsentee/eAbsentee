"""empty message

Revision ID: bec221a136e5
Revises: e7b58654fe02
Create Date: 2020-07-21 21:21:04.779507

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bec221a136e5'
down_revision = 'e7b58654fe02'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('lat', sa.String(length=32), nullable=True))
    op.add_column('users', sa.Column('long', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'long')
    op.drop_column('users', 'lat')
    # ### end Alembic commands ###