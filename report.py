import untangle

check = '\u2713'

excludeList = [
    'Universal Device Template',
    'IPTrade Profile EK',
    'IPTrade TAD',
    'Nokia S60'
]
report = untangle.parse( 'UnifiedCMPhoneFeatureList.xml' )

featureList = report.GRTReport.GRTSource[ 2 ].table.row

del featureList[ 0 ]

supportedList = {}

for device in featureList:

    if device.cell[ 0 ] in excludeList: continue
    
    if device.cell[2] in ('Record','Monitor','Built In Bridge'):

        deviceName = device.cell[0].cdata + ' (' + device.cell[ 1 ].cdata + ')'

        if not deviceName in supportedList:

            supportedList[ deviceName ] = { 'Record': False, 'Monitor': False, 'Built In Bridge': False }

        supportedList[ deviceName ].update( { device.cell[2].cdata: True } )

outFile = open( 'supported_list.md', 'w' )

outFile.write( 'Device/Phone (Protocol) | Monitoring | Gateway Recording | Phone/BiB Recording\n' )
outFile.write( '----------------------- | ---------- | ----------------- | -------------------\n' )

for deviceName, features in supportedList.items():

    if not ( features["Monitor"] or features["Record"] ): continue

    outFile.write( f'{ deviceName } | ' )
    outFile.write( f'{check if features["Monitor"] else "X"} | ' )
    outFile.write( f'{check if features["Record"] else "X"} | ' )
    outFile.write( f'{check if features["Built In Bridge"] else "X"}\n' )
    
outFile.close()