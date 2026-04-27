import json
import boto3
import urllib3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
merchant_table = dynamodb.Table('Merchant')
log_table = dynamodb.Table('Transaction')

http = urllib3.PoolManager()

JEFFS_URL      = "https://9q350g4063.execute-api.us-west-2.amazonaws.com/default/handleTransaction"
TOPHERS_URL    = "https://lp4uqktsqg.execute-api.us-west-2.amazonaws.com/default/doRequest"
WILDWEST_URL   = "https://l25ft7pzu5wpwm3xtskoiks6rm0javto.lambda-url.us-west-2.on.aws/"
CALIBEAR_URL   = "https://api.calibear.credit/transaction/"
CORBIN_URL     = "https://xbu6ixwga4.execute-api.us-west-2.amazonaws.com/default/handleTransaction"
JANK_URL       = "https://yt1i4wstmb.execute-api.us-west-2.amazonaws.com/default/transact"


def write_transaction_log(merchant_name, bank_name, card_number, amount, status):
    try:
        log_table.put_item(Item={
            "TransactionId": str(uuid.uuid4()),
            "merchant_name": merchant_name or "Unknown",
            "bank_name": bank_name or "Unknown",
            "card_last4": card_number[-4:] if card_number else "0000",
            "amount": amount or "0",
            "timestamp": datetime.utcnow().isoformat(),
            "status": status
        })
    except Exception as e:
        print("Error writing transaction log:", str(e))


def lambda_handler(event, context):
    try:
        inbound = json.loads(event.get("body", "{}"))
    except:
        inbound = {}

    merchant_name = inbound.get("merchant_name")
    merchant_token = inbound.get("merchant_token")

    # Authenticate merchant
    response = merchant_table.get_item(Key={"Name": merchant_name, "Token": merchant_token})
    if "Item" not in response:
        write_transaction_log(merchant_name, inbound.get("bank"), inbound.get("cc_number"), inbound.get("amount"), "Error")
        return respond("Merchant Not Authorized.")

    # Route to correct bank
    bank = inbound.get("bank", "").strip()
    status, bank_body = call_bank_for(bank, inbound)
    final_message = translate_response(bank, status, bank_body)

    log_status = "Approved" if "Accepted" in final_message or "successful" in final_message.lower() else "Declined"
    write_transaction_log(merchant_name, bank, inbound.get("cc_number"), inbound.get("amount"), log_status)

    return respond(final_message)


def respond(message):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/plain"},
        "body": message
    }


def call_bank_for(bank, inbound):
    bank_lower = bank.lower()

    if "jeff" in bank_lower:
        return call_jeffs_bank(inbound)
    elif "topher" in bank_lower:
        return call_tophers_bank(inbound)
    elif "wild west" in bank_lower:
        return call_wild_west_bank(inbound)
    elif "cali" in bank_lower:
        return call_calibear_bank(inbound)
    elif "corbin" in bank_lower:
        return call_corbin_bank(inbound)
    elif "jank" in bank_lower or "joseph" in bank_lower:
        return call_jank_bank(inbound)
    else:
        return 400, json.dumps({"message": "Unknown bank: " + bank})


def call_jeffs_bank(inbound):
    payload = {
        "cch_name": "kilgore_cch",
        "cch_token": "PrkIwzc7",
        "card_holder": s(inbound.get("card_holder")),
        "card_num": s(inbound.get("cc_number")),
        "exp_date": s(inbound.get("exp_date")),
        "cvv": s(inbound.get("cvv")),
        "card_zip": s(inbound.get("card_zip")),
        "txn_type": s(inbound.get("card_type")),
        "merchant": s(inbound.get("merchant_name")),
        "amount": s(inbound.get("amount")),
        "timestamp": s(inbound.get("timestamp"))
    }
    return post_json(JEFFS_URL, payload)


def call_tophers_bank(inbound):
    card_type = s(inbound.get("card_type")).lower()
    is_withdrawal = card_type != "deposit"
    txn_type = "credit" if card_type == "credit" else "debit"

    payload = {
        "cch_name": "gkilgore_cch",
        "cch_token": "B7xU8iLc",
        "card_number": s(inbound.get("cc_number")),
        "cvv": s(inbound.get("cvv")),
        "exp_date": s(inbound.get("exp_date")),
        "amount": to_float(inbound.get("amount")),
        "transaction_type": txn_type,
        "merchant_name": s(inbound.get("merchant_name")),
        "withdrawal": is_withdrawal
    }
    return post_json(TOPHERS_URL, payload)


def call_wild_west_bank(inbound):
    card_type = s(inbound.get("card_type")).lower()
    txn_type = "deposit" if card_type == "deposit" else "withdrawal"
    card_type_field = "credit" if card_type == "credit" else "debit"

    payload = {
        "cch_name": "kilgore_cch",
        "cch_token": "w5N2kH8P",
        "account_holder_name": s(inbound.get("card_holder")),
        "account_number": s(inbound.get("cc_number")),
        "transaction_type": txn_type,
        "card_type": card_type_field,
        "amount": s(inbound.get("amount"))
    }
    return post_json(WILDWEST_URL, payload)


def call_calibear_bank(inbound):
    card_type = s(inbound.get("card_type")).lower()
    txn_type = "deposit" if card_type == "deposit" else "withdrawal"

    payload = {
        "clearinghouse_id": "CH-cxll4zklooke",
        "card_number": s(inbound.get("cc_number")),
        "amount": to_float(inbound.get("amount")),
        "transaction_type": txn_type,
        "merchant_name": s(inbound.get("merchant_name"))
    }
    headers = {
        "Content-Type": "application/json",
        "x-api-key": "credential_token_p7y6wktakpuxqphr62gdswm"
    }
    return post_json(CALIBEAR_URL, payload, headers=headers)


def call_corbin_bank(inbound):
    card_type = s(inbound.get("card_type")).lower()
    txn_type = "withdrawal" if card_type != "deposit" else "deposit"

    payload = {
        "account_num": s(inbound.get("cc_number")),
        "cvv": s(inbound.get("cvv")),
        "exp_date": s(inbound.get("exp_date")),
        "amount": s(inbound.get("amount")),
        "transaction_type": txn_type,
        "card_type": "credit" if card_type == "credit" else "debit"
    }
    headers = {
        "Content-Type": "application/json",
        "username": "gkilgore",
        "password": "o-JF!?jVoX@5osZt"
    }
    return post_json(CORBIN_URL, payload, headers=headers)


def call_jank_bank(inbound):
    card_type = s(inbound.get("card_type")).lower()

    payload = {
        "cch_name": "gkilgore",
        "cch_token": "ESQgunwZUqgW7HkjYmWk5V7l2Sm7M30t",
        "account_num": s(inbound.get("cc_number")),
        "card_num": s(inbound.get("cc_number")),
        "exp_date": s(inbound.get("exp_date")),
        "cvv": s(inbound.get("cvv")),
        "amount": s(inbound.get("amount")),
        "type": card_type,
        "merchant": s(inbound.get("merchant_name"))
    }
    return post_json(JANK_URL, payload)

def post_json(url, payload, headers=None):
    if headers is None:
        headers = {"Content-Type": "application/json"}

    print(f"POST {url}")
    print("Payload:", json.dumps(payload))

    try:
        encoded = json.dumps(payload).encode("utf-8")
        response = http.request("POST", url, body=encoded, headers=headers)
        body = response.data.decode("utf-8")
        print(f"Response {response.status}: {body}")
        return response.status, body
    except Exception as e:
        print("HTTP error:", str(e))
        return 500, json.dumps({"message": "Error contacting bank"})


def translate_response(bank, status, body):
    print(f"translate_response: bank={bank}, status={status}, body={body}")

    bank_lower = bank.lower()

    if "wild west" in bank_lower:
        return translate_wild_west(status, body)
    elif "cali" in bank_lower:
        return translate_calibear(status, body)
    elif "topher" in bank_lower:
        return translate_tophers(status, body)
    elif "corbin" in bank_lower:
        return translate_corbin(status, body)
    else:
        return translate_jeffs_format(status, body)


def translate_jeffs_format(status, body):
    try:
        parsed = json.loads(body)
        message = parsed.get("message", body)
    except:
        message = body

    if status == 200:
        return message
    if status == 401:
        return "Declined - clearinghouse not authorized"
    if status == 400:
        return "Declined - bad request"
    if status == 404:
        return "Declined - Do Not Honor"
    if status == 403:
        return "Declined - Insufficient Funds"
    return "Declined - unknown error"


def translate_tophers(status, body):
    try:
        parsed = json.loads(body)
        outcome = parsed.get("outcome", "")
        message = parsed.get("message", body)
    except:
        outcome = ""
        message = body

    if status == 200:
        if outcome == "accepted":
            return "Accepted."
        return f"Declined - {message}"
    if status == 401:
        return "Declined - clearinghouse not authorized"
    if status == 400:
        return "Declined - bad request"
    if status == 404:
        return "Declined - Do Not Honor"
    if status == 422:
        return "Declined - Card Verification Unsuccessful"
    return "Declined - unknown error"


def translate_wild_west(status, body):
    try:
        outer = json.loads(body)
        inner_str = outer.get("body", body)
        if isinstance(inner_str, str):
            inner = json.loads(inner_str)
        else:
            inner = inner_str
        message = inner.get("message", body)
    except:
        message = body

    if status == 200:
        if "successful" in message.lower():
            return "Accepted."
        return message
    if status == 401:
        return "Declined - clearinghouse not authorized"
    if status == 400:
        return "Declined - bad request"
    return "Declined - unknown error"


def translate_calibear(status, body):
    try:
        parsed = json.loads(body)
        message = parsed.get("message", body)
    except:
        message = body

    if status == 200 and message == "APPROVED":
        return "Accepted."
    if status == 403:
        return f"Declined - {message}"
    if status == 401:
        return "Declined - clearinghouse not authorized"
    if status == 400:
        return "Declined - bad request"
    if status == 404:
        return "Declined - Do Not Honor"
    return "Declined - unknown error"


def translate_corbin(status, body):
    try:
        parsed = json.loads(body)
        message = parsed.get("message", body)
    except:
        message = body

    if status == 202:
        return "Accepted."
    if status == 200:
        return message
    if status == 401:
        return "Declined - clearinghouse not authorized"
    if status == 400:
        return "Declined - bad request"
    if status == 402:
        return "Declined - Insufficient Funds"
    if status == 404:
        return f"Declined - {message}"
    return "Declined - unknown error"

def s(val):
    return str(val) if val is not None else ""

def to_float(val):
    try:
        return float(val)
    except:
        return 0.0