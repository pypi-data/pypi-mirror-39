"""A simple example of how to access the Google Analytics API."""

import argparse,datetime
from settings import *
from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

import httplib2
import json
import smtplib
import os
import operator
from flask import Flask, render_template, request, jsonify
from oauth2client import client
from oauth2client import file
from oauth2client import tools
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

realtime_var = -1
gn_realtime_var = -1


def get_service(api_name, api_version, scope, key_file_location, service_account_email):
   """Get a service that communicates to a Google API.

   Args:
       api_name: The name of the api to connect to.
       api_version: The api version to connect to.
       scope: A list auth scopes to authorize for the application.
       key_file_location: The path to a valid service account p12 key file.
       service_account_email: The service account email address.

   Returns:
       A service that is connected to the specified API.
   """

   f = open(key_file_location, 'rb')
   key = f.read()
   f.close()

   credentials = SignedJwtAssertionCredentials(service_account_email, key, scope=scope)

   http = credentials.authorize(httplib2.Http())

   # Build the service object.
   service = build(api_name, api_version, http=http)

   return service


def get_results(service, profile_id):
   # Use the Analytics Service Object to query the Core Reporting API
   # for the number of sessions within the past seven days.
   return service.data().realtime().get(
           ids='ga:' + profile_id,
           metrics='rt:pageviews',
           dimensions='rt:pagePath',
           sort='-rt:pageviews'
           ).execute()


ga.query.metrics(
    expression='rt:pageviews'
).dimensions(
    name='rt:pagePath'
)


def print_results(results):
   # Print data nicely for the user.
   print results
   if results:
       print 'Realtime : %s' % results.get('totalsForAllResults').get('rt:activeUsers')
       print 'Sources : %s' % results.get('rows')
       rt = dict(results.get("rows"))
       print rt
       for i in sorted(rt, key=rt.get, reverse=True):
           print i, rt[i]
       #if int(results.get('totalsForAllResults').get('rt:activeUsers')) < ACTIVE_USERS_LIMIT:
       #    send_mail(results)

   else:
       print 'No results found'


def initiate_traffic_mailer():
   # Define the auth scopes to request.
   scope = ['https://www.googleapis.com/auth/analytics.readonly']

   # Use the developer console and replace the values with your
   # service account email and relative location of your key file.
   service_account_email = '324965955598-9vdf04c9h4jl0peseetl1fkbvahqpsoj@developer.gserviceaccount.com'
   key_file_location = 'privatekey.pem'

   # Authenticate and construct service.
   service = get_service('analytics', 'v3', scope, key_file_location, service_account_email)
   profile = '81174499'#get_first_profile_id(service)
   #print profile
   result = get_results(service, profile)
   print_results(result)
   return result
