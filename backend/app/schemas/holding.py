from pydantic import BaseModel
from decimal import Decimal
from datetime import date
from typing import List

class HoldingBase(BaseModel):
    asset_symbol: str
    asset_name: str
    asset_type: str
    quantity: Decimal
    purchase_price: Decimal
    current_price: Decimal
    purchase_date: date

class HoldingResponse(HoldingBase):
    current_value: Decimal
    total_cost: Decimal
    gain_loss: Decimal
    gain_loss_percentage: Decimal

    class Config:
        from_attributes = True

class PortfolioInsights(BaseModel):
    total_current_value: Decimal
    total_investment_cost: Decimal
    total_gain_loss: Decimal
    total_gain_loss_percentage: Decimal

class HoldingsResponse(BaseModel):
    holdings: List[HoldingResponse]
    insights: PortfolioInsights