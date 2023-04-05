import React from 'react';
import { useState } from "react";
import '../App.css';
import logo from '../mainimage.jpeg';

function Home() {

    const [alignment] = useState("left");

    return(
        <div className="Home">
            <h1 align={alignment} className="font-link">Project Portfolio</h1>
            <div align={alignment} className="font-link">Frank Baring</div>
            <hr
                style={{
                    background: "#808080",
                    height: "2px",
                    border: "none",
                }}
            />
            <img src = {logo} className = "logo" alt ="" align={alignment} height="400" width="340" style={{marginRight: "10px"}}/>
            <div className="font-link">Hi, welcome to my project portfolio. This is where I post papers, articles,
                analysis and everything in between. Enjoy! </div>
        </div>
    );
}

export default Home;