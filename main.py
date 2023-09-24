from flask import Flask, render_template, request, jsonify, redirect
from flask_mail import Mail, Message
import requests
from flask_cors import CORS, cross_origin
import stripe
import boto3
import os
from dotenv import load_dotenv

app = Flask(__name__)
#site dev testing Mode varible for testing
dev_testing_mode = True

#Load Enviorment Variables for testing
if dev_testing_mode==True:
	load_dotenv()

#SQL Database Setup

digital_ocean_cors_config = {
    "origins": ["https://high-altitude-media-assets.nyc3.cdn.digitaloceanspaces.com"]
}


cors= CORS(app, resources={r"/deliverables": {"origins": "https://high-altitude-media-assets.nyc3.cdn.digitaloceanspaces.com"}})

#Mail Setup
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USER_NAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_SSL'] = True
#app.config['SECURITY_EMAIL_SENDER'] = 'zion.johnson@high-altitude-media.com'


#gmail app pass : zenerhdjmwwwodri
#zoho app pass : k6GHuPTqjNH6

mail = Mail(app)

#stripe setup
stripe.api_key = os.getenv('STRIPE_API_KEY') # Secret key create enviorment variable

'''
#Digital Ocean setup
session = boto3.session.Session()
client = session.client('s3',
                        region_name='nyc3',
                        endpoint_url='https://nyc3.digitaloceanspaces.com',
                        aws_access_key_id='DO00HE6V39NHU6ZC7WPM',
                        aws_secret_access_key='a8+PUQEANJcX7dwmHhIIWWBeX6Y/GqnnrOkyB3pwDC4')

response = client.list_buckets()
for space in response['Buckets']:
    print(space['Name'])

#https://high-altitude-media-assets.nyc3.cdn.digitaloceanspaces.com/example-property/skull.glb

response = client.list_objects(Bucket='high-altitude-media-assets')
for obj in response['Contents']:
    print(obj['Key'])

session = boto3.session.Session()

#dowload file from digital ocean
#client.download_file('high-altitude-media-assets','example-property/skull.glb', '/static/temp_data/test_model.glb')


s3_client = boto3.client('s3', region_name='nyc3', endpoint_url='https://nyc3.digitaloceanspaces.com', aws_access_key_id='DO00HE6V39NHU6ZC7WPM', aws_secret_access_key='a8+PUQEANJcX7dwmHhIIWWBeX6Y/GqnnrOkyB3pwDC4')

bucket_name = 'high-altitude-media-ass'
object_key = 'DJI_0001.JPG'
local_dest_path = 'static/temp_data/new-model.glb'

try:
    s3_client.download_file(bucket_name, object_key, local_dest_path)
    print(f"File downloaded successfully to {local_dest_path}")
except Exception as e:
    print(f"Error downloading file: {e}")
'''



@app.route('/')
def home():
    title = 'See Your Build'
    # add to the services overview desc
    services_Overview = 'Real Time Drone Services for Construction Progress Monitoring'
    return render_template('home.html',Title=title, Services_Overview=services_Overview)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/appointment-booking')
def appointmentBooking():
    return render_template('appointment-booking.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact_send_email', methods=['POST'])
def contact_send_email():
    client_name = request.form.get('client-name')
    client_email = request.form.get('client-email')
    client_phone = request.form.get('client-phone-number')

    project_location = request.form.get('property-location')
    project_Info = request.form.get('project-info-text-area')

    still_imaging_service = request.form.get('still-image-service')
    videography_service = request.form.get('videography-service')
    virtual_tour_service = request.form.get('virtual-tour-service')
    model_service = request.form.get('model-3d-service')
    undecided_service = request.form.get('unsure-service')

    #testing
    tst_msg = Message(f"Client Contact - {client_name}", sender=client_email, recipients=['zion.johnson@high-altitude-media.com'])
    tst_msg.body = f"Name: '{client_name}'\nEmail: {client_email}\nPhone: {client_phone}\nProject_Location: {project_location}\nProject_Info: {project_Info}\nStill_imaging_Service: {still_imaging_service}\nVideography_Service: {videography_service}\nVirtual_Tour_Service: {virtual_tour_service}\n3D_Modeling_Service: {model_service}\nUndecided_Service: {undecided_service}"

    #create a varible for storing email status notification
    status_notification = str()

    try:
        if not mail.is_connected:
            mail.connect()
            print(f'mail server connected: {mail.is_connected}')
            mail.send(tst_msg)
            status_notification = 'Contact Email Successfully sent. We will get back to soon!'
    except Exception as e:
        print("SMTP server connection failed:", str(e))
        status_notification = f'Error Sending Email: {str(e)}'
        return str(e)

    return render_template("home.html", notification=status_notification)

@cross_origin()
@app.route('/deliverables')
def client_deliverables():
    client_property_name = "Example Property Name"
    return render_template('client-deliverables-base.html')

# get 3d model data

@app.route('/get_model_data', methods=['GET'])
def get_data():
    return 'Hello'

@app.route('/construction-services')
def construction_services():
    return render_template('construction-services.html')

@app.route('/aerial-imaging-services')
def aerial_imaging_services():
    return render_template('aerial-imaging-services.html')

@app.route('/data-formats-provided')
def data_formats_provided():
    return render_template('/data-formats-provided.html')

@app.route('/portfolio')
def portfolio():
    return render_template('/portfolio.html')

# Payment Processor
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

# Need to create a debug mode for backend testing
# this route takes in a query Paramerter for product ex. /page?product='product ID'
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
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
			success_url= 'http://10.0.0.218:5000/payment-success',
			cancel_url= 'http://10.0.0.218:5000/payment-cancled',
			automatic_tax={'enabled': False},
		)

	except Exception as e:
		return str(e)
		
	return redirect(session.url, code=303)

# Payment Success Endpoint
@app.route('/payment-success', methods=['GET'])
def payment_success():
    return render_template('/payment_processing/payment_success.html')

# Payment Cancel Endpoint
@app.route('/payment-cancled', methods=['GET'])
def payment_cancled():
    return render_template('/payment_processing/payment_cancel.html')

# Check out page
@app.route('/service-check-out')
def service_checkout():
    return render_template('/payment_processing/checkout.html')

# comment this line out before pushing code to server.
#app.run(debug=True)

#Run in debug mode while testing
if dev_testing_mode==True:
    app.run(debug=True)

if __name__ == '__main__':
    app.run()