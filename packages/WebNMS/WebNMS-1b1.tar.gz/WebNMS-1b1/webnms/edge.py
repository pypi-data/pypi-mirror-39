# coding: utf-8
"""WebNMS Edge SDK Base

This package helps you to start your IoT journey with WebNMSIoT platform,
by enabling any Gateway that supports python to be integrated with the
WebNMSIoT Platform seamlessly.

Notes
-----

To know more details about the SDK, refer to the user guide :
        https://www.webnms.com/iot/help/Python_sdk_user_guide.pdf
To download WebNMSIoT Platform trial version, visit :
        https://www.webnms.com/iot/download.html
To know more about us, visit:
        https://www.webnms.com/
        
SOFTWARE LICENSE AGREEMENT

This Software License Agreement (“Agreement”) details the policy for
license of WebNMS Edge SDK (“Licensed Software”) and constitutes a 
binding agreement between you or the entity that you represent (“You”)
and Zoho Corporation (“Zoho”).Please read the following terms 
carefully, before either 
  (i) downloading the Licensed Software froman authorized website, or
  (ii) installing the Licensed Software. 
You acknowledge that you have read this Agreement, have understood it,
and agree to be bound by its terms.If you do not agree to the 
terms and conditions of this Agreement, do not download or install 
the Licensed Software.

1. LICENSE GRANT:

The Licensed Software is intended to be used in conjunction with 
WebNMS IoT Platform (“Base Product”). Zoho hereby grants you 
a non-exclusive, non-transferable, world-wide license to 
use the Licensed Software, including user documentation and updates
to which you are entitled, in conjunction with the Base Product.
You understand that you require a valid license for the Base Product
in order to use the Licensed Software and that you will not be able 
to use the Licensed Software if the license for the Base Product 
expires or is otherwise terminated. 

2. THIRD PARTY PRODUCTS:

The Licensed Software may contain software which originated with 
third party vendors and without limiting the general applicability
of the other provisions of this Agreement, you agree that 
  (a) the title to any third party software incorporated in 
  the Licensed Software shall remain with the third party which 
  supplied the same; and 
  (b) you will not distribute any such third party software available
   with the Licensed Software, unless the license terms of such third 
   party software provide otherwise.
   
3. RESTRICTIONS ON USE:

In addition to all other terms and conditions of this Agreement,
you shall not:
 i.  remove any copyright, trademark or other proprietary notices from
     the Licensed Software or its copies;
 ii. rent, lease, license, sublicense or distribute the Licensed 
  Software or any portions of it on a standalone basis or as part of 
  your application; 
 iii.reverse engineer, decompile or disassemble the Licensed Software;
 
4. TECHNICAL SUPPORT:

Technical support for the Licensed Software is provided as part of your 
license to the Base product. Technical support for the Licensed Software
 is co-terminus with your license to the Base Product.
 
5. OWNERSHIP AND INTELLECTUAL PROPERTY:

Zoho owns all right, title and interest in and to the Licensed Software.
Zoho expressly reserves all rights not granted to you herein,
notwithstanding the right to discontinue or not to release any 
Licensed Software and to alter features, specifications, capabilities,
functions or characteristics of the Licensed Software.
The Licensed Software is only licensed and not sold to you by Zoho. 

6. AUDIT:

Zoho has the right to audit your Use of the Licensed Software by 
providing at least seven (7) days prior written notice of its 
intention to conduct such an audit at your facilities during 
normal business hours.

7. CONFIDENTIALITY:

The Licensed Software contains proprietary information of Zoho and you
hereby agree to take all reasonable efforts to maintain 
the confidentiality of the Licensed Software. You agree to reasonably
communicate the terms and conditions of this Agreement to those persons
employed by you who come into contact with or access the Licensed 
Software, and to use reasonable efforts to ensure their compliance with
such terms and conditions, including but not limited to, not knowingly
permitting such persons to use any portion of the Licensed Software for
a purpose that is not allowed under this Agreement.

8. WARRANTY DISCLAIMER:

ZOHO DOES NOT WARRANT THAT THE LICENSED SOFTWARE WILL BE ERROR-FREE.
EXCEPT AS PROVIDED HEREIN, THE LICENSED SOFTWARE IS FURNISHED "AS IS" 
WITHOUT WARRANTY OF ANY KIND, INCLUDING THE WARRANTIES OF MERCHANTABILITY
AND FITNESS FOR A PARTICULAR PURPOSE AND WITHOUT WARRANTY AS TO 
THE PERFORMANCE OR RESULTS YOU MAY OBTAIN BY USING THE LICENSED SOFTWARE.
YOU ARE SOLELY RESPONSIBLE FOR DETERMINING THE APPROPRIATENESS OF USING 
THE LICENSED SOFTWARE AND ASSUME ALL RISKS ASSOCIATED WITH THE USE OF IT,
INCLUDING BUT NOT LIMITED TO THE RISKS OF PROGRAM ERRORS, DAMAGE TO OR 
LOSS OF DATA, PROGRAMS OR EQUIPMENT, AND UNAVAILABILITY OR 
INTERRUPTION OF OPERATIONS.

BECAUSE SOME JURISDICTIONS DO NOT ALLOW FOR THE EXCLUSION OR LIMITATION
OF IMPLIED WARRANTIES, THE ABOVE EXCLUSIONS OR LIMITATIONS MAY NOT APPLY TO YOU.

9. LIMITATION OF LIABILITY:

In no event will Zoho be liable to you or any third party for any 
special, incidental, indirect, punitive or exemplary or consequential
damages, or damages for loss of business, loss of profits, business 
interruption, or loss of business information arising out of the use
or inability to use the Licensed Software or for any claim by any other
party even if Zoho has been advised of the possibility of such damages.
Zoho's entire liability with respect to its obligations under this 
Agreement or otherwise with respect to the Licensed Software shall
not exceed the fee paid by you for the Base Product.

10. INDEMNIFICATION:

Zoho agrees to indemnify and defend you from and against any and all 
claims, actions or proceedings, arising out of any claim that 
the Licensed Software infringes or violates any valid U.S. patent,
copyright or trade secret right of any third party; so long as you provide;
 (i) prompt written notice to Zoho of such claim;
 (ii) cooperate with Zoho in the defense and/or settlement thereof,
      at Zoho's expense; and, 
 (iii) allow Zoho to control the defense and all related settlement
      negotiations. 
The above is Zoho's sole obligation to you and shall be your sole and 
exclusive remedy pursuant to this Agreement for intellectual property
infringement. 
Zoho shall have no indemnity obligation for claims of infringement to
the extent resulting or alleged to result from 
  (i) any combination, operation, or use of the Licensed Software with
     any programs or equipment not supplied by Zoho;
  (ii) any modification of the Licensed Software by a party other 
     than Zoho; and 
  (iii) your failure, within a reasonable time frame, to implement any
     replacement or modification of Licensed Software provided by Zoho
     
11. TERMINATION:

This Agreement is co-terminus with your license to the Base Product.
You may terminate this Agreement at any time by destroying or 
returning to Zoho all copies of the Licensed Software in your possession.
Zoho may terminate this Agreement for any reason, including but 
not limited to your breach of any of the terms of this Agreement. 
Upon termination, you shall destroy or return to Zoho all copies of 
the Licensed Software and certify in writing that all known copies 
have been destroyed. All provisions relating to confidentiality, 
proprietary rights, non-disclosure, and limitation of liability shall 
survive the termination of this Agreement.

12. GENERAL:

This Agreement shall be construed, interpreted and governed by 
the laws of the State of California exclusive of its conflicts of 
law provisions. This Agreement constitutes the entire agreement between
the parties, and supersedes all prior communications, understandings 
or agreements between the parties. Any waiver or modification of this 
Agreement shall only be effective if it is in writing and signed by both
parties hereto. If any part of this Agreement is found to be invalid or 
unenforceable, the remainder shall be interpreted so as to reasonably 
effect the intention of the parties.         
        
        
"""

import json
import requests


class WebnmsGateway:
    """A class to define the Gateway.

    Parameters
    ----------
    address    : 'string'
        The domain name or the ip address of the WebNMS instance.
    port       : 'int'
        The Port No of the WebNMS instance.
    protocol   : 'string'
        The protocol used for communication. Currently Only HTTP is supported.
        The possible entry as of now is i. http
    deviceName : 'string'
        The Gateway name as configured in the WebNMS.
    serialNo   : 'string'
        The serial no. of the gateway device.
    """

    instance = None
    address = None
    port = None
    protocol = None
    deviceName = None
    serialNo = None

    def __init__(self, address, port, protocol, deviceName, serialNo):
        if WebnmsGateway.instance is not None:
            raise Exception("A Gateway is already initialized")
        else:
            self.address = address
            self.port = port
            self.deviceName = deviceName
            self.serialNo = serialNo

            if protocol == 'http':
                self.protocol = protocol
            else:
                raise Exception("Unsupported protocol")
                exit(-1)
            WebnmsGateway.instance = self

    @staticmethod
    def getInstance():
        if WebnmsGateway.instance is None:
            raise Exception("The gateway parameters are not initialised")
        else:
            return WebnmsGateway.instance


class DataWrapper:
    """A Wrapper class which is used to collect all the data associated
        with the gateway and push it to WebNMS IoT server

    """
    def __init__(self,):
        self.time = None
        self.sensorList = []

    class Sensor:
        def __init__(self, sensorName):
            self.name = sensorName
            self.data = dict()
            self.data['name'] = sensorName

    def setTimestamp(self, timestamp):
        """Function to set timestamp to the data wrapper

        timestamp: 'integer'
            The Unix timestamp in milliseconds
        """
        self.time = timestamp

    def addData(self, sensorName, parameterName, paramerterValue):
        """Function to add a parameter and its value along with
           its parent sensor

        sensorName: 'string'
            Name of the parent sensor
        parameterName: 'string'
            Name of the parameter
        paramerterValue:
            Value of the parameter
        """
        if not self.sensorList:
            sensor = self.Sensor(sensorName)
            sensor.data[parameterName] = paramerterValue
            self.sensorList.append(sensor)
        else:
            for sensorObj in self.sensorList:
                if sensorName in sensorObj.name:
                    sensorObj.data[parameterName] = paramerterValue
                    return
            sensor = self.Sensor(sensorName)
            sensor.data[parameterName] = paramerterValue
            self.sensorList.append(sensor)


def init(address, port, protocol, deviceName, serialNo):
    """The Function to initialize the SDK with respect to the server and the gateway

    address: 'string'
        The domain name or the ip address of the WebNMS instance.
    port: 'int'
        The Port No of the WebNMS instance.
    protocol: 'string'
        The protocol used for communication. Currently Only HTTP is supported.
        The possible entry as of now is i. http
    deviceName: 'string'
        The Gateway name as configured in the WebNMS.
    serialNo: 'string'
        The serial no. of the gateway device.
    """
    WebnmsGateway(address, port, protocol, deviceName, serialNo)


def getInstance():
    return WebnmsGateway.getInstance()


def getNewDataWrapper():
    """Function to get the Data Wrapper for gathering data and push
        it to WebNMS IoT Server.

    return: 'An Instance of the DataWrapper class'
    """
    return DataWrapper()


def constructWebnsmPacket(dataWrapper):
    gatewayObject = getInstance()
    tempdata = dict()
    tempdata['name'] = gatewayObject.deviceName
    tempdata['serial_no'] = gatewayObject.serialNo
    tempdata['time'] = dataWrapper.time
    tempdata['json_version'] = 1
    jsonList = []
    for sensor in dataWrapper.sensorList:
        jsonList.append(sensor.data)
    tempdata['sensors'] = jsonList
    return json.dumps(tempdata)


def sendData(dataWrapper):
    """Function to push the data collected via the data Wrapper

    dataWrapper: 'A data Wrapper instance with the collected data'
    return: 'int'
        1 on success and -1 on failure
    """
    dataUpdateURL = "/Gateway/data/Update"
    data = constructWebnsmPacket(dataWrapper)
    gatewayObject = getInstance()
    URL = "http://" + str(gatewayObject.address) + ":"+str(gatewayObject.port) + dataUpdateURL
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    try:
        request = requests.post(URL, data, headers=headers, timeout=5)
        if request.status_code == 200:
            statusCode = 1
        else :
            statusCode = -1
    except requests.exceptions.RequestException as e:
            print("Data send failure: " + str(e))
            statusCode = -1
    return statusCode

