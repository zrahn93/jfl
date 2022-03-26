import React, {useState} from 'react'
import './navbar.css'
import { RiMenu3Line, RiCloseLine } from 'react-icons/ri';
import logo from '../../assets/jfl_logo.png'
import {  Link } from "react-router-dom";

const Menu = () => (
  <>
     <Link to="/"><p>Draft</p> </Link>
     <Link to="/"><p>Standings</p> </Link>
     <Link to="/"><p>Teams</p> </Link>
    
  </>
 )

 const Navbar = () => {
  const [toggleMenu,setToggleMenu] = useState(false)

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
      <div className="navbar-menu">
        {toggleMenu ? 
        <RiCloseLine  color="#fff" size={27} onClick={() => setToggleMenu(false)} /> 
        : <RiMenu3Line color="#fff" size={27} onClick={() => setToggleMenu(true)} />}
        {toggleMenu && (
          <div className="navbar-menu_container scale-up-center" >
            <div className="navbar-menu_container-links">
             <Menu />
            </div>
            <div className="navbar-menu_container-links-sign"></div>
            </div>
        )}
      </div>
    </div>
  )
}

export default Navbar
