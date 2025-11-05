"""add_exchange_rates_table

Revision ID: c369269cf708
Revises: 74c054a265fc
Create Date: 2025-11-05 19:21:44.890879

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c369269cf708'
down_revision: Union[str, None] = '74c054a265fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'exchange_rates',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('currency_code', sa.String(length=10), nullable=False, comment='통화 코드 (예: USD)'),
        sa.Column('currency_name', sa.String(length=50), nullable=True, comment='통화명 (예: 미국 달러)'),
        sa.Column('base_rate', sa.Numeric(precision=15, scale=2), nullable=False, comment='기준율 (매매기준율)'),
        sa.Column('previous_rate', sa.Numeric(precision=15, scale=2), nullable=True, comment='이전 기준율 (등락률 계산용)'),
        sa.Column('change_rate', sa.Numeric(precision=10, scale=4), nullable=True, comment='등락률 (%)'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True, comment='업데이트 시각'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_exchange_rates_currency_code'), 'exchange_rates', ['currency_code'], unique=True)
    op.create_index(op.f('ix_exchange_rates_id'), 'exchange_rates', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_exchange_rates_id'), table_name='exchange_rates')
    op.drop_index(op.f('ix_exchange_rates_currency_code'), table_name='exchange_rates')
    op.drop_table('exchange_rates')
