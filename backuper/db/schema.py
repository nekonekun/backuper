from enum import Enum, unique

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa_pg


naming_convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),
    # Indexes
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    # Unique indexes
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    # CHECK-constraints
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    # Foreign keys
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',
    # Primary keys
    'pk': 'pk__%(table_name)s'
}

metadata = sa.MetaData(naming_convention=naming_convention)


@unique
class BackupStatus(Enum):
    SUCCESS = 'Success'
    FAILED_TO_OBTAIN_MODEL = 'Failed to obtain model'
    UNKNOWN_MODEL = 'Unknown model'
    BACKUP_FAILED = 'Backup failed'


backup_statuses_table = sa.Table(
    'backup_statuses',
    metadata,
    sa.Column('ip', sa_pg.INET, primary_key=True),
    sa.Column('status', sa.Enum(BackupStatus, name='backup_status')),
    sa.Column('updated', sa.DateTime),
    sa.Column('backuped', sa.DateTime),
)

backup_methods_table = sa.Table(
    'backup_methods',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('method_name', sa.String, index=True),
    sa.Column('params', sa_pg.JSONB),
)

models_table = sa.Table(
    'models',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('model', sa.String, index=True),
    sa.Column('method', sa.ForeignKey('backup_methods.id')),
)

special_switches_table = sa.Table(
    'special_switches',
    metadata,
    sa.Column('ip', sa_pg.INET, primary_key=True),
    sa.Column('method', sa.ForeignKey('backup_methods.id')),
)
