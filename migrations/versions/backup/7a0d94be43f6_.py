"""empty message

Revision ID: 7a0d94be43f6
Revises: f1e7f408db82
Create Date: 2023-10-21 21:59:16.445045

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a0d94be43f6'
down_revision = 'f1e7f408db82'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('email', sa.String(length=200), nullable=False),
    sa.Column('favorite_color', sa.String(length=120), nullable=True),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('date_posted', sa.DateTime(), nullable=True),
    sa.Column('slug', sa.String(length=255), nullable=True),
    sa.Column('poster_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['poster_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    op.drop_table('users')
    # ### end Alembic commands ###
