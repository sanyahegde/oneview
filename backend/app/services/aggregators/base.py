"""Base aggregator interface."""

from abc import ABC, abstractmethod
from typing import Dict, List, Any


class BaseAggregator(ABC):
    """Base class for financial aggregators."""
    
    @abstractmethod
    def exchange_token(self, public_token: str) -> str:
        """Exchange public token for access token."""
        pass
    
    @abstractmethod
    def get_account_info(self, access_token: str) -> Dict[str, Any]:
        """Get account information."""
        pass
    
    @abstractmethod
    def get_holdings(self, access_token: str) -> List[Dict[str, Any]]:
        """Get account holdings."""
        pass
    
    @abstractmethod
    def get_transactions(self, access_token: str) -> List[Dict[str, Any]]:
        """Get account transactions."""
        pass
