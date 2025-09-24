"""Portfolio snapshots service."""

from datetime import datetime, date
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.account import Account
from app.models.holding import Holding


class PortfolioSnapshot:
    """Portfolio snapshot model."""
    
    def __init__(self, date: date, total_value: float, total_cost: float):
        self.date = date
        self.total_value = total_value
        self.total_cost = total_cost
        self.gain_loss = total_value - total_cost
        self.gain_loss_percent = (self.gain_loss / total_cost * 100) if total_cost > 0 else 0


class SnapshotsService:
    """Service for managing portfolio snapshots."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_daily_snapshot(self, user_id: int) -> PortfolioSnapshot:
        """Create a daily snapshot of the user's portfolio."""
        # Get all accounts for user
        accounts = self.db.query(Account).filter(Account.user_id == user_id).all()
        account_ids = [account.id for account in accounts]
        
        if not account_ids:
            return PortfolioSnapshot(date.today(), 0, 0)
        
        # Calculate total value and cost
        total_value = 0
        total_cost = 0
        
        holdings = self.db.query(Holding).filter(Holding.account_id.in_(account_ids)).all()
        for holding in holdings:
            total_value += holding.value
            total_cost += holding.quantity * holding.avg_cost
        
        return PortfolioSnapshot(date.today(), total_value, total_cost)
    
    def get_historical_snapshots(self, user_id: int, days: int = 30) -> List[Dict[str, Any]]:
        """Get historical snapshots for charting."""
        # For now, generate mock historical data
        # In production, this would query a snapshots table
        snapshots = []
        base_value = 100000  # Starting portfolio value
        
        for i in range(days):
            snapshot_date = date.today() - timedelta(days=i)
            # Mock some realistic portfolio growth/decline
            daily_change = random.uniform(-0.05, 0.05)  # ±5% daily change
            value = base_value * (1 + daily_change) ** (days - i)
            
            snapshots.append({
                "date": snapshot_date.isoformat(),
                "total_value": round(value, 2),
                "total_cost": round(base_value * 0.95, 2),  # Assume 5% gain overall
                "gain_loss": round(value - base_value * 0.95, 2),
                "gain_loss_percent": round(((value - base_value * 0.95) / (base_value * 0.95)) * 100, 2)
            })
        
        return sorted(snapshots, key=lambda x: x["date"])
    
    def get_portfolio_performance(self, user_id: int) -> Dict[str, Any]:
        """Get portfolio performance metrics."""
        snapshot = self.create_daily_snapshot(user_id)
        
        return {
            "current_value": snapshot.total_value,
            "total_cost": snapshot.total_cost,
            "gain_loss": snapshot.gain_loss,
            "gain_loss_percent": snapshot.gain_loss_percent,
            "snapshot_date": snapshot.date.isoformat()
        }
