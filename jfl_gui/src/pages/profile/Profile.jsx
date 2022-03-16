import React, { useState } from 'react';
import { useParams } from 'react-router-dom'
import './profile.css'
import profile_banner from '../../assets/profile_banner.png'
import profile_pic from '../../assets/user.png'
import { Link } from 'react-router-dom';

const Profile = () => {
  const [user_name, set_user_name] = useState("")
  const [draft_selections, set_draft_selections] = useState([])
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
    //TODO: params not workings
    fetch('http://localhost:5000/api/user_data?user_id=' + id, {method: 'GET'})
    .then(response => response.json())
    .then(data => {
        console.log(data)
        set_user_name(data.user_name)
        set_draft_selections(data.draft_selections)
        set_wins(data.wins)
        set_losses(data.losses)
        set_ties(data.ties)
      }
    );
  }

  let params = useParams();
  const id = params.id;

  if (user_name === "")
    getStateData(id);

  var selection_elements = []
  for (var i = 0; i < draft_selections.length; i++){

    var games = []
    var week = draft_selections[i]
    if (week.length == 0)
      return <div/>

    for (var j = 0; j < week.length; j++) {
      var selection = week[j]
      console.log(nfl_images[selection[3]])
      if (selection[3] != null) {
        const team_pic = require('../../assets/' + nfl_images[selection[3]]);
        games.push(
          <div className="card-column" >
              <div className={"bids-card selection-win-" + selection[4]}>
                  <div className="bids-card-top">
                      <img src={team_pic} alt="" />
                      <Link to={`/post/` + selection[1]}>
                          <p className="bids-title">{selection[3]}</p>
                      </Link>
                  </div>
              </div>
          </div>
        )
      }
    }

    if (games.length > 0) {
      selection_elements.push(
        <div className='bids section__padding'>
          <div className="bids-container">
              <div className="bids-container-text">
              <h1>Week {week[0][0]}</h1>
              </div>
              <div className="bids-container-card">
                {games}
              </div>
          </div>
        </div>
      )
    }
  }


  return (
    <div className='profile section__padding'>
      <div className="profile-top">
        <div className="profile-banner">
          <img src={profile_banner} alt="banner" />
        </div>
        <div className="profile-pic">
            <img src={profile_pic} alt="profile" />
            <h3>{user_name}</h3>
            <h4>({wins}-{losses}-{ties})</h4>
        </div>
      </div>
      <div className="profile-bottom">
        <div>
          {selection_elements}
        </div>
      </div>
    </div>
  );
};

export default Profile;
