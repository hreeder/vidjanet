"""empty message

Revision ID: 24394b382fef
Revises: 296f140e113b
Create Date: 2014-10-25 16:52:05.704557

"""

# revision identifiers, used by Alembic.
revision = '24394b382fef'
down_revision = '296f140e113b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('primary', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('game')
    ### end Alembic commands ###
