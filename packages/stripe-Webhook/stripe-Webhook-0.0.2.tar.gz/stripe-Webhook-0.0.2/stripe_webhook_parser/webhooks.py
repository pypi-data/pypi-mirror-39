from flask import request, Blueprint
from stripe_webhook_parser.events import _plan_created, _plan_updated, _plan_deleted
from stripe_webhook_parser.events import _product_created, _product_updated, _product_deleted
from stripe_webhook_parser.events import _customer_subscription_created, _customer_subscription_deleted
from stripe_webhook_parser.events import _invoice_payment_succeed
from stripe_webhook_parser.events import _charge_succeeded
from stripe_webhook_parser.events import _customer_created, _customer_updated, _customer_deleted
import stripe
import os
import json


webhook_secret = os.environ.get('WEBHOOK_SECRET')
webhook = Blueprint('webhook', __name__)
stripe.api_key = "STRIPE_KEY_TEST"

@webhook.route('/webhooks', methods=['POST'])
def webhooks():
    payload = request.data
    event_json = json.loads(request.data)
    received_sig = request.headers.get('Stripe-Signature', None)
    sig_header = request.headers
    print("Type sig_header:", type(sig_header))
    # print(type(received_sig))
    # print(event_json)
    # print("Received event: id={id}, type={type}".format(id=event_json['id'], type=event_json['type']))
    dec = payload.decode(encoding='UTF-8')

    # TODO : Verification signature a check

    # if stripe.Event.retrieve(event_json['id']) == None:
    #     return 400
    # else:

    # try:
    #     event = stripe.Webhook.construct_event(dec, sig_header, webhook_secret)
    # except ValueError as e:
    #     print(e)
    #     return 'invalid payload', 400
    # except stripe.error.SignatureVerificationError as e:
    #     print(e)
    #     return 'invalid signature', 400

    #  product.created

    #
    # if event_json['type'] == "plan.created":
    #     print("its a plaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaan")
    # else:
    #     print("not a plan")
    # check_event(event_json)

    check_event(event_json)

    return 'got it', 200


def check_event(event_json):

    functions = {
        "plan.created": _plan_created,
        "plan.updated": _plan_updated,
        "plan.deleted": _plan_deleted,
        "product.created": _product_created,
        "product.updated": _product_updated,
        "product.deleted": _product_deleted,
        "customer.subscription.created": _customer_subscription_created,
        "customer.subscription.deleted": _customer_subscription_deleted,
        "invoice.payment_succeeded": _invoice_payment_succeed,
        "charge.succeeded": _charge_succeeded,
        "customer.created": _customer_created,
        "customer.deleted": _customer_deleted,
        "customer.updated": _customer_updated
    }

    if event_json['type'] in functions:
        result = functions[event_json['type']](event_json)
    else:
        print("We currently don\'t manage this event")
        result = None
    return result
