import algosdk from 'algosdk'

const algodToken = 'youralgodtoken'
const algodServer = 'http://localhost'
const algodPort = 4001

const algodClient = new algosdk.Algodv2(algodToken, algodServer, algodPort)

export default algodClient
