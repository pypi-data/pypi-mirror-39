"""Added InventoryIndent Table

Revision ID: 12a02ab56b86
Revises: 3badcc784860
Create Date: 2016-01-20 20:32:44.091261

"""

# revision identifiers, used by Alembic.
revision = '12a02ab56b86'
down_revision = '3badcc784860'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy_utils import ArrowType


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('InventoryIndent',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', ArrowType(), nullable=True),
    sa.Column('updated_at', ArrowType(), nullable=True),
    sa.Column('title', sa.String(length=60), nullable=True),
    sa.Column('desc', sa.String(), nullable=True),
    sa.Column('type', sa.Enum('production', 'prototype', 'testing', 'support', 'rd', name='indent_type'), server_default='production', nullable=False),
    sa.Column('status', sa.Enum('active', 'pending', 'archived', 'reversed', name='indent_status'), server_default='active', nullable=False),
    sa.Column('requested_by_id', sa.Integer(), nullable=False),
    sa.Column('serialno_id', sa.Integer(), nullable=False),
    sa.Column('auth_parent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['auth_parent_id'], ['SerialNumber.id'], ),
    sa.ForeignKeyConstraint(['requested_by_id'], ['User.id'], ),
    sa.ForeignKeyConstraint(['serialno_id'], ['SerialNumber.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('InventoryIndent')
    ### end Alembic commands ###
