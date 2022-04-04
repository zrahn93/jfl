import React, { useState } from 'react';
import './league.css'
import { Link } from 'react-router-dom';

const League = () => {
  const [season_selections, set_season_selections] = useState([])

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

  async function getStateData() {
    fetch(process.env.REACT_APP_API_IP + '/api/season_selections')
    .then(response => response.json())
    .then(data => {
        //console.log(data)
        set_season_selections(data)
      }
    );
  }

  if (season_selections.length === 0)
    getStateData();

    var season_elements = []
    for (var i = 0; i < season_selections.length; i++){
        var week_results = season_selections[i];
        var week_elements = []
        for (const [user_name, user_results] of Object.entries(week_results['users'])) {
            var games = []

            if (user_results.length > 0) {
                for (var idx = 0; idx < user_results.length; idx++) {
                    var selection = user_results[idx];
                    if (selection[3] != null) {
                        const team_pic = require('../../assets/' + nfl_images[selection[4]]);
                        games.push(
                            <div className="league-card-column" >
                                <div className={"league-card selection-result-" + selection[6]}>
                                    <div className="league-card-top">
                                        <img src={team_pic} alt="" />
                                        <Link to={`/post/` + selection[3]}>
                                            <p className="team-title">{selection[4]}</p>
                                        </Link>
                                    </div>
                                </div>
                            </div>
                        )
                    }
                }
                if (games.length > 0) {
                    week_elements.push(
                    <div className='league section__padding'>
                        <div className="league-container">
                            <div className="league-container-user">
                                <h3>
                                    <Link to={`/profile/` + user_results[0][1]}>
                                        {user_name}
                                    </Link>
                                </h3>
                            </div>
                            <div className="league-container-card">
                                {games}
                            </div>
                        </div>
                    </div>
                    )
                }
            }
        }
        if (week_elements.length > 0) {
            season_elements.push(
                <div id={week_results['week_id']} className='league section__padding'>
                    <div className="league-container">
                        <div className="league-container-week">
                        <h1>Week {week_results['week']}</h1>
                        </div>
                        <div className="league-container-card">
                            {week_elements}
                        </div>
                    </div>
                </div>
            )
            //TODO: Add user/player bye weeks
        }
    }

    return (
        <div className='league section__padding'>
            <div className="league-info">
            <div>
                {season_elements}
            </div>
            </div>
        </div>
    );
};

export default League;
