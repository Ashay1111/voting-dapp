import React, { useState } from 'react'
import algosdk from 'algosdk'
import algodClient from './algosdkConfig'

function App() {
  const [address, setAddress] = useState('')
  const [mnemonic, setMnemonic] = useState('')
  const [appId, setAppId] = useState('')
  const [status, setStatus] = useState('')

  const connectWallet = () => {
    try {
      const privateKey = algosdk.mnemonicToSecretKey(mnemonic)
      setAddress(privateKey.addr)
      setStatus('Wallet connected')
    } catch (e) {
      setStatus('Invalid mnemonic')
    }
  }

  const vote = async (option) => {
    try {
      const { addr, sk } = algosdk.mnemonicToSecretKey(mnemonic)
      const params = await algodClient.getTransactionParams().do()
      const txn = algosdk.makeApplicationNoOpTxnFromObject({
        from: addr,
        appIndex: parseInt(appId),
        appArgs: [new Uint8Array(Buffer.from(option))],
        suggestedParams: params
      })
      const signed = txn.signTxn(sk)
      const { txId } = await algodClient.sendRawTransaction(signed).do()
      setStatus(`Submitted: ${txId}`)
    } catch (e) {
      setStatus('Transaction failed')
    }
  }

  return (
    <div style={{ padding: '20px' }}>
      <h1>Voting DApp</h1>
      <input
        placeholder="Mnemonic"
        value={mnemonic}
        onChange={(e) => setMnemonic(e.target.value)}
        style={{ width: '400px' }}
      />
      <br />
      <input
        placeholder="App ID"
        value={appId}
        onChange={(e) => setAppId(e.target.value)}
      />
      <br />
      <button onClick={connectWallet}>Connect</button>
      <br /><br />
      {address && (
        <>
          <p>Connected as: {address}</p>
          <button onClick={() => vote('voteA')}>Vote A</button>
          <button onClick={() => vote('voteB')}>Vote B</button>
        </>
      )}
      <p>{status}</p>
    </div>
  )
}

export default App
