"""Portfolio service for normalizing aggregator data."""

from typing import Dict, List, Any
from sqlalchemy.orm import Session

from app.models.account import Account
from app.models.holding import Holding
from app.models.transaction import Transaction, TransactionType
from app.services.aggregators.mock_broker import MockBrokerAggregator
from app.services.aggregators.mock_bank import MockBankAggregator


class PortfolioService:
    """Service for managing portfolio data from aggregators."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def sync_account_data(self, account: Account) -> None:
        """Sync data from aggregator for a specific account."""
        # Get appropriate aggregator
        if account.provider in ["robinhood", "schwab"]:
            aggregator = MockBrokerAggregator()
        elif account.provider in ["plaid", "akoya"]:
            aggregator = MockBankAggregator()
        else:
            raise ValueError(f"Unsupported provider: {account.provider}")
        
        # Get fresh data from aggregator
        holdings_data = aggregator.get_holdings(account.access_token)
        transactions_data = aggregator.get_transactions(account.access_token)
        
        # Update holdings
        self._update_holdings(account, holdings_data)
        
        # Update transactions
        self._update_transactions(account, transactions_data)
        
        # Update last sync time
        from datetime import datetime
        account.last_sync = datetime.utcnow()
        self.db.commit()
    
    def _update_holdings(self, account: Account, holdings_data: List[Dict[str, Any]]) -> None:
        """Update holdings for an account."""
        # Clear existing holdings
        self.db.query(Holding).filter(Holding.account_id == account.id).delete()
        
        # Add new holdings
        for holding_data in holdings_data:
            holding = Holding(
                account_id=account.id,
                symbol=holding_data["symbol"],
                quantity=holding_data["quantity"],
                avg_cost=holding_data["avg_cost"],
                current_price=holding_data["current_price"],
                value=holding_data["value"]
            )
            self.db.add(holding)
    
    def _update_transactions(self, account: Account, transactions_data: List[Dict[str, Any]]) -> None:
        """Update transactions for an account."""
        # Clear existing transactions
        self.db.query(Transaction).filter(Transaction.account_id == account.id).delete()
        
        # Add new transactions
        for transaction_data in transactions_data:
            transaction = Transaction(
                account_id=account.id,
                symbol=transaction_data.get("symbol"),
                type=TransactionType(transaction_data["type"]),
                quantity=transaction_data.get("quantity"),
                price=transaction_data.get("price"),
                amount=transaction_data["amount"],
                date=transaction_data["date"],
                description=transaction_data.get("description")
            )
            self.db.add(transaction)
    
    def get_portfolio_summary(self, user_id: int) -> Dict[str, Any]:
        """Get portfolio summary for a user."""
        # Get all accounts for user
        accounts = self.db.query(Account).filter(Account.user_id == user_id).all()
        
        total_value = 0
        total_cost = 0
        holdings_count = 0
        
        for account in accounts:
            holdings = self.db.query(Holding).filter(Holding.account_id == account.id).all()
            for holding in holdings:
                total_value += holding.value
                total_cost += holding.quantity * holding.avg_cost
                holdings_count += 1
        
        return {
            "total_value": round(total_value, 2),
            "total_cost": round(total_cost, 2),
            "total_gain_loss": round(total_value - total_cost, 2),
            "total_gain_loss_percent": round(((total_value - total_cost) / total_cost * 100) if total_cost > 0 else 0, 2),
            "holdings_count": holdings_count,
            "accounts_count": len(accounts)
        }
