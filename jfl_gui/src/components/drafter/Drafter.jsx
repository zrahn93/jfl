import React from 'react';
import './drafter.css'
import "slick-carousel/slick/slick.css"; 
import "slick-carousel/slick/slick-theme.css";
import Slider from "react-slick";
import { Link } from 'react-router-dom';

class Drafter extends React.Component {
    nfl_images = {
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

    constructor(props) {
        super(props);

        this.state = {
            current_week: -1,
            draft_data: [],
            team_data: [],
        }

        this.getStateData();
    }

    async getStateData() {
        fetch(process.env.REACT_APP_API_IP + '/api/current_week', {method: 'GET'})
        .then(response => response.json())
        .then(week_data => {
            //console.log("week_data: ")
            //console.log(week_data)
            this.setState({current_week: week_data.current_week})
            fetch(process.env.REACT_APP_API_IP + '/api/draft_status?week=' + week_data.current_week, {method: 'GET'})
            .then(response => response.json())
            .then(draft_data => {
                //console.log("draft_data: ")
                //console.log(draft_data)
                fetch(process.env.REACT_APP_API_IP + '/api/teams_playing?week=' + week_data.current_week, {method: 'GET'})
                .then(response => response.json())
                .then(team_data => {
                    //console.log("team_data: ")
                    //console.log(team_data)
                this.setState({ 
                    current_week: week_data.current_week,
                    draft_data: draft_data,
                    team_data: team_data
                })
                })
            })
            }
        );
    }

  render_draft() {
    var settings = {
        dots: false, infinite: false, speed: 500, slidesToShow: 5, slidesToScroll: 1, swipeToSlide:true,
        responsive: [
        { breakpoint: 1160, settings: { slidesToShow: 4, slidesToScroll: 1, swipeToSlide:true } },
        { breakpoint: 950, settings: { slidesToShow: 4, slidesToScroll: 1, swipeToSlide:true, } },
        { breakpoint: 825, settings: { slidesToShow: 3, slidesToScroll: 1, } },
        { breakpoint: 550, settings: { slidesToShow: 3, slidesToScroll: 1 } },
        { breakpoint: 470, settings: { slidesToShow: 2, slidesToScroll: 1, } },
        { breakpoint: 400, settings: { slidesToShow: 2, slidesToScroll: 1, variableWidth: true, } }
        ]
    };

    //user_selections.draft_order, users.user_id, users.name, teams.team_id, teams.name
    const PICK_NUM = 0;
    const USER_ID = 1;
    const NAME = 2;
    const TEAM_ID = 3;
    const TEAM = 4;

    var div_components = [];
    for (var i = 0; i < this.state.draft_data.length; i++) {
        const pick = this.state.draft_data[i];

        var selectionStyle = {};
        var selection = null;
        if (pick[TEAM] != null) {
            const selection_pic = require('../../assets/' + this.nfl_images[pick[TEAM]]);
            selectionStyle = {
                backgroundImage: `url(${selection_pic})`,
                backgroundPosition: 'center',
                backgroundSize: '200% 200%',
            }
            selection = <p className='slider-card-selection'>{pick[TEAM]}</p>
        }

        //TODO: some team names fall out of the slider-card... Maybe force the text to two rows
        const profile_pic = require('../../assets/user.png');
        var card = <div className='slider-card' >
            <div className='slider-card' style={selectionStyle} >
                <div className='opake-bg'>
                    <p className='slider-card-number'>{pick[PICK_NUM]}</p>
                    <div className="slider-img">
                    <img className='user-card-thumbnail' src={profile_pic} alt="centered image" />
                    </div>
                    <Link to={`/profile/` + pick[USER_ID]}>
                    <p className='slider-card-name'>{pick[NAME]}</p>
                    </Link>
                    <p className='slider-card-price'>{selection}</p>
                </div>
            </div>
        </div>;

        div_components.push(card)
    }

    return (
        <div className='header section__padding'>
            <div className="header-slider">
                <h1>Draft</h1>
                <Slider {...settings} className='slider'>
                    {div_components}
                </Slider>
            </div>
        </div>
    )
  }

    render_teams() {
        const _self = this;
        const DRAFT_PICK = 0
        const USER_ID = 1
        const USER_NAME = 2
        const TEAM_ID = 3
        const DRAFT_SELECTION = 4;

        var selected_teams = []
        for (let i = 0; i < this.state.draft_data.length; i++) {
            selected_teams.push(this.state.draft_data[i][DRAFT_SELECTION])
        }

        var available_teams = []
        for (let i = 0; i < this.state.team_data.length; i++) {
            if (!selected_teams.includes(this.state.team_data[i].team))
            available_teams.push(this.state.team_data[i])
        }

        var team_elements = []
        for (let i = 0; i < available_teams.length; i++) {
            const team = available_teams[i];
            const opponent_str = team.home ? "vs " + team.opponent : "at " + team.opponent;
            const team_logo = require('../../assets/' + this.nfl_images[team.team]);
            const wins = (team.wins == null) ? 0 : team.wins
            const losses = (team.losses == null) ? 0 : team.losses
            const ties = (team.ties == null) ? 0 : team.ties

            var spread_str = "-"
            if (team.odds != null)
            spread_str = team.odds > 0 ? "+" + team.odds : team.odds

            const draft_button = <button className="primary-btn" onClick={
            function() {
                for (var j = 0; j < _self.state.draft_data.length; j++) {
                    if (_self.state.draft_data[j][DRAFT_SELECTION] == null) {
                        fetch(process.env.REACT_APP_API_IP + '/api/pick_team', {
                            method: 'POST',
                            body: JSON.stringify({
                                'user_id': _self.state.draft_data[j][USER_ID],
                                'week': _self.state.current_week,
                                'pick': _self.state.draft_data[j][DRAFT_PICK],
                                'team': team.team
                            })
                        })
                        .then(response => response.json())
                        .then(() => {
                            _self.state.draft_data[j][DRAFT_SELECTION] = team.team;
                            _self.setState({ draft_data: _self.state.draft_data });
                        })
                        break
                    }
                }
            }}>Draft</button>

            const team_element = <div className="card-column" >
                <div className="bids-card">
                    <div className="bids-card-top">
                        <img src={team_logo} alt="" />
                        <div className="bids-record-title">
                            <p>({wins}-{losses}-{ties})</p>
                        </div>
                        <Link to={`/post/` + team.team_id}>
                            <p className="bids-title">{team.team}</p>
                        </Link>
                    </div>
                    <div className="bids-card-bottom bids-opponent-title">
                        <p>{opponent_str}</p>
                    </div>
                    <div className="bids-odds-title">
                        <p>{spread_str}</p>
                    </div>
                    <div className="draft-selection">
                        {draft_button}
                    </div>
                </div>
            </div>

            team_elements.push(team_element)
        }

        return (
            <div className='bids section__padding'>
                <div className="bids-container">
                    <div className="bids-container-text">
                    <h1>Available Teams</h1>
                    </div>
                    <div className="bids-container-card">
                        {team_elements}
                    </div>
                    <div className="reset" onClick={() => {
                        fetch(process.env.REACT_APP_API_IP + '/api/reset_week', {
                            method: 'POST',
                            body: JSON.stringify({'week': _self.state.current_week})
                        })
                        .then(response => response.json())
                        .then(() => {_self.getStateData();})
                    }}>
                        <button>Clear Draft Picks</button>
                    </div>
                    <div className="sim-games" onClick={() => {
                        var all_teams_picked = true;
                        for (var i = 0; i < _self.state.draft_data.length; i++) {
                            if (_self.state.draft_data[i][DRAFT_SELECTION] == null) {
                                all_teams_picked = false;
                            }
                        }
                        if (all_teams_picked) {
                            fetch(process.env.REACT_APP_API_IP + '/api/sim_games', {
                                method: 'POST',
                                body: JSON.stringify({'week': _self.state.current_week})
                            })
                            .then(response => response.json())
                            .then(() => {_self.getStateData();})
                        } else {
                            alert("Not all teams selected! Go with the Best Bird Available");
                        }
                    }}>
                        <button>Simulate Game Results</button>
                    </div>
                    <div className="complete-week" onClick={() => {
                        var all_games_finished = true
                        for (var i = 0; i < _self.state.team_data.length; i++) {
                            if (!_self.state.team_data[i]["finished"]) {
                                all_games_finished = false;
                            }
                        }
                        if (!all_games_finished) {
                            alert("Not all games finished! Smash that 'Simulate Game Results' button");
                        }
                        else {
                            fetch(process.env.REACT_APP_API_IP + '/api/complete_week', {
                                method: 'POST',
                                body: JSON.stringify({'week': _self.state.current_week})
                            })
                            .then(response => response.json())
                            .then(() => {_self.getStateData();})
                        }
                    }}>
                        <button>Complete Week</button>
                    </div>
                </div>
            </div>
        )
    }

    render() {
        return <div>
            {this.render_draft()}
            {this.render_teams()}
        </div>;
    }
}

export default Drafter
