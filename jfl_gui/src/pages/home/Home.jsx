import React from 'react';
import { Drafter } from '../../components'
import logo from '../../assets/football.gif'

import './home.css'


const Home = () => {

  return <div>
    <div className='header section__padding'>
      <div className="header-content">
          <div>
            <h1>Jeff Fisher League</h1>
            <img className='shake-vertical' src={logo} alt="" />
          </div>
      </div>
    </div>
    <Drafter />
  </div>;
};

export default Home;
