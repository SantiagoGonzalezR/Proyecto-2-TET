import dotenv from 'dotenv';
import grpc from '@grpc/grpc-js';
import protoLoader from '@grpc/proto-loader';

dotenv.config()
//Entender el contenido del archivo .env
const PROTO_PATH = process.env.PROTO_PATH;
const HOSTS = process.env.HOSTS.split(',');
const maxHosts = HOSTS.length + 1;
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

async function checkHosts() {//Ciclo que sucede cuando la MOM no es la principal
  var available = 0;
  for (let i = 0; i < HOSTS.length; i++) {//Mira cuantas MOM estan funcionando
    CurrentHosts[i].CheckOnline({}, (err, data) => {
      if (!err)
        available += 1;
    });
  }
  await wait(1000);//Espera que todas puedan responder
  console.log('Available: ', available);
  if (available == 0) {//Si no hay MOMs funcionando, esta toma ese rol
    console.log("No available!!!");
  } else {
    setTimeout(function () { checkHosts(); }, 2000);//Si ya hay una MOM funcional, vuelve a mirar por si pierde funcionalidad
  }
}

const microService = grpc.loadPackageDefinition(packageDefinition).MicroService;

function main() {
  for (let i = 0; i < HOSTS.length; i++) {//Se inicia la conexion con todos los micro servicios
    CurrentHosts[i + 1] = new microService(HOSTS[i], grpc.credentials.createInsecure());
  }
  checkHosts();//Se mira si ya hay un MOM principal, o toma ese rol
};

main();