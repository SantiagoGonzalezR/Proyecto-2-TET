import dotenv from 'dotenv';
import grpc from '@grpc/grpc-js';
import protoLoader from '@grpc/proto-loader';

dotenv.config()
//Entender el contenido del archivo .env
const PROTO_PATH = process.env.PROTO_PATH;
const HOSTS = process.env.HOSTS.split(',');
const maxHosts = HOSTS.length;
const CurrentHosts = new Array(maxHosts);

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
  var available = 0;
  for (let i = 0; i < HOSTS.length; i++) {//Mira cuantas estan funcionando
    CurrentHosts[i].CheckOnline({}, (err, data) => {
      if (err) {
        //Que hacer si no se puede conectar con uno especifico
      } else {
        available += 1;
      }
    });
  }
  await wait(1000);//Espera que todas puedan responder
  console.log('Available: ', available);
  if (available == 0) {//Si no hay ninguno
    console.log("No available!!!");
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