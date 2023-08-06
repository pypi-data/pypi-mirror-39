# -*- coding: utf-8 -*-
""" Simple Mercedes me API.

Attributes:
    username (int): mercedes me username (email)
    password (string): mercedes me password
    update_interval (int): min update intervall in seconds

"""

import json
import time
from multiprocessing import RLock
import requests
import lxml.html
# from mbwebapppy import Exceptions as mbmeExc

SERVER_UI = "https://ui.meapp.secure.mercedes-benz.com"
SERVER_LOGIN = "https://login.secure.mercedes-benz.com"
SERVER_APP = "https://app.secure.mercedes-benz.com"
SERVER_API = "https://api.secure.mercedes-benz.com"

ME_STATUS_URL = "{0}/backend/users/identity".format(SERVER_APP)
CAR_STATUS_URL = "{0}/backend/vehicles/%s/status".format(SERVER_APP)
CAR_DETAIL_URL = "{0}/backend/vehicles/%s/converant".format(SERVER_APP)
ME_LOCATION_URL = "{0}/backend/vehicles/%s/location/v2".format(SERVER_APP)
LOGIN_STEP1_URL = "{0}/session/login?app-id=VHPMBCON.PRODEC".format(SERVER_APP)
LOGIN_STEP2_URL = "/wl/login"
LOGIN_STEP3_URL = "{0}/oidc10/auth/oauth/v2/authorize/consent".format(SERVER_API)

CONTENT_TYPE_JSON = "application/json;charset=UTF-8"

DEBUG_MODE = False

# Set to False for testing with tools like fiddler
# Change to True for production
LOGIN_VERIFY_SSL_CERT = True


class Car(object):
    def __init__(self):
        self.licenseplate = None
        self.finorvin = None
        self.salesdesignation = None
        self.nickname = None
        self.modelyear = None
        self.colorname = None
        self.fueltype = None
        self.powerhp = None
        self.powerkw = None
        self.numberofdoors = None
        self.numberofseats = None
        self.tires = None
        self.odometer = None
        self.fuellevelpercent = None
        self.doors = None
        self.stateofcharge = None
        self.location = None

class StateOfObject(object):
    def __init__(self, unit=None, value=None, retrievalstatus=None, timestamp=None):
        self.unit = None
        self.value = None
        self.retrievalstatus = None
        self.timestamp = None
        if unit is not None:
            self.unit = unit
        if value is not None:
            self.value = value
        if retrievalstatus is not None:
            self.retrievalstatus = retrievalstatus
        if timestamp is not None:
            self.timestamp = timestamp

class Odometer(object):
    def __init__(self):
        self.odometer = None
        self.distancesincereset = None
        self.distancesincestart = None

class Tires(object):
    def __init__(self):
        self.tirepressurefrontleft = None
        self.tirepressurefrontright = None
        self.tirepressurerearleft = None
        self.tirepressurerearright = None

class Doors(object):
    def __init__(self):
        self.doorstatusfrontleft = None
        self.doorstatusfrontright = None
        self.doorstatusrearleft = None
        self.doorstatusrearright = None
        self.doorlockstatusfrontleft = None
        self.doorlockstatusfrontright = None
        self.doorlockstatusrearleft = None
        self.doorlockstatusrearright = None
        self.doorlockstatusdecklid = None
        self.doorlockstatusgas = None
        self.doorlockstatusvehicle = None

class Location(object):
    def __init__(self, latitude=None, longitude=None, heading=None):
        self.latitude = None
        self.longitude = None
        self.heading = None
        if latitude is not None:
            self.latitude = latitude
        if longitude is not None:
            self.longitude = longitude
        if heading is not None:
            self.heading = heading

class CarAttribute(object):
    def __init__(self, value, retrievalstatus, timestamp):
        self.value = value
        self.retrievalstatus = retrievalstatus
        self.timestamp = timestamp

class Controller(object):
    """ Simple Mercedes me API.
    """
    def __init__(self, username, password, update_interval):

        self.__lock = RLock()
        self.cars = []
        self.update_interval = update_interval
        self.is_valid_session = False
        self.last_update_time = 0
        self.session = requests.session()
        self.session_cookies = self._get_session_cookies(username, password)
        if self.is_valid_session:
            self._get_cars()


    def update(self):
        """ Simple Mercedes me API.

        """
        #self._get_cars()


    def get_location(self, vin):
        """ get refreshed location information.

        """
        location_response = self.session.get(ME_LOCATION_URL % vin,
                                             verify=LOGIN_VERIFY_SSL_CERT)
        return json.loads(location_response.content.decode('utf8'))['data']


    def _get_cars(self):
        cur_time = time.time()
        with self.__lock:
            if cur_time - self.last_update_time > self.update_interval:
                response = self.session.get(ME_STATUS_URL,
                                            verify=LOGIN_VERIFY_SSL_CERT)

                #if response.headers["Content-Type"] == CONTENT_TYPE_JSON:
                cars = json.loads(
                    response.content.decode('utf8'))['vehicles']
                
                for c in cars:
                    car = Car()
                    car.finorvin = c.get("vin")
                    car.licenseplate = c.get("licenceplate")

                    response = self.session.get(CAR_DETAIL_URL % car.finorvin,
                                                verify=LOGIN_VERIFY_SSL_CERT)
                    detail = json.loads(response.content.decode('utf8')).get("data")
                    
                    if DEBUG_MODE:
                        file = open("%s_converant.json" % car.finorvin, "w")
                        file.write(response.text)
                        file.close()

                    car.salesdesignation = detail.get("salesDesignation")
                    self.cars.append(car)

                self.last_update_time = time.time()


    def _get_session_cookies(self, username, password):
        # Start session and get login form.
        session = self.session
        loginpage = session.get(LOGIN_STEP1_URL, verify=LOGIN_VERIFY_SSL_CERT)

        # Get the hidden elements and put them in our form.
        login_html = lxml.html.fromstring(loginpage.text)
        hidden_elements = login_html.xpath('//form//input')
        form = {x.attrib['name']: x.attrib['value'] for x in hidden_elements}

        # "Fill out" the form.
        form['username'] = username
        form['password'] = password
        form['remember-me'] = 1

        # login and check the values.
        url = "{0}{1}".format(SERVER_LOGIN, LOGIN_STEP2_URL)
        loginpage2 = session.post(url, data=form, verify=LOGIN_VERIFY_SSL_CERT)

        # step 3
        login2_html = lxml.html.fromstring(loginpage2.text)
        hidden_elements = login2_html.xpath('//form//input')
        form = {x.attrib['name']: x.attrib['value'] for x in hidden_elements}

        if DEBUG_MODE:
            file = open("LoginStep2.txt", "w")
            file.write(loginpage2.text)
            file.close()

        loginpage3 = session.post(LOGIN_STEP3_URL, data=form, verify=LOGIN_VERIFY_SSL_CERT)
        
        if DEBUG_MODE:
            file = open("LoginStep3.txt", "w")
            file.write(loginpage3.text)
            file.close()

        self.is_valid_session = True
        return session.cookies
