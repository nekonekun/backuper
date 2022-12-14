"""Initial

Revision ID: 6d74470327d2
Revises: 
Create Date: 2022-12-07 13:19:51.725911

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6d74470327d2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('methods',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('actions', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('subnets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subnet', postgresql.CIDR(), nullable=True),
    sa.Column('folder', sa.String(), server_default='', nullable=True),
    sa.Column('enabled', sa.Boolean(), server_default='true', nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('distinct_devices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('enabled', sa.Boolean(), server_default='true', nullable=True),
    sa.Column('ip_address', postgresql.INET(), nullable=True),
    sa.Column('folder', sa.String(), server_default='', nullable=True),
    sa.Column('device_name', sa.String(), nullable=True),
    sa.Column('method_name', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['method_name'], ['methods.name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('models',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('model', sa.String(), nullable=True),
    sa.Column('method_name', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['method_name'], ['methods.name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('models')
    op.drop_table('distinct_devices')
    op.drop_table('subnets')
    op.drop_table('methods')
    # ### end Alembic commands ###
