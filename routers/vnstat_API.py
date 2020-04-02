#!flask/bin/pythoni
from flask import Flask
import os
from flask import request

vnstat = Flask(__name__)

@vnstat.route('/network/statistics')
def get_network_statiscits():
    args = request.args
    #print (args['interface'])
    if str(args['interface']) == 'all':
        stream = os.popen('vnstat -h --json')
        output = stream.read()
        output
        #print("All statisics of all interfaces -- Out put: "+str(output))
        return output
    if (str(args['interface'] != 'all')) and  (str(args['stamp']) != 'history'):
        #vnstat -l -i enp2s0 -h --json
        #vnstat -i enp2s0 -tr 2 -h --json
        stream = os.popen('vnstat -i '+str(args['interface'])+' -tr '+str(args['stamp']) + ' -h --json')
        output = stream.read()
        output
        #print("Snap shot of a time - Out put: "+str(output))
        return output

    if (str(args['interface']) != 'all') and (str(args['stamp']) == 'history'):
        stream = os.popen('vnstat -i '+str(args['interface'])+' -h --json')
        output = stream.read()
        output
        #print("History of a specif interface Out put: "+str(output))
        return output

if __name__ == '__main__':
    vnstat.run(debug=True, host='0.0.0.0', port=1414)
