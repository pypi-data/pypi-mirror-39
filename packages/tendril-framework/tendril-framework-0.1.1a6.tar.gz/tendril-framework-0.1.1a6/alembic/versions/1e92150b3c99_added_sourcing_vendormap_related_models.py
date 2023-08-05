"""Added Sourcing VendorMap related models

Revision ID: 1e92150b3c99
Revises: 50df4ae210da
Create Date: 2016-01-06 04:05:57.308887

"""

# revision identifiers, used by Alembic.
revision = '1e92150b3c99'
down_revision = '50df4ae210da'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy_utils.types.arrow import ArrowType


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('SourcingVendor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('dname', sa.String(), nullable=True),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('mapfile_base', sa.String(), nullable=False),
    sa.Column('pclass_str', sa.String(), nullable=False),
    sa.Column('status', sa.Enum('active', 'suspended', 'defunct', name='vendor_status'), server_default='active', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('mapfile_base'),
    sa.UniqueConstraint('name')
    )
    op.create_table('VendorPartMap',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', ArrowType(), nullable=True),
    sa.Column('ident', sa.String(), nullable=False),
    sa.Column('strategy', sa.String(), nullable=True),
    sa.Column('vendor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['vendor_id'], ['SourcingVendor.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('vendor_id', 'ident', name='constraint_vmap_ident')
    )
    op.create_table('VendorPartNumber',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', ArrowType(), nullable=True),
    sa.Column('vpno', sa.String(), nullable=False),
    sa.Column('type', sa.Enum('auto', 'manual', name='map_type'), server_default='auto', nullable=False),
    sa.Column('vpmap_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['vpmap_id'], ['VendorPartMap.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('vpmap_id', 'vpno', name='constraint_vmap_vpno')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('VendorPartNumber')
    op.drop_table('VendorPartMap')
    op.drop_table('SourcingVendor')

    # TODO figure out how to drop ENUM types?
    ### end Alembic commands ###
