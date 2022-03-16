import React from 'react'
import './navbar.css'
import logo from '../../assets/logo.png'
import {  Link } from "react-router-dom";

const Menu = () => (
  <>
     <Link to="/"><p>Draft</p> </Link>
     <Link to="/"><p>Standings</p> </Link>
     <Link to="/"><p>Teams</p> </Link>
    
  </>
 )

 const Navbar = () => {
  return (
    <div className='navbar'>
      <div className="navbar-links">
        <div className="navbar-links_logo">
          <img src={logo} alt="logo" />
          <Link to="/"> 
            <h1>JFL</h1>
          </Link>
        </div>
        <div className="navbar-links_container">
         <Menu />
        </div>
      </div>
    </div>
  )
}

export default Navbar
