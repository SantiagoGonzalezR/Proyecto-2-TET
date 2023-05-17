require('dotenv').config();
const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');

//Entender el contenido del archivo .env
const PROTO_PATH = process.env.PROTO_PATH;
const maxHosts = 5;
const CurrentHosts = new Array(maxHosts);
const fs = require('fs');

const packageDefinition = protoLoader.loadSync(
  PROTO_PATH,
  {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true
  });

const proto = grpc.loadPackageDefinition(packageDefinition);

function checkHosts() {
  const jsonData = fs.readFileSync('maquinas.json', 'utf8');

  // Convertir el json en un objeto
  const jsonObject = JSON.parse(jsonData);

  // Crear una lista con las IPs para la conexion por gRPC
  const HOSTS = Object.keys(jsonObject);
  // Agregar el puerto para la conexion y crear dicha conexion
  const port = ':8080';
  for (let i = 0; i < HOSTS.length; i++) {
    HOSTS[i] += port;
    CurrentHosts[i] = new microService(HOSTS[i], grpc.credentials.createInsecure())
  }

  const newJsonData = {};

  // Agregar los valores al diccionario
  for (const key in jsonObject) {
    newJsonData[key] = jsonObject[key];
  }
  var available = 0;
  for (let i = 0; i < HOSTS.length; i++) {//Mira cuantas estan funcionando
    CurrentHosts[i].CheckOnline({}, (err, data) => {
      const char = ':';
      const portless = HOSTS[i].substring(0, HOSTS[i].indexOf(char));
      if (err) {
        if (portless in newJsonData) { }
        else {
          delete HOSTS[i];
          delete CurrentHosts[i];
        }
      } else {
        newJsonData[portless] = parseFloat(data.time);
        const modifiedJsonData = JSON.stringify(newJsonData, null, 2);
        fs.writeFileSync('maquinas.json', modifiedJsonData, 'utf8');
        available += 1;
      }
    });
  }
  setTimeout(function () { availablef(available); }, 1000);
}

function availablef(available){
  console.log('Available: ', available);
  if (available == 0) {//Si no hay ninguno
    console.log("No machine available!!!");
  }
  setTimeout(function () { checkHosts(); }, 2000);
}

const microService = grpc.loadPackageDefinition(packageDefinition).MicroService;

function main() {
  checkHosts();
};

main();