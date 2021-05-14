import React, { useState } from 'react';
import './css/App.css';
import Header from './components/header.js';
import Chat from './components/chat.js';


function App() {
  return (
    <div className="App">
      <Header />
      <Chat chat_id="7c40c1cc-d0b4-45d6-972d-a48d12e51d71"/>
    </div>
  );
}

export default App;
