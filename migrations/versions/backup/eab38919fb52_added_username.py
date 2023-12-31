"""added username

Revision ID: eab38919fb52
Revises: c29d8cbbf4a4
Create Date: 2023-10-18 19:51:46.158826

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'eab38919fb52'
down_revision = 'c29d8cbbf4a4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('new_table')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=20), nullable=False))
        batch_op.create_unique_constraint(None, ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('username')

    op.create_table('new_table',
    sa.Column('ID', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('Name', mysql.VARCHAR(length=45), nullable=True),
    sa.Column('new_tablecol', mysql.VARCHAR(length=45), nullable=True),
    sa.PrimaryKeyConstraint('ID'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
