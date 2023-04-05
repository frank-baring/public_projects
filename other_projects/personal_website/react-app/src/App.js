import React, { useState } from 'react';
import { BrowserRouter, Switch, Route, Link } from 'react-router-dom';
import './App.css';
import './components/Home';
import Home from "./components/Home";
import Resume from "./components/Resume";
import Contact from "./components/Contact";

function App() {
    const [isNavOpen, setIsNavOpen] = useState(false);

    function toggleNav() {
        setIsNavOpen(!isNavOpen);
        document.querySelector('.navbar-burger').classList.toggle('is-active');
    }

    return (
        <BrowserRouter>
            <div>
                <nav className="navbar">
                    <div className="navbar-burger" onClick={toggleNav}>
                        <span />
                        <span />
                        <span />
                    </div>
                    {isNavOpen && (
                        <ul className="navbar-menu">
                            <li>
                                <Link className="font-link" to="/">Home</Link>
                            </li>
                            <li>
                                <Link className="font-link" to="/resume">Resume</Link>
                            </li>
                            <li>
                                <Link className="font-link" to="/contact">Contact</Link>
                            </li>
                        </ul>
                    )}
                </nav>
                <Switch>
                    <Route exact path="/">
                        <Home/>
                    </Route>
                    <Route path="/resume">
                        <Resume />
                    </Route>
                    <Route path="/contact">
                        <Contact />
                    </Route>
                </Switch>
            </div>
        </BrowserRouter>
    );
}

export default App;