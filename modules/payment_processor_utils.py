import stripe
import os

# Payment Processor

#stripe setup
stripe.api_key = os.getenv('STRIPE_API_KEY') # Secret key create enviorment variable

# Return session URL
def handle_create_checkout_session(request, dev_testing_mode) -> str :
    # make condition if there is not a product ID
    productID = request.args.get('product')
    paymentMode = request.args.get('mode') # mode can only be subcription

    domain = 'www.high-altitude-media.com'
    

    if dev_testing_mode == True:
        domain = 'http://10.0.0.218:5000'

    url_success = domain + '/payment-success'
    url_cancel = domain + '/payment-cancled'


    print(paymentMode)
    try:
        session = stripe.checkout.Session.create(
            line_items=[
                {
                # provide Price ID (ex. pr_1234) of the product i want to sell
                "price": productID,
                "quantity": 1,
                },
            ],
            mode= f'{paymentMode}',
            success_url= url_success,
            cancel_url= url_cancel,
            automatic_tax={'enabled': False},
        )

    except Exception as e:
        return str(e)
        
    return session.url


'''
#Testing Stripe API
@app.route('/payment', methods=['GET'])
def Payment():
    #Get customers and print them out.
    customers = stripe.Customer.list()
    #emails = [Customer['email'] for customer in customers]
    #emails = stripe.Customer.data
    
    return jsonify(customers['data'][0]['email']), 200
'''