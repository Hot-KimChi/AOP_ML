import logo from './logo.svg';
import './App.css';
import { useState } from 'react'

function App() {

  let server_list = ["K2", "Juniper"];
  


  return (
    <div className="App">
      <div className="black-nav">
        <h4>AOP MeasSetGeneration</h4>

        <h3>{server_list}</h3>
      </div>
      
    </div>
  );
}

export default App;
