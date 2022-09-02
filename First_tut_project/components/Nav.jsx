import React from "react";
import pizzaimg from "../pic/download.jpg"

export default function Nav(){
    return(
        <nav className="nav">
            <img src = {pizzaimg} className="pizzaimg"/>
            <h3 className="logo_text">React</h3>
            <h4 className="crouse_title">React Crouse - Project 1</h4>
        </nav>
    )


}