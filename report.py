import untangle

check = '\u2713'

excludeList = [
    'Universal Device Template', # N/A
    'Cisco TelePresence', # Not a real/configurable device?
    'Nokia S60', # 3rd party
    'Cisco 7910' # Deprecated as of 11.5(1)
]
report = untangle.parse( 'UnifiedCMPhoneFeatureList.xml' )

featureList = report.GRTReport.GRTSource[ 2 ].table.row

del featureList[ 0 ]

supportedList = {}

for device in featureList:

    if device.cell[ 0 ] in excludeList: continue
    if device.cell[ 1 ] == 'SCCP': continue
    
    if device.cell[ 2 ] in ( 'Record', 'Monitor', 'Built In Bridge' ):

        deviceName = device.cell[0].cdata

        if not deviceName in supportedList:

            supportedList[ deviceName ] = { 'Record': False, 'Monitor': False, 'Built In Bridge': False }

        supportedList[ deviceName ].update( { device.cell[ 2 ].cdata: True } )

supportedList = dict( sorted( supportedList.items() ) )

outFile = open( 'supported_list.md', 'w' )

outFile.write( 'Device/Phone (Protocol) | Monitoring | Gateway Recording | Phone (BiB) Recording\n' )
outFile.write( '----------------------- | ---------- | ----------------- | -------------------\n' )

for deviceName, features in supportedList.items():

    if not ( features["Monitor"] or features["Record"] ): continue

    outFile.write( f'{ deviceName } | ' )
    outFile.write( f'{check if features["Monitor"] else "X"} | ' )
    outFile.write( f'{check if features["Record"] else "X"} | ' )
    outFile.write( f'{check if features["Built In Bridge"] else "X"}\n' )
    
outFile.close()