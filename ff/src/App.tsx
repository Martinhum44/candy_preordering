import React, { useState, useRef } from 'react'
import styles from './user.module.css';
import QrCodeGenerator from './QrCodeGenerator';


const App: React.FC = () => {
    const [PIN, setPIN] = useState<string>("")
    const [name, setName] = useState<string>("")
    const [state, setState] = useState<"creation" | "created" | "login">("creation")
    const [disabled, setDisabled] = useState<boolean>(true)
    const [conf, setConf] = useState<boolean>(true)
    const [loginPIN, setLoginPIN] = useState<string>("")
    const [loginAccNumber, setLoginAccNumber] = useState<string>("")
    
    const nameRef = useRef<HTMLInputElement>(null)
    const PINRef = useRef<HTMLInputElement>(null)
    const codeRef = useRef<string>(null)
    const accountGeneratedRef = useRef<HTMLHeadingElement>(null)
    const confirmCreateWalletRef = useRef<HTMLButtonElement>(null)

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
        const json = await res.json()

        if (json.success) {
            alert(json.msg)
            setState("created")
            console.log(json)
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
                <div style={{marginTop: "10px"}}>
                    <button onClick={() => setState("login")} style={{display: "inline-block", width: "75px", height: "30px", fontSize: "12px", marginRight: "10px"}} className={styles.blue}>Log in</button>
                    <button onClick={() => setState("creation")} style={{display: "inline-block", width: "120px", height: "30px", fontSize: "12px"}} className={styles.blue}>Create Account</button>
                </div>
            </div>
            <div id="login" style={{ display: state === "login" ? "block" : "none" }}>
                <h1>Log in to your FUNPARK wallet!</h1>
                <input placeholder='Account Number' value={loginAccNumber} style={{ marginBottom: "10px", display: "block" }} onChange={(e) => { setLoginAccNumber(e.target.value) }} type="text" />
                <input placeholder='Account PIN' value={loginPIN} style={{ marginBottom: "10px", display: "block" }} onChange={(e) => { setLoginPIN(e.target.value) }} type="text" />
                <button onClick={() => setState("login")} style={{display: "inline-block", marginRight: "10px"}} className={styles.blue}>Log in</button>
            </div>
        </div>
    )
}

export default App
