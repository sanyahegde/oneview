"""Mock bank aggregator (Plaid/Akoya)."""

import random
from typing import Dict, List, Any
from datetime import datetime, timedelta

from .base import BaseAggregator


class MockBankAggregator(BaseAggregator):
    """Mock bank aggregator for Plaid/Akoya."""
    
    def exchange_token(self, public_token: str) -> str:
        """Exchange public token for access token."""
        # Mock token exchange
        return f"mock_bank_token_{public_token[-8:]}"
    
    def get_account_info(self, access_token: str) -> Dict[str, Any]:
        """Get account information."""
        return {
            "account_id": f"bank_{access_token[-8:]}",
            "name": f"Bank Account {access_token[-4:]}",
            "type": "bank",
            "status": "active"
        }
    
    def get_holdings(self, access_token: str) -> List[Dict[str, Any]]:
        """Get account holdings (cash only for banks)."""
        # Bank accounts typically only have cash holdings
        return [{
            "symbol": "USD",
            "quantity": random.uniform(1000, 50000),
            "avg_cost": 1.0,
            "current_price": 1.0,
            "value": random.uniform(1000, 50000)
        }]
    
    def get_transactions(self, access_token: str) -> List[Dict[str, Any]]:
        """Get account transactions."""
        # Mock bank transaction data
        transactions = []
        
        for _ in range(random.randint(20, 50)):
            transaction_type = random.choice(["deposit", "withdrawal", "transfer"])
            amount = random.uniform(10, 2000)
            
            transactions.append({
                "symbol": None,  # Cash transactions don't have symbols
                "type": transaction_type,
                "quantity": None,
                "price": None,
                "amount": round(amount, 2),
                "date": datetime.utcnow() - timedelta(days=random.randint(1, 90)),
                "description": f"{transaction_type.title()} transaction"
            })
        
        return sorted(transactions, key=lambda x: x["date"], reverse=True)
