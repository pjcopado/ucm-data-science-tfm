import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from src.app.common.database import Base


class MarketMappingModel(Base):
    __tablename__ = "market_mapping"
    __mapper_args__ = {"eager_defaults": True}

    market: Mapped[str] = mapped_column(sa.String(2), primary_key=True, nullable=False)
    market_des: Mapped[str] = mapped_column(sa.String(32), index=True, nullable=False)
    cluster: Mapped[str] = mapped_column(sa.String(32), index=True, nullable=False)
    region: Mapped[str] = mapped_column(sa.String(32), index=True, nullable=False)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(market={self.market}, market_des={self.market_des})"
