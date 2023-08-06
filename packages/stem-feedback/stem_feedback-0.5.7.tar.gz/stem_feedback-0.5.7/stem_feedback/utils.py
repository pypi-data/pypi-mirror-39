import json


def get_json_event(feed_back_type, subject, message, customer_id, customer_erp_id,
                   customer_name, user_id, user_name, email):
    json_str = dict()
    json_str['type'] = str(feed_back_type)
    json_str['subject'] = str(subject)
    json_str['message'] = str(message)
    cust = {"customer_id": customer_id, "customer_erp_id": customer_erp_id, "customer_name": customer_name}
    usr = {"user_id": user_id, "user_name": user_name, "email": email, "customer": cust}
    json_str['user'] = usr
    result = json.dumps(json_str)
    return result


def get_json_notification(feed_back_type, payment_type, subject, message, sum, currency_iso_id, currency_abbr,
                          customer_id, customer_erp_id, customer_name, user_id, user_name, email):
    json_str = dict()
    json_str['type'] = str(feed_back_type)
    json_str['subject'] = str(subject)
    json_str['message'] = str(message)
    cust = {"customer_id": customer_id, "customer_erp_id": customer_erp_id, "customer_name": customer_name}
    json_str['customer'] = cust
    usr = {"user_id": user_id, "user_name": user_name, "email": email, "customer": cust}
    json_str['user'] = usr
    cur = {
            'iso_id': currency_iso_id,
            'abbr': currency_abbr,
        }
    json_str['doc'] = {
        'payment_for': payment_type,
        'sum': sum,
        'currency': cur}
    return json_str