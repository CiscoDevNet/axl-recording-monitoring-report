import os
import datetime
import re

import untangle
import requests
from dotenv import load_dotenv

load_dotenv()

checkMark = '\u2713'

excludeList = [
    'Universal Device Template', # N/A
    'Cisco TelePresence', # Not a real/configurable device?
    'Cisco 7910', # Deprecated as of 11.5(1)
    # 3rd party
    'Nokia S60', 
    'IPTrade Profile EK',
    'IPTrade TAD',
    'Mindshare MAXplus'
]

sql = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://www.cisco.com/AXL/API/1.0">
            <soapenv:Header/>
            <soapenv:Body>
                <ns:getCCMVersion>
                    <processNodeName></processNodeName>
                </ns:getCCMVersion>
            </soapenv:Body>
            </soapenv:Envelope>'''

resp = requests.post(
    f'https://{ os.getenv( "CUCM_ADDRESS" ) }:8443/axl/',
    auth = ( os.getenv( 'AXL_USER' ), os.getenv( 'AXL_PASSWORD' ) ),
    headers = { 'Content-Type': 'text/xml' },
    data = sql,
    verify = False )

xml = untangle.parse( resp.text )

cucmVersion = xml.soapenv_Envelope.soapenv_Body.ns_getCCMVersionResponse.return_.componentVersion.version.cdata
axlVersion = re.search( r'^([0-9]+\.[0-9]+)', cucmVersion ).group() 

sql = f'''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://www.cisco.com/AXL/API/{ axlVersion }">
            <soapenv:Header/>
            <soapenv:Body>
                <ns:executeSQLQuery sequence="1">
                    <sql>select typemodel.name, productsupportsfeature.tksupportsfeature, tkdeviceprotocol 
                            from productsupportsfeature, typemodel
                            where productsupportsfeature.tkmodel=typemodel.enum and 
                            productsupportsfeature.tksupportsfeature in (24,25,32)</sql>
                </ns:executeSQLQuery>
            </soapenv:Body>
            </soapenv:Envelope>'''

resp = requests.post(
    f'https://{ os.getenv( "CUCM_ADDRESS" ) }:8443/axl/',
    auth = ( os.getenv( 'AXL_USER' ), os.getenv( 'AXL_PASSWORD' ) ),
    headers = { 'Content-Type': 'text/xml', 'SOAPAction': f'"CUCM:DB ver={ axlVersion } executeSQLQuery"' },
    data = sql,
    verify = False )

xml = untangle.parse( resp.text )

featureList = xml.soapenv_Envelope.soapenv_Body.ns_executeSQLQueryResponse.return_.row

supportedList = {}

for device in featureList:

    if device.name.cdata in excludeList: continue
    
    if device.tksupportsfeature.cdata in ( '24', '25', '32' ): # Monitor, Record, Built In Bridge

        deviceName = device.name.cdata

        if not deviceName in supportedList:

            supportedList[ deviceName ] = { 'Record': False, 'Monitor': False, 'Built In Bridge': False }

        match device.tksupportsfeature.cdata:

            case '24':
                supportedList[ deviceName ].update( { 'Monitor': True } )
            case '25':
                supportedList[ deviceName ].update( { 'Record': True } )
            case '32':
                supportedList[ deviceName ].update( { 'Built In Bridge': True } )
                

supportedList = dict( sorted( supportedList.items() ) )

outFile = open( 'supported_list.md', 'w' )
outFile.write( '# Unified CM Silent Monitoring/Recording Supported Device Matrix\n' )
outFile.write( f'Last update: { datetime.date.today() } / CUCM version { axlVersion }\n' )
outFile.write( 'Device | Monitoring | Gateway Recording | Phone (BiB) Recording\n' )
outFile.write( ':----- | :--------- | :---------------- | :--------------------\n' )

for deviceName, features in supportedList.items():

    if not ( features["Monitor"] or features["Record"] ): continue

    outFile.write( f'{ deviceName } | ' )
    outFile.write( f'{checkMark if features["Monitor"] else "X"} | ' )
    outFile.write( f'{checkMark if features["Record"] else "X"} | ' )
    outFile.write( f'{checkMark if features["Built In Bridge"] else "X"}\n' )
    
outFile.close()