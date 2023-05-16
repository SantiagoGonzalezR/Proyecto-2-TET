import dotenv from 'dotenv';
import grpc from '@grpc/grpc-js';
import protoLoader from '@grpc/proto-loader';

dotenv.config()
//Entender el contenido del archivo .env
const PROTO_PATH = process.env.PROTO_PATH;
const fs = require('fs');
const Connections = 'maquinas.json';

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

async function checkHosts() {
  var HOSTS = process.env.HOSTS.split(',');
  var CurrentHosts = new Array(5);
  var available = 0;
  for (let i = 0; i < HOSTS.length; i++) {//Mira cuantas estan funcionando
    CurrentHosts[i].CheckOnline({}, (err, data) => {
      if (err) {
        delete Connections[i];
        delete HOSTS[i];
      } else {
        try {
          var ip = data.request.ip;
          const json = JSON.parse(fs.readFileSync(Connections, 'utf8'));
          json[ip] = data.request.process;
          fs.writeFileSync(Connections, JSON.stringify(json, null, 2), 'utf8');
        } catch (err) {
          console.error('Error:', err);
        }
        available += 1;
      }
    });
  }
  await wait(1000);//Espera que todas puedan responder
  console.log('Available: ', available);
  if (available == 0) {//Si no hay ninguno
    console.log("No machines available!!!");
  }
  setTimeout(function () { checkHosts(); }, 2000);
}

const microService = grpc.loadPackageDefinition(packageDefinition).MicroService;

function main() {
  for (let i = 0; i < maxHosts; i++) {//Se inicia la conexion con todos los micro servicios
    CurrentHosts[i] = new microService(HOSTS[i], grpc.credentials.createInsecure());
  }
  checkHosts();
};

main();