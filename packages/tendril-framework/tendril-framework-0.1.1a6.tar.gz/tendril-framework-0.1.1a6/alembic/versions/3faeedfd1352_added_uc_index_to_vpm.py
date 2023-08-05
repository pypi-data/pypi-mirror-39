"""Added UC index to VPM

Revision ID: 3faeedfd1352
Revises: 142224936b78
Create Date: 2016-05-31 11:11:12.373350

"""

# revision identifiers, used by Alembic.
revision = '3faeedfd1352'
down_revision = '142224936b78'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_vid_ident', 'VendorPartMap', ['vendor_id', 'ident'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_vid_ident', table_name='VendorPartMap')
    ### end Alembic commands ###
