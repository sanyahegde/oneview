"""Mock broker aggregator (Robinhood/Schwab)."""

import random
from typing import Dict, List, Any
from datetime import datetime, timedelta

from .base import BaseAggregator


class MockBrokerAggregator(BaseAggregator):
    """Mock broker aggregator for Robinhood/Schwab."""
    
    def exchange_token(self, public_token: str) -> str:
        """Exchange public token for access token."""
        # Mock token exchange
        return f"mock_broker_token_{public_token[-8:]}"
    
    def get_account_info(self, access_token: str) -> Dict[str, Any]:
        """Get account information."""
        return {
            "account_id": f"broker_{access_token[-8:]}",
            "name": f"Brokerage Account {access_token[-4:]}",
            "type": "brokerage",
            "status": "active"
        }
    
    def get_holdings(self, access_token: str) -> List[Dict[str, Any]]:
        """Get account holdings."""
        # Mock holdings data
        symbols = ["AAPL", "GOOGL", "TSLA", "MSFT", "NVDA", "AMZN", "META", "NFLX"]
        holdings = []
        
        for symbol in random.sample(symbols, random.randint(2, 5)):
            quantity = random.uniform(1, 20)
            avg_cost = random.uniform(50, 500)
            current_price = avg_cost * random.uniform(0.8, 1.3)
            
            holdings.append({
                "symbol": symbol,
                "quantity": round(quantity, 2),
                "avg_cost": round(avg_cost, 2),
                "current_price": round(current_price, 2),
                "value": round(quantity * current_price, 2)
            })
        
        return holdings
    
    def get_transactions(self, access_token: str) -> List[Dict[str, Any]]:
        """Get account transactions."""
        # Mock transaction data
        symbols = ["AAPL", "GOOGL", "TSLA", "MSFT", "NVDA", "AMZN", "META", "NFLX"]
        transactions = []
        
        for _ in range(random.randint(10, 30)):
            symbol = random.choice(symbols)
            transaction_type = random.choice(["buy", "sell"])
            quantity = random.uniform(1, 10)
            price = random.uniform(50, 500)
            amount = quantity * price
            
            transactions.append({
                "symbol": symbol,
                "type": transaction_type,
                "quantity": round(quantity, 2),
                "price": round(price, 2),
                "amount": round(amount, 2),
                "date": datetime.utcnow() - timedelta(days=random.randint(1, 365)),
                "description": f"{transaction_type.title()} {quantity} shares of {symbol}"
            })
        
        return sorted(transactions, key=lambda x: x["date"], reverse=True)
