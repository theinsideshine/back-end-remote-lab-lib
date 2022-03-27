
from flask import Flask, jsonify, request
from serial_device import SerialDevice
from flask_cors import CORS
import sys
import json  
import time



#Version 1.0.03 
#      ADD print version     get/step_cal   get/put step_k

ser = SerialDevice()
json_fields = {} 
print("Back-end RemoteLab-lib ")
print("Version 1.0.00. ")
#if ser.open('/dev/ttyUSB0'): #Si no encuentra el COM LO BUSCA    
if ser.open('COM11'):
    print("Conectado en windows")
else:
   print("Error al abrir puerto.")
   sys.exit("Programa abortado.")
time.sleep(3)# arduino al iniciliarse el puerto serie ser resetea, este delay es para esperar que pase el reset 

app =  Flask(__name__)

#resuelve la seguridad del navegador de bloquear las peticiones locales 
CORS(app)

#cors = CORS(app, resources={
#    r"/*": {
#        "origins":"*"
#        }
#    })


from config import products

@app.route('/ping')
def ping():
    return jsonify({"message":"pong!"})

@app.route('/info/parameters')
def getParameters():
    ser.send_cmd("{info:'all-params'}") 
    json_fields = ser.read_answer()   
   # return (json_fields)
    return jsonify(json_fields)

@app.route('/info/calibration')
def getCalibration():
    ser.send_cmd("{info:'all-calibration'}") 
    json_fields = ser.read_answer()   
   # return (json_fields)
    return jsonify(json_fields)

@app.route('/info/version')
def getVersion():
    ser.send_cmd("{info:'version'}") 
    json_fields = ser.read_answer()   
   # return (json_fields)
    return jsonify(json_fields)

@app.route('/info/status')
def getStatus():
    ser.send_cmd("{info:'status'}") 
    json_fields = ser.read_answer()   
   # return (json_fields)
    return jsonify(json_fields)

@app.route('/info/reaction_one')
def getReaction_one():
    ser.send_cmd("{info:'reaction_one'}") 
    json_fields = ser.read_answer()   
   # return (json_fields)
    return jsonify(json_fields)

@app.route('/info/reaction_two')
def getReaction_two():
    ser.send_cmd("{info:'reaction_two'}") 
    json_fields = ser.read_answer()   
   # return (json_fields)
    return jsonify(json_fields)

@app.route('/info/flexion')
def getFlexion():
    ser.send_cmd("{info:'flexion'}") 
    json_fields = ser.read_answer()   
   # return (json_fields)
    return jsonify(json_fields)






@app.route('/parameters/distance/<string:distance>', methods=['PUT'])
def putParmDistance(distance):    
    ser.send_cmd("{distance:'"+distance+"'}")    
    json_fields = ser.read_answer()   
    return jsonify(json_fields)


@app.route('/parameters/force/<string:force>', methods=['PUT'])
def putParmForce(force):
    ser.send_cmd("{force:'"+force+"'}")    
    json_fields = ser.read_answer()   
    return jsonify(json_fields)

@app.route('/parameters/step_k/<string:step_k>', methods=['PUT'])
def putParmStepK(step_k):
    ser.send_cmd("{step_k:'"+step_k+"'}")    
    json_fields = ser.read_answer()   
    return jsonify(json_fields)

@app.route('/comands/start', methods=['PUT'])
def putCmdStart():  #por razones de compatibilidad esta peticion es bloqueante.
    ser.send_cmd("{cmd:'start'}")
    while (True):
        json_fields = ser.read_answer() #viene convertido en dict usa ' '
        print (json_fields)
        print (json_fields.get('st_test'))        #chequea key = 'st_test'
        if (("st_test" in json_fields) == True ) :#chequea el valor = 0
            if (json_fields.get('st_test') == 0):
                print(1)
                return jsonify(json_fields)
        
    
    
    


#testgit
if __name__ == '__main__':
    app.run( host='0.0.0.0', port=4000)
    
     