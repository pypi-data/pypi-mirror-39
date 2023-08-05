
# TODO dont forget to remove the comment after integration in the project

def _plan_created(event_json):
    response = Plan.post('/newplan', body=event_json)
    print("Plan created")
    return event_json


def _plan_updated(event_json):
    # response = Plan.put('/updateplan', body=event_json)
    print("plan updated")
    return 200


def _plan_deleted(event_json):
    # response = Plan.delete('/delplan', body=event_json)
    print("plan deleted")
    return 200


def _product_created(event_json):
    # response = Product.post('/newproduct', body=event_json)
    print("product created")
    return 200


def _product_updated(event_json):
    # response = Product.put('/updateproduct', body=event_json)
    print("product updated")
    return 200


def _product_deleted(event_json):
    # response = Product.delete('/delproduct', body=event_json)
    print("product deleted")
    return 200


def _customer_subscription_created(event_json):
    # response = Subscription.put('/createcustomersub', body=event_json)
    print("subscription created for customer")
    return 200


def _customer_subscription_deleted(event_json):
    # response = Product.delete('/delcustonersub', body=event_json) TODO no stripe, out of webhooks
    print("subscription deleted for customer")
    return 200


def _invoice_payment_succeed(event_json):
    # TODO : a voir la deuxieme devrait fonctionner
    # response = Subscription.put('/subscription/event_json['subscription'], body=event_json)
    # response = Subscription.put('/createcustomersub', body=event_json)
    print("invoice payment succeed")
    return 200


# TODO : not sure for now, to do after thinking aout it
def _charge_succeeded(event_json):
    # response = Charge.put('/chargesucceed, body=event_json)
    print("charge payment succeed")
    return 200


def _customer_created(event_json):
    # response = User.put('/newcustomer, body=event_json)
    print("customer created")
    return 200


def _customer_updated(event_json):
    # response = User.put('/updatesourcecustomer, body=event_json) TODO wait and see should be handle out of webhooks
    print("customer succesfully updated")
    return 200


def _customer_deleted(event_json):
    # response = User.put('/deletecustomer, body=event_json) TODO modif user to delete the customer id, out of webhooks
    print("customer deleted")
    return 200


def _create_connected_acc(event_json):
    # response = User.put('/newconnectedacc', body=event_json)
    print("connected account created")


def _update_connected_acc(event_json):
    # response = User.put('/updateconnectedacc', body=event_json)
    print("connected account updated")
