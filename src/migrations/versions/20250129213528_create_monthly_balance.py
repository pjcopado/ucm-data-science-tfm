"""create monthly balance

Revision ID: 20250129213528
Revises: 20250129213415
Create Date: 2025-01-29 22:35:29.239185

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20250129213528"
down_revision = "20250129213415"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "monthly_balance",
        sa.Column("id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("month", sa.String(6), nullable=False),
        sa.Column("market", sa.String(length=2), nullable=False),
        sa.Column("bu", sa.String(length=16), nullable=False),
        sa.Column("volume", sa.NUMERIC(precision=20, scale=2), nullable=False),
        sa.Column("value", sa.NUMERIC(precision=20, scale=2), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_monthly_balance_bu"), "monthly_balance", ["bu"], unique=False)
    op.create_index(op.f("ix_monthly_balance_created_at"), "monthly_balance", ["created_at"], unique=False)
    op.create_index(op.f("ix_monthly_balance_market"), "monthly_balance", ["market"], unique=False)
    op.create_index(op.f("ix_monthly_balance_month"), "monthly_balance", ["month"], unique=False)
    op.create_index(op.f("ix_monthly_balance_value"), "monthly_balance", ["value"], unique=False)
    op.create_index(op.f("ix_monthly_balance_volume"), "monthly_balance", ["volume"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_monthly_balance_volume"), table_name="monthly_balance")
    op.drop_index(op.f("ix_monthly_balance_value"), table_name="monthly_balance")
    op.drop_index(op.f("ix_monthly_balance_month"), table_name="monthly_balance")
    op.drop_index(op.f("ix_monthly_balance_market"), table_name="monthly_balance")
    op.drop_index(op.f("ix_monthly_balance_created_at"), table_name="monthly_balance")
    op.drop_index(op.f("ix_monthly_balance_bu"), table_name="monthly_balance")
    op.drop_table("monthly_balance")
    # ### end Alembic commands ###
