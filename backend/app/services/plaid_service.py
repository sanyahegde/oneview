"""
Plaid API Service
Handles integration with Plaid API for fetching real financial data.

Note: Install plaid-python first: pip install plaid-python
Get credentials from: https://dashboard.plaid.com
"""
from typing import Dict, Optional, List
from datetime import datetime, timedelta
from app.core.config import settings

# Try importing Plaid - structure may vary by version
PLAID_AVAILABLE = False
try:
    from plaid.api import plaid_api
    from plaid.configuration import Configuration
    from plaid.api_client import ApiClient
    PLAID_AVAILABLE = True
except ImportError:
    print("Warning: plaid-python not installed. Install with: pip install plaid-python")


def get_plaid_client():
    """
    Create and return a Plaid API client.
    Requires PLAID_CLIENT_ID, PLAID_SECRET, and PLAID_ENV in settings.
    """
    if not PLAID_AVAILABLE:
        raise ImportError("plaid-python is not installed. Run: pip install plaid-python")
    
    if not settings.PLAID_CLIENT_ID or not settings.PLAID_SECRET:
        raise ValueError("Plaid credentials not configured. Set PLAID_CLIENT_ID and PLAID_SECRET in .env")
    
    # Create configuration
    configuration = Configuration(
        host=settings.PLAID_ENV,  # 'sandbox', 'development', or 'production'
    )
    configuration.api_key['clientId'] = settings.PLAID_CLIENT_ID
    configuration.api_key['secret'] = settings.PLAID_SECRET
    
    api_client = ApiClient(configuration)
    return plaid_api.PlaidApi(api_client)


async def create_link_token(user_id: int) -> Dict:
    """
    Create a Link token for Plaid Link initialization.
    This token is used to launch Plaid Link in the frontend.
    """
    if not PLAID_AVAILABLE:
        raise ImportError("plaid-python is not installed")
    
    try:
        from plaid.model.link_token_create_request import LinkTokenCreateRequest
        from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
        from plaid.model.country_code import CountryCode
        from plaid.model.products import Products
        
        client = get_plaid_client()
        request = LinkTokenCreateRequest(
            products=[Products('transactions'), Products('investments')],
            client_name="One View",
            country_codes=[CountryCode('US')],
            language='en',
            user=LinkTokenCreateRequestUser(
                client_user_id=str(user_id)
            )
        )
        response = client.link_token_create(request)
        return {
            'link_token': response['link_token'],
            'expiration': response['expiration']
        }
    except Exception as e:
        print(f"Error creating Link token: {e}")
        raise


async def exchange_public_token(public_token: str) -> Dict:
    """
    Exchange a public token from Plaid Link for an access token.
    Store the access_token securely in your database.
    """
    if not PLAID_AVAILABLE:
        raise ImportError("plaid-python is not installed")
    
    try:
        from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
        
        client = get_plaid_client()
        request = ItemPublicTokenExchangeRequest(public_token=public_token)
        response = client.item_public_token_exchange(request)
        return {
            'access_token': response['access_token'],
            'item_id': response['item_id']
        }
    except Exception as e:
        print(f"Error exchanging public token: {e}")
        raise


async def get_accounts(access_token: str) -> List[Dict]:
    """
    Get all accounts (banking and investment) associated with an access token.
    """
    if not PLAID_AVAILABLE:
        raise ImportError("plaid-python is not installed")
    
    try:
        from plaid.model.accounts_get_request import AccountsGetRequest
        
        client = get_plaid_client()
        request = AccountsGetRequest(access_token=access_token)
        response = client.accounts_get(request)
        
        accounts = []
        for account in response['accounts']:
            accounts.append({
                'account_id': account['account_id'],
                'name': account['name'],
                'mask': account.get('mask'),
                'type': account['type'],
                'subtype': account.get('subtype'),
                'balances': {
                    'available': account['balances'].get('available'),
                    'current': account['balances'].get('current'),
                    'limit': account['balances'].get('limit'),
                    'iso_currency_code': account['balances'].get('iso_currency_code'),
                }
            })
        return accounts
    except Exception as e:
        print(f"Error fetching accounts: {e}")
        raise


async def get_transactions(access_token: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict]:
    """
    Get transactions for an access token.
    Defaults to last 30 days if dates not provided.
    """
    if not PLAID_AVAILABLE:
        raise ImportError("plaid-python is not installed")
    
    try:
        from plaid.model.transactions_get_request import TransactionsGetRequest
        
        client = get_plaid_client()
        
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)
        if not end_date:
            end_date = datetime.now()
        
        request = TransactionsGetRequest(
            access_token=access_token,
            start_date=start_date.date(),
            end_date=end_date.date()
        )
        response = client.transactions_get(request)
        
        transactions = []
        for transaction in response['transactions']:
            transactions.append({
                'transaction_id': transaction['transaction_id'],
                'account_id': transaction['account_id'],
                'amount': transaction['amount'],
                'date': transaction['date'].isoformat() if hasattr(transaction['date'], 'isoformat') else str(transaction['date']),
                'name': transaction['name'],
                'merchant_name': transaction.get('merchant_name'),
                'category': transaction.get('category'),
                'pending': transaction.get('pending', False),
            })
        return transactions
    except Exception as e:
        print(f"Error fetching transactions: {e}")
        raise


async def get_investment_holdings(access_token: str) -> List[Dict]:
    """
    Get investment holdings (securities/stocks) for an access token.
    """
    if not PLAID_AVAILABLE:
        raise ImportError("plaid-python is not installed")
    
    try:
        from plaid.model.investments_holdings_get_request import InvestmentsHoldingsGetRequest
        
        client = get_plaid_client()
        request = InvestmentsHoldingsGetRequest(access_token=access_token)
        response = client.investments_holdings_get(request)
        
        holdings = []
        securities_map = {s['security_id']: s for s in response.get('securities', [])}
        
        for holding in response.get('holdings', []):
            security = securities_map.get(holding['security_id'], {})
            holdings.append({
                'account_id': holding['account_id'],
                'security_id': holding['security_id'],
                'quantity': holding['quantity'],
                'institution_price': holding.get('institution_price'),
                'institution_value': holding.get('institution_value'),
                'cost_basis': holding.get('cost_basis'),
                'ticker_symbol': security.get('ticker_symbol'),
                'name': security.get('name'),
                'type': security.get('type'),
            })
        return holdings
    except Exception as e:
        print(f"Error fetching investment holdings: {e}")
        raise


async def get_investment_transactions(access_token: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict]:
    """
    Get investment transactions for an access token.
    Defaults to last 30 days if dates not provided.
    """
    if not PLAID_AVAILABLE:
        raise ImportError("plaid-python is not installed")
    
    try:
        from plaid.model.investments_transactions_get_request import InvestmentsTransactionsGetRequest
        
        client = get_plaid_client()
        
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)
        if not end_date:
            end_date = datetime.now()
        
        request = InvestmentsTransactionsGetRequest(
            access_token=access_token,
            start_date=start_date.date(),
            end_date=end_date.date()
        )
        response = client.investments_transactions_get(request)
        
        transactions = []
        for transaction in response.get('investment_transactions', []):
            transactions.append({
                'investment_transaction_id': transaction['investment_transaction_id'],
                'account_id': transaction['account_id'],
                'security_id': transaction.get('security_id'),
                'amount': transaction.get('amount'),
                'date': transaction['date'].isoformat() if hasattr(transaction['date'], 'isoformat') else str(transaction['date']),
                'name': transaction['name'],
                'type': transaction['type'],
                'subtype': transaction.get('subtype'),
                'quantity': transaction.get('quantity'),
                'price': transaction.get('price'),
            })
        return transactions
    except Exception as e:
        print(f"Error fetching investment transactions: {e}")
        raise
