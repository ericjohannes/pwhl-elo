import "./App.css"
import pwhl_final_elos from "./assets/pwhl_latest_elos.json"
import {convertAndCapitalize, pubDateString} from "./utils"
import {projectionTable} from "./projectionTable"
import {eloHistoryChart} from "./eloHistoryChart"

const compareFn = (a, b) =>{
  if (a[1] > b[1]) {
    return -1;
  } else if (a[1] < b[1]) {
    return 1;
  }
  // a must be equal to b
  return 0;
}

function App() {

  return (
    <>
      <h1 className="oswald-bold">PWHL Team Elo Ratings</h1>
      <h3 className="updated-at quattrocento-regular">Last updated {pubDateString(pwhl_final_elos.date)}</h3>
      <table className="rating-table">
        <thead className="fira-code-bold">
          <tr>
            <th className="team-name table-head-cell">Team</th>
            <th className="num-col table-head-cell">Rating</th>
          </tr>
        </thead>
        <tbody className="fira-code-regular">
          {
            Object.entries(pwhl_final_elos.teams).sort(compareFn).map((entry, i)=>{
              return(
                <tr className="data-row" key={"data-row-" + i}>
                  <td 
                    className="team-name table-left-cell fira-code-regular"
                    key={"team-name-" + i}>{convertAndCapitalize(entry[0])}
                    </td>
                  <td className="num-col fira-code-regular" key={"team-score-" + i}>{entry[1]}</td>
                </tr>
              )
            })
          }
        </tbody>
      </table>
      {projectionTable()}
      {eloHistoryChart()}

      <p className="quattrocento-regular">See the <a href="https://github.com/ericjohannes/pwhl-elo">code for this project</a>.</p>
      <p className="quattrocento-regular">Created with 🧮 by <a href="https://ericjblom.com/">Eric Blom</a>.</p>
    </>
  )
}

export default App
