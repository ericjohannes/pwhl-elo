import "./App.css"
import {convertAndCapitalize, pubDateString, roundProjection} from "./utils"
import game_projections from "./assets/game_projections.json"

const compareFn = (a, b) =>{
    if (a.date < b.date) {
      return -1;
    } else if (a.date < b.date) {
      return 1;
    }
    // a must be equal to b
    return 0;
  }

export const projectionTable = ()=>(
    <section>
        <h1 className="oswald-bold">Projections for Upcoming Games</h1>
        {
            game_projections.sort(compareFn).map((entry, i)=>{
                return(
                    <>
                        <h3>{pubDateString(entry.date)}</h3>
                        <table key={"projection-table-" + i } className="rating-table">
                            <thead className="quattrocento-bold" key={"projection-table-head" + i}>
                                <tr key={"projection-table-header-row" + i}>
                                    <th key={"projection-table-teams-head" + i} className="team-name table-head-cell">Teams</th>
                                    <th key={"projection-table-home-head" + i} className="team-rating table-head-cell">Home</th>
                                    <th key={"projection-table-rating-head" + i} className="team-rating table-head-cell">Rating</th>
                                    <th key={"projection-table-proj-head" + i} className="team-rating table-head-cell">Win</th>
                                </tr>
                            </thead>
                            <tbody className="quattrocento-regular">
                                {/* away team */}
                                <tr key={"projection-table-away-row" + i} className="data-row">
                                    <td 
                                        className="team-name table-left-cell" 
                                        key={"team-name-" + i}>{convertAndCapitalize(entry.away_team)}
                                    </td>
                                    <td className="team-rating" key={"is-away" + i}>Away</td>
                                    <td 
                                        className="team-name num-col" 
                                        key={"away-rating-" + i}>{entry.elo_before_away}
                                    </td>
                                    <td 
                                        className="team-name num-col" 
                                        key={"away-projection-" + i}>{roundProjection(entry.expected_win_away)}
                                    </td>

                                </tr>
                                {/* home team */}
                                <tr key={"projection-table-home-row" + i} className="data-row">
                                    <td 
                                        className="team-name table-left-cell" 
                                        key={"team-name-" + i}>{convertAndCapitalize(entry.home_team)}
                                    </td>
                                    <td className="team-rating" key={"is-home" + i}>Home</td>
                                    <td 
                                        className="team-name num-col" 
                                        key={"away-rating-" + i}>{entry.elo_before_home}
                                    </td>
                                    <td 
                                        className="team-name num-col" 
                                        key={"away-projection-" + i}>{roundProjection(entry.expected_win_home)}
                                    </td>

                                </tr>
                            </tbody>

                        </table>
                    </>
                )
            })
        }
    </section>
)
