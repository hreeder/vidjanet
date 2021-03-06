"""empty message

Revision ID: 48960b8ea815
Revises: None
Create Date: 2014-10-25 15:48:19.485013

"""

# revision identifiers, used by Alembic.
revision = '48960b8ea815'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('timeslot',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('day', sa.String(length=32), nullable=True),
    sa.Column('start', sa.String(length=32), nullable=True),
    sa.Column('end', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('timeslot')
    ### end Alembic commands ###
