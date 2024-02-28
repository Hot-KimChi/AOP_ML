import logo from './logo.svg';
import './App.css';
import { useState } from 'react'

function App() {

  const server_list = ["K2", "Juniper"];
  const [title, title_pro] = useState('남자코트추천')
  

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
