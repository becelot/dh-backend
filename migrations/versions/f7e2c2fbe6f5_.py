"""empty message

Revision ID: f7e2c2fbe6f5
Revises: 2479caccac75
Create Date: 2019-05-08 08:28:20.472534

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7e2c2fbe6f5'
down_revision = '2479caccac75'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('RecentDeck',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('current_deck_id', sa.Integer(), nullable=True),
    sa.Column('previous_deck_id', sa.Integer(), nullable=True),
    sa.Column('deck_3_id', sa.Integer(), nullable=True),
    sa.Column('deck_4_id', sa.Integer(), nullable=True),
    sa.Column('deck_5_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['current_deck_id'], ['Deck.id'], ),
    sa.ForeignKeyConstraint(['deck_3_id'], ['Deck.id'], ),
    sa.ForeignKeyConstraint(['deck_4_id'], ['Deck.id'], ),
    sa.ForeignKeyConstraint(['deck_5_id'], ['Deck.id'], ),
    sa.ForeignKeyConstraint(['previous_deck_id'], ['Deck.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('DeckVersion', 'deck_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('DeckVersion', 'deck_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_table('RecentDeck')
    # ### end Alembic commands ###
