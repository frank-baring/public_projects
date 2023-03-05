import React from 'react';
import Navbar from './components/Nav/Navbar';
import { useState } from "react";
import './App.css';
import logo from './img/mainimage.jpeg';

function App(){

    const [alignment] = useState("left");

  return(
    <div className="App">
        <Navbar />
        <h1 align={alignment} className="font-link">Project Portfolio</h1>
        <div align={alignment} className="font-link">Frank Baring</div>
        <hr
            style={{
                background: "#808080",
                height: "2px",
                border: "none",
            }}
        />
        <img src = {logo} className = "logo" alt ="" align={alignment} height="400" width="340"/>
    </div>
  );
}

export default App;
