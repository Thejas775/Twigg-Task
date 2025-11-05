from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from decimal import Decimal
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.holding import Holding
from app.models.asset import Asset
from app.schemas.holding import HoldingsResponse, HoldingResponse, PortfolioInsights
from app.utils.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=HoldingsResponse)
async def get_holdings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    holdings_query = db.query(
        Holding.quantity,
        Holding.purchase_price,
        Holding.purchase_date,
        Asset.symbol,
        Asset.name,
        Asset.asset_type,
        Asset.current_price
    ).join(Asset).filter(Holding.user_id == current_user.id)

    holdings_data = holdings_query.all()

    holdings_list = []
    total_current_value = Decimal('0')
    total_investment_cost = Decimal('0')

    for holding in holdings_data:
        current_value = holding.quantity * holding.current_price
        total_cost = holding.quantity * holding.purchase_price
        gain_loss = current_value - total_cost
        gain_loss_percentage = (gain_loss / total_cost * 100) if total_cost > 0 else Decimal('0')

        holdings_list.append(HoldingResponse(
            asset_symbol=holding.symbol,
            asset_name=holding.name,
            asset_type=holding.asset_type,
            quantity=holding.quantity,
            purchase_price=holding.purchase_price,
            current_price=holding.current_price,
            purchase_date=holding.purchase_date,
            current_value=current_value,
            total_cost=total_cost,
            gain_loss=gain_loss,
            gain_loss_percentage=gain_loss_percentage
        ))

        total_current_value += current_value
        total_investment_cost += total_cost

    total_gain_loss = total_current_value - total_investment_cost
    total_gain_loss_percentage = (total_gain_loss / total_investment_cost * 100) if total_investment_cost > 0 else Decimal('0')

    insights = PortfolioInsights(
        total_current_value=total_current_value,
        total_investment_cost=total_investment_cost,
        total_gain_loss=total_gain_loss,
        total_gain_loss_percentage=total_gain_loss_percentage
    )

    return HoldingsResponse(holdings=holdings_list, insights=insights)