// Resume.js
import React, {useState} from 'react';

function Contact() {

    const [alignment] = useState("left");

    return (
        <div>
            <h1 className="font-link">Feel free to get in touch</h1>
            <hr
                style={{
                    background: "#808080",
                    height: "2px",
                    border: "none",
                }}
            />
            <div align={alignment} className="font-link" style={{marginBottom: '10px'}}>
                <a href="frankbaring@gmail.com">frankbaring@gmail.com</a>
            </div>
            <div align={alignment} className="font-link" style={{marginBottom: '10px'}}>
                <a href="https://www.linkedin.com/in/frank-baring-634824165/">LinkedIn</a>
            </div>
            <div align={alignment} className="font-link" style={{marginBottom: '10px'}}>
                <a href="https://github.com/frank-baring/public">GitHub</a>
            </div>
        </div>
    );
}

export default Contact;