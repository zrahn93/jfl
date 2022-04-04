import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import logo from '../../assets/football.gif'

import './standings.css'


const Standings = () => {
    const [standings_info, set_standings_info] = useState([])

    async function getStandings() {
        fetch(process.env.REACT_APP_API_IP + '/api/standings', {method: 'GET'})
        .then(response => response.json())
        .then(data => {
            //console.log(data)
            set_standings_info(data)
            }
        );
    }

    if (standings_info.length == 0)
        getStandings();

    var standings_elements = []
    for (var i = 0; i < standings_info.length; i++){
        if (standings_info[i]['user_name'] != null) {
            standings_elements.push(<tr key={standings_info[i]['user_name']}>
                <td class="text-left">
                    <Link to={`/profile/` + standings_info[i]['user_id']}>
                        {standings_info[i]['user_name']}
                    </Link>
                </td>
                <td class="text-left">{standings_info[i]['wins']}</td>
                <td class="text-left">{standings_info[i]['losses']}</td>
                <td class="text-left">{standings_info[i]['ties']}</td>
                <td class="text-left">{standings_info[i]['win_pct'].toFixed(3)}</td>
            </tr>)
        }
    }

    return <div>
        <div className='section__padding'>
            <div class="table-title">
                <h3>2022 JFL Standings</h3>
            </div>
            <table class="table-fill">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Wins</th>
                        <th>Losses</th>
                        <th>Ties</th>
                        <th>Win %</th>
                    </tr>
                </thead>
                <tbody>
                    {standings_elements}
                </tbody>
            </table>
        </div>
    </div>;
};

export default Standings;
