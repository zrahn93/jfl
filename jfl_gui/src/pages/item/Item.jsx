import React, { useState } from 'react';
import { useParams } from 'react-router-dom'
import './item.css'
import opponent from '../../assets/nfl-dallas-cowboys-team-logo-2.png'


function Item() {
  const [team_name, set_team_name] = useState()
  const [team_image, set_team_image] = useState()
  const [wins, set_wins] = useState()
  const [losses, set_losses] = useState()
  const [ties, set_ties] = useState()

  const nfl_images = {
    "Arizona Cardinals": "nfl-arizona-cardinals-team-logo-2.png",
    "Atlanta Falcons": "nfl-atlanta-falcons-team-logo-2.png",
    "Baltimore Ravens": "nfl-baltimore-ravens-team-logo-2.png",
    "Buffalo Bills": "nfl-buffalo-bills-team-logo-2.png",
    "Carolina Panthers": "nfl-carolina-panthers-team-logo-2.png",
    "Chicago Bears": "nfl-chicago-bears-team-logo-2.png",
    "Cincinnati Bengals": "nfl-cincinnati-bengals-team-logo.png",
    "Cleveland Browns": "nfl-cleveland-browns-team-logo-2.png",
    "Dallas Cowboys": "nfl-dallas-cowboys-team-logo-2.png",
    "Denver Broncos": "nfl-denver-broncos-team-logo-2.png",
    "Detroit Lions": "nfl-detroit-lions-team-logo-2.png",
    "Green Bay Packers": "nfl-green-bay-packers-team-logo-2.png",
    "Houston Texans": "nfl-houston-texans-team-logo-2.png",
    "Indianapolis Colts": "nfl-indianapolis-colts-team-logo-2.png",
    "Jacksonville Jaguars": "nfl-jacksonville-jaguars-team-logo-2.png",
    "Kansas City Chiefs": "nfl-kansas-city-chiefs-team-logo-2.png",
    "Los Angeles Chargers": "nfl-los-angeles-chargers-team-logo-2.png",
    "Los Angeles Rams": "los-angeles-rams-2020-logo.png",
    "Miami Dolphins": "nfl-miami-dolphins-team-logo-2.png",
    "Minnesota Vikings": "nfl-minnesota-vikings-team-logo-2.png",
    "New England Patriots": "nfl-new-england-patriots-team-logo-2.png",
    "New Orleans Saints": "nfl-new-orleans-saints-team-logo-2.png",
    "New York Giants": "nfl-new-york-giants-team-logo-2.png",
    "New York Jets": "nfl-new-york-jets-team-logo.png",
    "Las Vegas Raiders": "nfl-oakland-raiders-team-logo.png",
    "Philadelphia Eagles": "nfl-philadelphia-eagles-team-logo-2.png",
    "Pittsburgh Steelers": "nfl-pittsburgh-steelers-team-logo-2.png",
    "San Francisco 49ers": "nfl-san-francisco-49ers-team-logo-2.png",
    "Seattle Seahawks": "nfl-seattle-seahawks-team-logo-2.png",
    "Tampa Bay Buccaneers": "tampa-bay-buccaneers-2020-logo.png",
    "Tennessee Titans": "nfl-tennessee-titans-team-logo-2.png",
    "Washington Commanders": "washington-commanders-logo.png",
  }

  async function getStateData(id) {
    fetch(process.env.REACT_APP_API_IP + '/api/team_data?team_id=' + id, {method: 'GET'})
    .then(response => response.json())
    .then(data => {
        console.log(data)
        set_team_name(data[0])
        set_team_image(nfl_images[data[0]])
        set_wins(data[1])
        set_losses(data[2])
        set_ties(data[3])
      }
    );
  }

  let params = useParams();
  const id = params.id;

  var image = <div/>
  if (team_image != null) {
    const team_pic = require('../../assets/' + team_image);
    image = <img src={team_pic} alt="item" />
  }

  if (team_name == null)
    getStateData(id);

  return( 
      <div className='item section__padding'>
        <div className="item-image">
          {image}
        </div>
          <div className="item-content">
            <div className="item-content-title">
              <h1>{team_name}</h1>
              <p>({wins}-{losses}-{ties})</p>
            </div>
            <div className="item-content-creator">
              <div><p>Schedule</p></div>
              <div>
                <img src={opponent} alt="creator" />
                <p>W </p>
              </div>
            </div>
            <div className="item-content-detail">
              <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book</p>
            </div>
          </div>
      </div>
  )
}

export default Item;
