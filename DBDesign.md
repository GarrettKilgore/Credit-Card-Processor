# Credit Card Processor Database Design

## Data Organization

---

## 1. Merchant Table
Purpose: Keep track of merchant information including authentication and banking details.

**Partition Key:** MerchantID (String)  
**Sort Key:** AuthToken (String)

**Other Attributes:**
- MerchantName (String)
- BankID (String) — reference to Bank table
- MerchantAccountNumber (String)
- Status (String)

**Rationale:**
- MerchantID prevents duplicate or misspelled merchant names.
- AuthToken as sort key allows token rotation while keeping the same MerchantID.
- BankID enforces referential integrity and prevents typos like “WElls Fargo”.
- Account numbers stored as strings preserve formatting and leading zeros.

---

## 2. Bank Table
Purpose: Master list of banks and their API integration information.

**Partition Key:** BankID (String)

**Other Attributes:**
- BankName (String)
- APIEndpoint (String)
- APIKey (String)
- Status (String)

**Rationale:**
- Standardized BankID eliminates spelling errors.
- Centralized API configuration allows updates without modifying merchant or transaction data.
- Application validates BankID before writes to prevent invalid references.

---

## 3. Transaction Table
Purpose: Records all transaction attempts for customer and merchant banks.

**Partition Key:** TransactionID (String)

**Other Attributes:**
- MerchantID (String)
- CreditCardNumber (String)
- CustomerBankID (String)
- MerchantBankID (String)
- Amount (Number) — stored in cents
- Timestamp (String)
- Status (String)
- AuthToken (String)
- ResponseCode (String)
- ResponseMessage (String)

**Rationale:**
- Credit card numbers stored as strings preserve leading zeros and avoid numeric overflow.
- Amount stored in cents avoids floating‑point precision errors.
- Separate customer and merchant bank fields track both sides of the transaction.
- Timestamp supports chronological sorting and future GSIs.

---

## Key Design Decisions

### Why String for Credit Card Numbers?
- Preserves leading zeros  
- Not used in math  
- Prevents overflow  
- Easier to tokenize  

### How to Handle Bank Identification?
- Use BankID instead of names to prevent typos  
- Validate BankID against Bank table  
- Controlled vocabulary eliminates human error  

### Fixing Bad Data?
- Validate inputs before writes  
- Normalize simple formatting issues  
- Do not silently “fix” critical data  
- Log validation failures for debugging  
