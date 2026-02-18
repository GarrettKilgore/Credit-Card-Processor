# Credit Card Processor Database Design

## Data Organization

### 1. Merchant Table
**Purpose**: Keep track of merchant information including authentication and banking details.

**Partition Key**: MerchantID (String)  
**Sort Key**: AuthToken (String)

**Other Attributes**:
- MerchantName (String)
- BankID (String) - Reference to Bank table
- MerchantAccountNumber (String)
- Status (String) - Active/Inactive

**Rationale**: 
- Using MerchantID instead of name prevents duplicate business names and provides stable identifier
- AuthToken as sort key allows for token rotation while keeping same MerchantID
- BankID prevents typos like "WElls Fargo" vs "Wells Fargo" - enforces referential integrity
- Account numbers as strings preserve leading zeros

---

### 2. Bank Table
**Purpose**: Master list of banks and their API integration information.

**Partition Key**: BankID (String)  
**Sort Key**: BankID (String)

**Other Attributes**:
- BankName (String)
- APIEndpoint (String)
- APIKey (String)
- Status (String) - Active/Inactive

**Rationale**:
- Standardized BankID (e.g., "WELLS_FARGO", "CHASE") eliminates spelling errors
- Centralized API configuration - easy to update without touching merchant/transaction data
- Application validates BankID against this table to prevent invalid references

---

### 3. Transaction Table
**Purpose**: Records all transaction attempts for customer and merchant banks.

**Partition Key**: TransactionID (String)  
**Sort Key**: Timestamp (String)

**Other Attributes**:
- MerchantID (String)
- CreditCardNumber (String) - encrypted/tokenized
- CustomerBankID (String) - Customer's credit card bank
- MerchantBankID (String) - Merchant's deposit bank
- Amount (Number) - In cents to avoid floating-point errors
- Status (String) - Pending/Approved/Declined/Failed
- AuthToken (String)
- ResponseCode (String)
- ResponseMessage (String)

**Rationale**:
- **Credit card as String**: Preserves leading zeros, not used in math operations, prevents overflow
- **Amount in cents**: Avoids floating-point precision errors in financial calculations
- Separate customer and merchant bank fields track both sides of transaction
- Timestamp as sort key enables efficient time-range queries

---

## Key Design Decisions

**Why String for Credit Card Numbers?**
- Preserves leading zeros
- Not used in mathematical operations
- Prevents overflow issues
- Easier to format and tokenize

**How to Handle Bank Identification?**
- Use BankID instead of names to prevent typos (WElls vs Wells)
- Application validates BankID against Bank table before writes
- Controlled vocabulary eliminates human error

**Fixing Bad Data?**
- **Do**: Validate inputs before writes (check BankID exists, amounts are positive)
- **Do**: Normalize simple things (trim whitespace, standardize BankID format)
- **Don't**: Silently fix critical data - fail loudly with clear errors
- **Always**: Log validation failures for debugging
