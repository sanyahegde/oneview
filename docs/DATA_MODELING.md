# PortfolioAI Data Modeling

## Database Schema

### Core Entities

#### Users
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    full_name VARCHAR,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);
```

#### Accounts
```sql
CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    provider VARCHAR NOT NULL,
    provider_account_id VARCHAR NOT NULL,
    account_type accounttype NOT NULL,
    name VARCHAR,
    access_token VARCHAR,
    last_sync TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE TYPE accounttype AS ENUM ('brokerage', 'bank');
```

#### Holdings
```sql
CREATE TABLE holdings (
    id SERIAL PRIMARY KEY,
    account_id INTEGER REFERENCES accounts(id) ON DELETE CASCADE,
    symbol VARCHAR NOT NULL,
    quantity DECIMAL NOT NULL,
    avg_cost DECIMAL NOT NULL,
    current_price DECIMAL NOT NULL,
    value DECIMAL NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);
```

#### Transactions
```sql
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    account_id INTEGER REFERENCES accounts(id) ON DELETE CASCADE,
    symbol VARCHAR,
    type transactiontype NOT NULL,
    quantity DECIMAL,
    price DECIMAL,
    amount DECIMAL NOT NULL,
    date TIMESTAMP WITH TIME ZONE NOT NULL,
    description VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TYPE transactiontype AS ENUM ('buy', 'sell', 'dividend', 'deposit', 'withdrawal');
```

## Data Relationships

### Entity Relationship Diagram

```
Users (1) ──────── (N) Accounts (1) ──────── (N) Holdings
    │                    │
    │                    │
    │                    └─────────────────── (N) Transactions
    │
    └─────────────────────────────────────── (N) Snapshots
```

### Relationship Details

1. **User → Accounts**: One-to-Many
   - A user can have multiple linked accounts
   - Accounts are deleted when user is deleted (CASCADE)

2. **Account → Holdings**: One-to-Many
   - An account can have multiple holdings
   - Holdings are deleted when account is deleted (CASCADE)

3. **Account → Transactions**: One-to-Many
   - An account can have multiple transactions
   - Transactions are deleted when account is deleted (CASCADE)

4. **User → Snapshots**: One-to-Many
   - A user can have multiple portfolio snapshots
   - Snapshots track portfolio value over time

## Data Normalization

### Normalization Strategy
- **1NF**: All attributes contain atomic values
- **2NF**: No partial dependencies on composite keys
- **3NF**: No transitive dependencies

### Denormalization Considerations
- Holdings table includes calculated `value` field for performance
- Account names stored redundantly for quick access
- Current prices cached in holdings table

## Indexing Strategy

### Primary Indexes
```sql
-- Users table
CREATE INDEX idx_users_email ON users(email);

-- Accounts table
CREATE INDEX idx_accounts_user_id ON accounts(user_id);
CREATE INDEX idx_accounts_provider ON accounts(provider);

-- Holdings table
CREATE INDEX idx_holdings_account_id ON holdings(account_id);
CREATE INDEX idx_holdings_symbol ON holdings(symbol);

-- Transactions table
CREATE INDEX idx_transactions_account_id ON transactions(account_id);
CREATE INDEX idx_transactions_symbol ON transactions(symbol);
CREATE INDEX idx_transactions_date ON transactions(date);
CREATE INDEX idx_transactions_type ON transactions(type);
```

### Composite Indexes
```sql
-- For common query patterns
CREATE INDEX idx_transactions_account_date ON transactions(account_id, date DESC);
CREATE INDEX idx_holdings_account_symbol ON holdings(account_id, symbol);
```

## Data Types and Constraints

### Numeric Types
- **DECIMAL**: Used for monetary values (price, amount, quantity)
- **INTEGER**: Used for IDs and counts
- **BOOLEAN**: Used for flags (is_active)

### String Types
- **VARCHAR**: Used for variable-length text
- **TEXT**: Used for longer descriptions
- **ENUM**: Used for predefined categories

### Temporal Types
- **TIMESTAMP WITH TIME ZONE**: Used for all date/time fields
- **DATE**: Used for date-only fields

### Constraints
```sql
-- Not null constraints
ALTER TABLE users ALTER COLUMN email SET NOT NULL;
ALTER TABLE users ALTER COLUMN hashed_password SET NOT NULL;
ALTER TABLE accounts ALTER COLUMN provider SET NOT NULL;
ALTER TABLE accounts ALTER COLUMN provider_account_id SET NOT NULL;

-- Check constraints
ALTER TABLE holdings ADD CONSTRAINT chk_quantity_positive CHECK (quantity > 0);
ALTER TABLE holdings ADD CONSTRAINT chk_price_positive CHECK (current_price > 0);
ALTER TABLE transactions ADD CONSTRAINT chk_amount_positive CHECK (amount > 0);

-- Unique constraints
ALTER TABLE users ADD CONSTRAINT uk_users_email UNIQUE (email);
ALTER TABLE accounts ADD CONSTRAINT uk_accounts_provider_id UNIQUE (provider, provider_account_id);
```

## Data Validation

### Application-Level Validation
- Email format validation
- Password strength requirements
- Symbol format validation (uppercase, alphanumeric)
- Date range validation
- Numeric range validation

### Database-Level Validation
- Foreign key constraints
- Check constraints for positive values
- Unique constraints for business rules
- Not null constraints for required fields

## Data Migration Strategy

### Alembic Migrations
```python
# Example migration
def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

def downgrade():
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
```

### Migration Best Practices
- Always provide both upgrade and downgrade functions
- Use descriptive migration names
- Test migrations on copy of production data
- Backup database before major migrations
- Use transactions for atomic migrations

## Data Archiving Strategy

### Archival Policies
- **Transactions**: Archive after 7 years
- **Snapshots**: Archive after 3 years
- **Holdings**: Keep current data only
- **Accounts**: Archive inactive accounts after 1 year

### Archival Implementation
```sql
-- Create archive tables
CREATE TABLE transactions_archive (LIKE transactions);
CREATE TABLE snapshots_archive (LIKE snapshots);

-- Archive old data
INSERT INTO transactions_archive 
SELECT * FROM transactions 
WHERE date < NOW() - INTERVAL '7 years';

DELETE FROM transactions 
WHERE date < NOW() - INTERVAL '7 years';
```

## Performance Optimization

### Query Optimization
- Use appropriate indexes
- Avoid N+1 queries with eager loading
- Use database views for complex queries
- Implement query result caching

### Connection Pooling
```python
# SQLAlchemy connection pool configuration
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True,
    pool_recycle=3600
)
```

### Caching Strategy
- Redis for session storage
- Redis for frequently accessed data
- Application-level caching for computed values
- CDN for static assets

## Data Security

### Encryption
- Database connections use SSL/TLS
- Sensitive data encrypted at rest
- Passwords hashed with bcrypt
- API tokens encrypted in storage

### Access Control
- Role-based access control (RBAC)
- Row-level security (RLS) for multi-tenancy
- API rate limiting
- Audit logging for sensitive operations

### Backup and Recovery
- Daily automated backups
- Point-in-time recovery capability
- Cross-region backup replication
- Regular backup restoration testing

## Monitoring and Alerting

### Database Metrics
- Connection pool utilization
- Query performance metrics
- Index usage statistics
- Storage utilization

### Data Quality Monitoring
- Data validation rule violations
- Missing or null critical fields
- Data consistency checks
- Anomaly detection for financial data

### Alerting Thresholds
- Database connection failures
- Query performance degradation
- Storage space warnings
- Data quality violations
