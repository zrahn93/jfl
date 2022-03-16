import './App.css';
import React from 'react'
import {Navbar,Footer} from './components'
import {Home,Profile,Item} from './pages'
import { Routes, Route } from "react-router-dom";

function App() {

  return (
    <div>
      <Navbar />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path=":item/:id" element={<Item />} />
            <Route path="/profile/:id" element={<Profile />} />
          </Routes>
      <Footer />
    </div>
  );
}

export default App;
