import "./App.css"
import {convertAndCapitalize, pubDateString, roundProjection} from "./utils"
import game_projections from "./assets/game_projections.json"
import React, { Fragment } from 'react'

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
        <h1 className="oswald-bold">Upcoming Game Projections</h1>
        {
            game_projections.sort(compareFn).map((date, j)=>{
                return (
                    <Fragment key={"date-header"+j}>
                    <h3
                        key={"date-label" + j}
                        className="quattrocento-regular date-header"
                    >{date.date}</h3>
                    <table
                        key={"projection-table-" + j}
                        className="rating-table projection-table "
                    >
                        <thead 
                            key={"projection-table-head" + j}
                            className="fira-code-bold"
                        >
                            <tr key={"projection-table-header-row" + j}>
                                <th
                                    key={"projection-table-teams-head" + j}
                                    className="team-name table-head-cell"
                                >Teams</th>
                                <th
                                    key={"projection-table-home-head" + j}
                                    className="team-rating table-head-cell"
                                >Home</th>
                                <th
                                    key={"projection-table-rating-head" + j}
                                    className="team-rating table-head-cell num-col"
                                >Rating</th>
                                <th
                                    key={"projection-table-proj-head" + j}
                                    className="team-rating table-head-cell num-col"
                                >Win%</th>
                            </tr>
                        </thead>
                        <tbody key={"projection-table-body" + j} className="fira-code-regular">
                    {
                        date.games.map((entry, i)=>{
                            const notFirstClass = i > 0 ? " not-first-game" : "";
                            const homeFavored = entry.expected_win_home > entry.expected_win_away;
                            const keySuffix = String(i) + "-" + String(j)
                            return(
                                <Fragment key={"game-proj-header" + keySuffix}>
                                    {/* away team */}
                                    <tr 
                                        key={"projection-table-away-row" + keySuffix}
                                        className={"data-row" + notFirstClass}
                                    >
                                        <td 
                                            className="team-name table-left-cell" 
                                            key={"away-team-name-" + keySuffix}>{convertAndCapitalize(entry.away_team)}
                                        </td>
                                        <td className="team-rating" key={"is-away" + keySuffix}>Away</td>
                                        <td 
                                            className="team-name num-col" 
                                            key={"away-rating-" + keySuffix}>{entry.elo_before_away}
                                        </td>
                                        <td 
                                            className={"team-name num-col" + (homeFavored ? "" : " fira-code-bold")}
                                            key={"away-projection-" + keySuffix}>{roundProjection(entry.expected_win_away)}
                                        </td>

                                    </tr>
                                    {/* home team */}
                                    <tr key={"projection-table-home-row" + keySuffix} className="data-row">
                                        <td 
                                            className="team-name table-left-cell" 
                                            key={"home-team-name-" + keySuffix}>{convertAndCapitalize(entry.home_team)}
                                        </td>
                                        <td className="team-rating" key={"is-home" + keySuffix}>Home</td>
                                        <td 
                                            className="team-name num-col" 
                                            key={"home-rating-" + keySuffix}>{entry.elo_before_home}
                                        </td>
                                        <td 
                                            className={"team-name num-col" + (homeFavored ? " fira-code-bold" : "")}
                                            key={"home-projection-" + keySuffix}>{roundProjection(entry.expected_win_home)}
                                        </td>
                                    </tr>
                                </Fragment>
                            )
                        })
                    }
                    </tbody>
                    </table>
                    </Fragment>
                )
            })
        }
    </section>
)
