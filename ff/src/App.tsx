import React, { useState, useEffect, useRef } from 'react'
import styles from './user.module.css';
import QrCodeGenerator from './QrCodeGenerator';
import { Html5QrcodeScanner } from 'html5-qrcode';
import { QRCodeSVG } from "qrcode.react"

type Account = {
    name: string,
    id: string,
    balance: number
}

type JsonResultAccount = {
    msg: string
    account: Account
    success: boolean
    error: undefined
} | {
    msg: string
    success: boolean
    account: undefined
    error: string | undefined
}

const App: React.FC = () => {
    const [PIN, setPIN] = useState<string>("")
    const [scan, setScan] = useState<boolean>(false)
    const [name, setName] = useState<string>("")
    const [state, setState] = useState<"creation" | "logged-in" | "login">("creation")
    const [disabled, setDisabled] = useState<boolean>(true)
    const [conf, setConf] = useState<boolean>(true)
    const [loginPIN, setLoginPIN] = useState<string>("")
    const [loginAccNumber, setLoginAccNumber] = useState<string>("")
    
    const nameRef = useRef<HTMLInputElement>(null)
    const PINRef = useRef<HTMLInputElement>(null)
    const codeRef = useRef<string>(null)
    const accountGeneratedRef = useRef<HTMLHeadingElement>(null)
    const confirmCreateWalletRef = useRef<HTMLButtonElement>(null)
    const [accData, setAccData] = useState<Account | undefined>()

    useEffect(() => {
        const scanner = new Html5QrcodeScanner("reader", {
            qrbox: { width: 250, height: 250 },
            fps: 5,
        }, false)
    
        scanner.render((data) => {
            alert("Account number scanned: "+data)
            setLoginAccNumber(data)
            setScan(false)
        }, (err) => {
            //console.error(err)
        })
    }, [])

    async function create() {
        console.log(document.getElementById("gen_button"))

        const res = await fetch("http://localhost:3000/api/create-account", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: name,
                pin: PIN,
                id: codeRef.current
            })
        })
        const json: JsonResultAccount = await res.json()

        if (json.success) {
            alert(json.msg)
            setState("logged-in")
            setAccData(json.account)
        } else {
            alert(json.msg)
        }
    }

    return (
        <div id="container" style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", height: "100vh", width: "100vw" }}>
            <div id="creation" style={{ display: state === "creation" ? "block" : "none" }}>
                <h1>Create a FUNPARK wallet!</h1>
                <h2 style={{ display: "none" }} ref={accountGeneratedRef}>Wallet generated!</h2>
                <QrCodeGenerator genButtonDisabled={disabled} mode="random_with_prerequisites" elements={[<input placeholder='Name' ref={nameRef} value={name} style={{ marginBottom: "10px", display: "block" }} onChange={(e) => { setName(e.target.value) }} type="text" />, <input placeholder='PIN' ref={PINRef} value={PIN} style={{ marginBottom: "10px", display: "block" }}
                onChange={
                    (e) => { 
                        setPIN(e.target.value); 
                        if (e.target.value.length != 4) { 
                            setDisabled(true);
                        } else {
                            setDisabled(false);
                        }
                    } 
                }
                type="number" />]} 
                callbackWhenGenerated={(text) => { 
                    if (nameRef.current != null) nameRef.current.style.display = "none"; 
                    if (PINRef.current != null) PINRef.current.style.display = "none"; 
                    if (confirmCreateWalletRef.current != null) {
                        confirmCreateWalletRef.current?.classList.remove(styles.gray); 
                        confirmCreateWalletRef.current?.classList.add(styles.blue);
                        setConf(false); 
                    } 
                    codeRef.current = text;
                }}/>
                <button onClick={create} style={{ marginTop: "10px" }} className={styles.gray} disabled={conf} ref={confirmCreateWalletRef}>Confirm create wallet</button>
            </div>
            <div id="login" style={{ display: state === "login" ? "flex" : "none", flexDirection: "column", alignItems: "center"}}>
                <h1>Log in to your FUNPARK wallet!</h1>
                <button onClick={() => setScan(!scan)} style={{ marginBottom: "10px" }} className={styles.blue}>{!scan ? "Scan Account QR" : "Stop Scanning"}</button>
                <div style={{display: scan ? "block" : "none", marginTop: "10px", marginBottom: "10px"}}>
                    <h3>Scan QR for account number</h3>
                    <div id="reader" style={{ width: "100%" }}></div>
                </div>
                <input placeholder='Account Number' value={loginAccNumber} style={{ marginBottom: "10px", display: "block" }} onChange={(e) => { setLoginAccNumber(e.target.value) }} type="text" />
                <input placeholder='Account PIN' value={loginPIN} style={{ marginBottom: "10px", display: "block" }} onChange={(e) => { setLoginPIN(e.target.value) }} type="text" />
                <button onClick={async() => { 
                    console.log(loginAccNumber, loginPIN)
                    const res = await fetch(`http://localhost:3000/api/get-account/`, {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({PIN: loginPIN, ID: loginAccNumber})
                    })
                    const json: JsonResultAccount = await res.json()
                    if(!json.success) {
                        console.log(json)
                        console.log(json.error)
                        return alert(json.msg) 
                    }
                    setAccData(json.account)
                    setState("logged-in");
                }} style={{display: "inline-block", marginRight: "10px"}} disabled={loginPIN.length != 4 || loginAccNumber.length != 30 ? true: false} className={loginPIN.length != 4 || loginAccNumber.length != 30 ? styles.gray: styles.blue}>Log in</button>
            </div>
            <div id="logged-in" style={{ display: state === "logged-in" ? "flex" : "none", flexDirection: "column", alignItems: "center"}}>
                <h1>Welcome {accData && accData.name}</h1>
                <div
                    id="qr"
                    style={{
                        display: "block",
                        alignItems: "center",
                        justifyContent: "center",
                        borderRadius: "10px",
                        height: "350px",
                        width: "200px",
                        backgroundColor: "lightgray",
                        flexDirection: "column",
                        textAlign: "center",
                        overflowX: "scroll"
                    }}
                >
                    <h2 style={{ display: "block" }}>QR</h2>
                    <QRCodeSVG size={128} value={accData && accData.id} />
                    <h3>Name: {accData && accData.name}</h3>
                    <h3>Balance: ${accData && accData.balance}</h3>
                    <h6>ID: {accData && accData.id}</h6>
                </div>
            </div>
            <div style={{marginTop: "10px", display: state === "creation" || state === "login" ? "block" : "none"}}>
                    <button onClick={() => setState("login")} style={{display: "inline-block", width: "75px", height: "30px", fontSize: "12px", marginRight: "10px"}} className={styles.blue}>Log in</button>
                    <button style={{display: "inline-block", width: "120px", height: "30px", fontSize: "12px", marginRight: "10px"}} onClick={() => {window.location.reload()}} className={styles.blue}>Create account</button>
            </div>
        </div>
    )
}

export default App
