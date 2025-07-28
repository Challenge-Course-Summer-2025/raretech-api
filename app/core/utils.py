from decimal import Decimal

def decimal_to_float(item: dict) -> dict:

    # DynamoDBから取得したデータのDecimal型をfloat/intに変換
    for key, value in item.items():
        if isinstance(value, Decimal):
            if value % 1 == 0:
                item[key] = int(value)
            else:
                item[key] = float(value)
        elif isinstance(value, dict):
            item[key] = decimal_to_float(value)
        elif isinstance(value, list):
            item[key] = [decimal_to_float(i) if isinstance(i, dict) else i for i in value]
    return item
