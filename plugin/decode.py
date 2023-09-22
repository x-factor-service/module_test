

def decodeJson(json) :
    # Input
    if json['INPUT']['API']['USE'] :
        InApiInfo = {'url' : json['INPUT']['API']['TANIUM']['URL'],
        'authUrl' : json['INPUT']['API']['TANIUM']['PATH']['AUTH'],
        'questionUrl' : json['INPUT']['API']['TANIUM']['PATH']['SAVEQUSTION'],
        'username' : json['INPUT']['API']['TANIUM']['USERNAME'],
        'password' : json['INPUT']['API']['TANIUM']['PASSWORD'],
        'sensorIdList' : list(json['INPUT']['API']['TANIUM']['SensorID'].keys()),
        'sensorIdValue' : list(json['INPUT']['API']['TANIUM']['SensorID'].values())
        }
    else :
        InApiInfo = None
    if json['INPUT']['DB']['USE'] :
        InDbInfo = {'host' : json['INPUT']['DB']['PS']["HOST"],
        'port' : json['INPUT']['DB']['PS']["PORT"],
        'dbname' : json['INPUT']['DB']['PS']["NAME"],
        'user' : json['INPUT']['DB']['PS']["USER"],
        'pwd' : json['INPUT']['DB']['PS']["PWD"]}
    else :
        InDbInfo = None
    #Output
    if json['OUTPUT']['DB']['USE'] :
        OutDbInfo = {'host' : json['OUTPUT']['DB']['INFO']["HOST"],
        'port' : json['OUTPUT']['DB']['INFO']["PORT"],
        'dbname' : json['OUTPUT']['DB']['INFO']["NAME"],
        'user' : json['OUTPUT']['DB']['INFO']["USER"],
        'pwd' : json['OUTPUT']['DB']['INFO']["PWD"]}
    else :
        OutDbInfo = None

    return {"INAPI" : InApiInfo, "INDB" : InDbInfo, "OUTDB" : OutDbInfo}