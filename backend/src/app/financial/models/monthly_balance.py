import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from src.app.common.database import Base, UUIDMixIn


class MonthlyBalanceModel(Base, UUIDMixIn):
    __tablename__ = "monthly_balance"
    __mapper_args__ = {"eager_defaults": True}

    month: Mapped[str] = mapped_column(sa.String(6), nullable=False, index=True)
    market: Mapped[str] = mapped_column(sa.String(2), index=True, nullable=False)
    bu: Mapped[str] = mapped_column(sa.String(16), index=True, nullable=False)
    volume: Mapped[float] = mapped_column(sa.NUMERIC(20, 2), index=True, nullable=False)
    value: Mapped[float] = mapped_column(sa.NUMERIC(20, 2), index=True, nullable=False)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(period={self.market}{self.month}, market={self.market}, bu={self.bu}, volume={self.volume}, value={self.value})"
