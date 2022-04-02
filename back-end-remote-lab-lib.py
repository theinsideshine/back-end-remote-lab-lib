
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




@app.route('/ping')
def ping():
    return jsonify({"message":"pong!"})

@app.route('/read/all-params')
def getParameters():
    ser.send_cmd("{read:'all-params'}") 
    json_fields = ser.read_answer()   
   # return (json_fields)
    return jsonify(json_fields)

@app.route('/read/all-cfg')
def getCalibration():
    ser.send_cmd("{read:'all-cfg'}") 
    json_fields = ser.read_answer()   
   # return (json_fields)
    return jsonify(json_fields)

@app.route('/read/all-input')
def getAllUint8():
    ser.send_cmd("{read:'all-input'}") 
    json_fields = ser.read_answer()   
   # return (json_fields)
    return jsonify(json_fields)

@app.route('/read/version')
def getVersion():
    ser.send_cmd("{read:'version'}") 
    json_fields = ser.read_answer()   
   # return (json_fields)
    return jsonify(json_fields)

@app.route('/read/status')
def getStatus():
    ser.send_cmd("{read:'status'}") 
    json_fields = ser.read_answer()   
   # return (json_fields)
    return jsonify(json_fields)

@app.route('/read/serial_level')
def getSerialLevel():
    ser.send_cmd("{read:'serial_level'}") 
    json_fields = ser.read_answer()   
   # return (json_fields)
    return jsonify(json_fields)

#{uint8_0:'1000' ,uint8_1:'2000',uint8_2:'3000' ,uint8_3:'4000',uint8_4:'5000'}

@app.route('/save/all-input', methods=['PUT'])                                                                                              
def putSaveAllUint8():                                                                                                                              
    data = request.get_json()
    uint8_0 = data.get('input0')
    uint8_1 = data.get('input1')
    uint8_2 = data.get('input2')
    uint8_3 = data.get('input3')
    uint8_4 = data.get('input4')    
    
    ser.send_cmd("{input0:'" +str(data.get('input0'))+"',input1:'" +str(data.get('input1'))+"',input2:'" +str(data.get('input2'))+"',input3:'" +str(data.get('input3'))+"',input4:'" +str(data.get('input4'))+"'}") 
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

@app.route('/cmd/start', methods=['PUT'])
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
    
     