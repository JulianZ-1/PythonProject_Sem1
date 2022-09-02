import React from "react";
import ReactDOM from "react-dom";
import { render } from "react-dom";
import Main from "./components/Main"
import Nav from "./components/Nav";

export default function App(){
    console.log("im here")
    return(
        <div className="container">
            <Nav />
            <Main />
        </div>
    )
}