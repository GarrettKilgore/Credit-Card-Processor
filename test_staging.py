import requests
import os
import sys

URL = os.environ.get("STAGING_URL", "https://j1rbrsjcm6.execute-api.us-west-2.amazonaws.com/staging/processCard")

PASS = 0
FAIL = 0

def test(name, payload, expected):
    global PASS, FAIL
    try:
        response = requests.post(URL, json=payload, timeout=20)
        actual = response.text.strip()
        if expected.lower() in actual.lower():
            print(f"  PASS: {name} → {actual}")
            PASS += 1
        else:
            print(f"  FAIL: {name}")
            print(f"        Expected to contain: {expected}")
            print(f"        Got: {actual}")
            FAIL += 1
    except Exception as e:
        print(f"  FAIL: {name} → Exception: {e}")
        FAIL += 1


print("\n=== RUNNING STAGING TESTS ===\n")

# ─── MERCHANT AUTH TESTS ───
print("--- Merchant Auth ---")
test(
    "Valid merchant auth",
    {
        "bank": "Jeffs Bank",
        "merchant_name": "Contact Climbing",
        "merchant_token": "BqzXGsPJ",
        "card_holder": "Liam Carter",
        "cc_number": "4532756279624064",
        "card_type": "credit",
        "cvv": "648",
        "amount": "3.25",
        "card_zip": "84770",
        "exp_date": "04/28",
        "timestamp": "2026-04-27T00:00:00"
    },
    "Accepted"
)

test(
    "Invalid merchant token",
    {
        "bank": "Jeffs Bank",
        "merchant_name": "Contact Climbing",
        "merchant_token": "WRONGTOKEN",
        "card_holder": "Liam Carter",
        "cc_number": "4532756279624064",
        "card_type": "credit",
        "cvv": "648",
        "amount": "3.25",
        "card_zip": "84770",
        "exp_date": "04/28",
        "timestamp": "2026-04-27T00:00:00"
    },
    "Merchant Not Authorized"
)

test(
    "Missing merchant name",
    {
        "bank": "Jeffs Bank",
        "merchant_token": "BqzXGsPJ",
        "card_holder": "Liam Carter",
        "cc_number": "4532756279624064",
        "card_type": "credit",
        "cvv": "648",
        "amount": "3.25",
        "card_zip": "84770",
        "exp_date": "04/28",
        "timestamp": "2026-04-27T00:00:00"
    },
    "Merchant Not Authorized"
)

# ─── GOOD TRANSACTIONS ───
print("\n--- Good Transactions ---")
test(
    "Jeff's Bank credit accepted",
    {
        "bank": "Jeffs Bank",
        "merchant_name": "Contact Climbing",
        "merchant_token": "BqzXGsPJ",
        "card_holder": "Liam Carter",
        "cc_number": "4532756279624064",
        "card_type": "credit",
        "cvv": "648",
        "amount": "3.25",
        "card_zip": "84770",
        "exp_date": "04/28",
        "timestamp": "2026-04-27T00:00:00"
    },
    "Accepted"
)

test(
    "Jeff's Bank debit accepted",
    {
        "bank": "Jeffs Bank",
        "merchant_name": "Contact Climbing",
        "merchant_token": "BqzXGsPJ",
        "card_holder": "Isabella Martinez",
        "cc_number": "4556318984301377",
        "card_type": "debit",
        "cvv": "118",
        "amount": "3.25",
        "card_zip": "84097",
        "exp_date": "06/29",
        "timestamp": "2026-04-27T00:00:00"
    },
    "Accepted"
)

test(
    "CaliBear accepted",
    {
        "bank": "CaliBear",
        "merchant_name": "Contact Climbing",
        "merchant_token": "BqzXGsPJ",
        "card_holder": "michael abraham",
        "cc_number": "9594406409097439",
        "card_type": "debit",
        "cvv": "184",
        "amount": "3.25",
        "card_zip": "84770",
        "exp_date": "04/28",
        "timestamp": "2026-04-27T00:00:00"
    },
    "Accepted"
)

test(
    "Corbin accepted",
    {
        "bank": "Corbin",
        "merchant_name": "Contact Climbing",
        "merchant_token": "BqzXGsPJ",
        "card_holder": "Jeff Compas",
        "cc_number": "4539370182645290",
        "card_type": "debit",
        "cvv": "673",
        "amount": "3.25",
        "card_zip": "32301",
        "exp_date": "05/28",
        "timestamp": "2026-04-27T00:00:00"
    },
    "Approved"  # Corbin returns "Approved." not "Accepted."
)

test(
    "Wild West Bank accepted",
    {
        "bank": "Wild West Bank",
        "merchant_name": "Contact Climbing",
        "merchant_token": "BqzXGsPJ",
        "card_holder": "Liam Carter",
        "cc_number": "3175908426",
        "card_type": "debit",
        "cvv": "648",
        "amount": "3.25",
        "card_zip": "84770",
        "exp_date": "04/28",
        "timestamp": "2026-04-27T00:00:00"
    },
    "Approved"  # Wild West returns "Approved." not "Accepted."
)

test(
    "Topher's Bank accepted",
    {
        "bank": "Tophers Bank",
        "merchant_name": "Contact Climbing",
        "merchant_token": "BqzXGsPJ",
        "card_holder": "Diana Osei",
        "cc_number": "4916338506082839",
        "card_type": "credit",
        "cvv": "a4d0f625",
        "amount": "3.25",
        "card_zip": "84770",
        "exp_date": "2028-06",
        "timestamp": "2026-04-27T00:00:00"
    },
    "Accepted"
)

# ─── DECLINE TESTS ───
print("\n--- Decline Tests ---")
test(
    "Bad CVV returns Declined",
    {
        "bank": "Jeffs Bank",
        "merchant_name": "Contact Climbing",
        "merchant_token": "BqzXGsPJ",
        "card_holder": "Liam Carter",
        "cc_number": "4532756279624064",
        "card_type": "credit",
        "cvv": "999",
        "amount": "3.25",
        "card_zip": "84770",
        "exp_date": "04/28",
        "timestamp": "2026-04-27T00:00:00"
    },
    "Declined"
)

test(
    "Bad card number returns Declined",
    {
        "bank": "Jeffs Bank",
        "merchant_name": "Contact Climbing",
        "merchant_token": "BqzXGsPJ",
        "card_holder": "Liam Carter",
        "cc_number": "0000000000000000",
        "card_type": "credit",
        "cvv": "648",
        "amount": "3.25",
        "card_zip": "84770",
        "exp_date": "04/28",
        "timestamp": "2026-04-27T00:00:00"
    },
    "Declined"
)

test(
    "Insufficient funds returns Declined",
    {
        "bank": "Jeffs Bank",
        "merchant_name": "Contact Climbing",
        "merchant_token": "BqzXGsPJ",
        "card_holder": "Liam Carter",
        "cc_number": "4532756279624064",
        "card_type": "credit",
        "cvv": "648",
        "amount": "99999.00",
        "card_zip": "84770",
        "exp_date": "04/28",
        "timestamp": "2026-04-27T00:00:00"
    },
    "Declined"
)

# ─── BAD PAYLOAD TESTS ───
print("\n--- Bad Payload Tests ---")
test(
    "Empty body",
    {},
    "Merchant Not Authorized"
)

test(
    "Unknown bank",
    {
        "bank": "Fake Bank",
        "merchant_name": "Contact Climbing",
        "merchant_token": "BqzXGsPJ",
        "card_holder": "Liam Carter",
        "cc_number": "4532756279624064",
        "card_type": "credit",
        "cvv": "648",
        "amount": "3.25",
        "card_zip": "84770",
        "exp_date": "04/28",
        "timestamp": "2026-04-27T00:00:00"
    },
    "Declined"
)

# ─── SUMMARY ───
print(f"\n=== RESULTS: {PASS} passed, {FAIL} failed ===\n")

if FAIL > 0:
    sys.exit(1)
