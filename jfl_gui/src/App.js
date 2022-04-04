import './App.css';
import React from 'react'
import {Navbar,Footer} from './components'
import {Home,Profile,Item,League,Standings} from './pages'
import { Routes, Route } from "react-router-dom";

function App() {

  return (
    <div>
      <Navbar />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/league" element={<League />} />
            <Route path="/standings" element={<Standings />} />
            <Route path=":item/:id" element={<Item />} />
            <Route path="/profile/:id" element={<Profile />} />
          </Routes>
      <Footer />
    </div>
  );
}

export default App;
