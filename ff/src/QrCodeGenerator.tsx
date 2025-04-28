import { useState, useEffect, useRef } from 'react'
import styles from './user.module.css'
import { QRCodeSVG } from "qrcode.react"

type Props = {
    mode: "input" | "random" | "random_with_prerequisites"
    elements?: React.ReactElement<HTMLInputElement>[]
    callbackWhenGenerated?: (text: string | null) => undefined
    genButtonDisabled?: boolean
}

function randomDigits(amountOfDigits: number): string {
    let array: number[] = []
    for (let i = 0; i < amountOfDigits; i++) {
        array.push(Math.floor(Math.random() * 10))
    }
    return array.join("")
}

const QrCodeGenerator: React.FC<Props> = ({ mode, elements, callbackWhenGenerated, genButtonDisabled }) => {
    const [textToGenerate, setTextToGenerate] = useState<string>("")
    const button = useRef<HTMLButtonElement | null>(null)
    const random = useRef<string | null>(null)

    useEffect(() => {
        const btn = document.getElementById("gen_button") as HTMLButtonElement | null
        if (btn) {
            btn.style.backgroundColor = textToGenerate === "" ? "gray" : "#007bff"
            btn.disabled = textToGenerate === ""
        }
    }, [textToGenerate])

    useEffect(() => {
        random.current = randomDigits(30)
        const wrong = (mode === "random_with_prerequisites" && !elements) || 
                      (mode === "input" && elements) || 
                      (mode === "random" && elements)
        if (wrong) {
            throw new Error("Modes wrong")
        }
    }, [])

    useEffect(() => {
        if (mode === "random_with_prerequisites" && elements) {
            let noFill = elements.some(el => el.props.value.length === 0)
            const btn = document.getElementById("gen_button") as HTMLButtonElement

            btn.style.backgroundColor = !genButtonDisabled && !noFill ? "#007bff" : "gray"
            btn.disabled = !genButtonDisabled && !noFill ? false : true

            console.log(genButtonDisabled, noFill)
        }
    })

    function generate() {
        const qr = document.getElementById("qr")
        const btn = document.getElementById("gen_button")
        if (qr) qr.style.display = "flex"
        if (btn) btn.style.display = "none"
        if (callbackWhenGenerated) callbackWhenGenerated((mode === "input" ? textToGenerate : random.current))
    }

    return (
        <div id="creation" style={{display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", width: "100vw"}}>
            {mode === "random" ? "" : (
                mode === "random_with_prerequisites"
                    ? elements
                    : <input
                        style={{ marginBottom: "10px" }}
                        value={textToGenerate}
                        onChange={(e) => setTextToGenerate(e.target.value)}
                        placeholder='Text to generate'
                    />
            )}
            <br />
            <button
                id="gen_button"
                style={{ marginBottom: "10px" }}
                ref={button}
                className={styles.blue}
                onClick={() => generate()}
            >
                Create account and account's QR
            </button>

            <div
                id="qr"
                style={{
                    display: "none",
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
                <QRCodeSVG size={128} value={mode === "input" ? textToGenerate : (random.current || "")} />
                <div>
                    {mode === "input" ? (
                        <h2>{`Generated with text: ${textToGenerate}`}</h2>
                    ) : (
                        mode === "random_with_prerequisites" && elements ? (
                            [elements.map((element) => (
                                <h2>{element.props.placeholder}: {element.props.value}</h2>
                            )), <h6>{`Number: ${random.current}`}</h6>]
                        ) : (
                            <h3>{`Number: ${random.current}`}</h3>
                        )
                    )}
                </div>
            </div>
        </div>
    )
}

export default QrCodeGenerator
