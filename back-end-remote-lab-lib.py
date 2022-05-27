
from flask import Flask, jsonify, request
from serial_device import SerialDevice
#from serial_device_th import SerialDevice
from flask_cors import CORS
import sys
import json  
import time

#Version 2.0.02
#Se agrego soporte para recepcion por tread

#Version 2.0.01
#Se corrigio recepcion de ejecucion del experimento.
#Version 2.0.00 
#     Se agrego soporte runExample3 y 4
#     Los pedidos de ejecucion pasaron a ser GET ya que no trasportan data!!!


ser = SerialDevice()
json_fields = {} 

# Si se usa la recepcion por thead el time out =1 ya que quee  no pierde ninguna recepcion 
# Si se usa la recepcion por polling el time_out=60 ya que este lo usa para esperar la ejecucion del experimento

time_out = 60


print("Back-end RemoteLab-lib ")
print("Version 2.0.02 ")
#if ser.open('/dev/ttyUSB0'): #Si no encuentra el COM LO BUSCA    
if ser.open(port='COM11', timeout=time_out):
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
    json_fields = ser.read_cmd(time_out)       
   # return (json_fields)
    return jsonify(json_fields)

@app.route('/read/all-cfg')
def getAllConfig():
    ser.send_cmd("{read:'all-cfg'}") 
    json_fields = ser.read_cmd(time_out)   
   # return (json_fields)
    return jsonify(json_fields)

@app.route('/read/all-input')
def getAllInputs():
    ser.send_cmd("{read:'all-input'}") 
    json_fields = ser.read_cmd(time_out)   
   # return (json_fields)
    return jsonify(json_fields)

@app.route('/read/all-output')
def getAllOutputs():
    ser.send_cmd("{read:'all-output'}") 
    json_fields = ser.read_cmd(time_out)   
   # return (json_fields)
    return jsonify(json_fields)

@app.route('/read/all-result')
def getAllResult():
    ser.send_cmd("{read:'all-result'}") 
    json_fields = ser.read_cmd(time_out)   
   # return (json_fields)
    return jsonify(json_fields)

@app.route('/read/all-lib')
def getAllLib():
    ser.send_cmd("{read:'all-lib'}") 
    json_fields = ser.read_cmd(time_out)   
   # return (json_fields)
    return jsonify(json_fields)

@app.route('/read/version')
def getVersion():
    ser.send_cmd("{read:'version'}") 
    json_fields = ser.read_cmd(time_out)   
   # return (json_fields)
    return jsonify(json_fields)

@app.route('/read/status')
def getStatus():
    ser.send_cmd("{read:'status'}") 
    json_fields = ser.read_cmd(time_out)
   # return (json_fields)
    return jsonify(json_fields)

@app.route('/read/serial_level')
def getSerialLevel():
    ser.send_cmd("{read:'serial_level'}") 
    json_fields = ser.read_cmd(time_out)   
   # return (json_fields)
    return jsonify(json_fields)

@app.route('/save/disable_serial')                                                                                              
def putSaveSerial():                                                                                                                              
    ser.send_cmd("{serial_level:'0'}") 
    json_fields = ser.read_cmd(time_out) 
    return jsonify(json_fields)


@app.route('/save/run1')                                                                                              
def putRunExample1():                                                                                                                              
    ser.send_cmd("{st_mode:'100'}") 
    json_fields = ser.read_cmd(time_out) 
    return jsonify(json_fields)

@app.route('/save/run2')                                                                                              
def putRunExample2():                                                                                                                              
    ser.send_cmd("{st_mode:'101'}") 
    json_fields = ser.read_cmd(time_out) 
    return jsonify(json_fields)


@app.route('/save/run3')                                                                                              
def putRunExample3():                                                                                                                              
    ser.send_cmd("{st_mode:'102'}") 
    json_fields = ser.read_cmd(time_out) 
    return jsonify(json_fields)


@app.route('/save/run4')                                                                                              
def putRunExample4():                                                                                                                              
    ser.send_cmd("{st_mode:'103'}") 
    json_fields = ser.read_cmd(time_out) 
    return jsonify(json_fields)



@app.route('/save/all-input', methods=['PUT'])                                                                                              
def putSaveAllInput():                                                                                                                              
    data = request.get_json()    
    ser.send_cmd("{input0:'" +str(data.get('input0'))+"',input1:'" +str(data.get('input1'))+"',input2:'" +str(data.get('input2'))+"',input3:'" +str(data.get('input3'))+"',input4:'" +str(data.get('input4'))+"'}") 
    json_fields = ser.read_cmd(time_out)
    return jsonify(json_fields)

@app.route('/save/all-cfg', methods=['PUT'])                                                                                              
def putSaveAllCfg():                                                                                                                              
    data = request.get_json()   
    ser.send_cmd("{cfg0:'" +str(data.get('cfg0'))+"',cfg1:'" +str(data.get('cfg1'))+"',cfg2:'" +str(data.get('cfg2'))+"',cfg3:'" +str(data.get('cfg3'))+"',cfg4:'" +str(data.get('cfg4'))+"',cfg5:'" +str(data.get('cfg5'))+"',cfg6:'" +str(data.get('cfg6'))+"',cfg7:'" +str(data.get('cfg7'))+"',cfg8:'" +str(data.get('cfg8'))+"',cfg9:'" +str(data.get('cfg9'))+"'}") 
    json_fields = ser.read_cmd(time_out) 
    return jsonify(json_fields)




@app.route('/cmd/start')
def putCmdStart():  #por razones de compatibilidad esta peticion es bloqueante.   
    ser.send_cmd("{cmd:'start'}")
    json_fields = ser.read_cmd(time_out)
    print (json_fields)
    while (True):
        json_fields = ser.read_cmd(time_out)
        print (json_fields)       
        if (("st_test" in json_fields) == True ) :#chequea el valor = 0
            if (json_fields.get('st_test') == 0):
                return jsonify(json_fields)
        
    
    
    


#testgit
if __name__ == '__main__':
    app.run( host='0.0.0.0', port=4000)
    
     