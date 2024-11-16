import "./App.css"
import pwhl_final_elos from "./assets/pwhl_latest_elos.json"


const compareFn = (a, b) =>{
  if (a[1] > b[1]) {
    return -1;
  } else if (a[1] < b[1]) {
    return 1;
  }
  // a must be equal to b
  return 0;
}

const pubDateString = (datetime) =>{
  const pubDate =  new Date(datetime)
  console.log('datetime')
  console.log(datetime)
  console.log(pubDate)
  const months = ['Jan.','Feb.','Mar.','April','May','June','July','Aug.','Sept.','Oct.','Nov.','Dec.'];
  const year = pubDate.getFullYear();
  const month = months[pubDate.getMonth()];
  const date = pubDate.getDate();
  return month + ' ' + date + ' ' + year;
}
function convertAndCapitalize(str) {
  // Replace underscores with spaces and split the string into words
  return str
    .replace(/_/g, ' ')
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()) // Capitalize each word
    .join(' '); // Join the words back together with spaces
}

function App() {

  return (
    <>
      <h1 className="oswald-bold">PWHL Team Elo Ratings</h1>
      <p className="updated-at quattrocento-regular">Last updated at {pubDateString(pwhl_final_elos.date)}</p>
      <table className="rating-table">
        <thead className="quattrocento-bold">
          <tr>
            <th className="team-name table-head-cell">Team</th>
            <th className="team-rating table-head-cell">Rating</th>
          </tr>
        </thead>
        <tbody className="quattrocento-regular">
          {
            Object.entries(pwhl_final_elos.teams).sort(compareFn).map((entry, i)=>{
              return(
                <tr className="data-row" key={"data-row-" + i}>
                  <td className="team-name table-left-cell" key={"team-name-" + i}>{convertAndCapitalize(entry[0])}</td>
                  <td className="team-rating" key={"team-score-" + i}>{entry[1]}</td>

                </tr>
              )
            })
          }
        </tbody>
      </table>
      <p className="quattrocento-regular">Created with 🧮 by <a href="https://ericjblom.com/">Eric Blom</a></p>
    </>
  )
}

export default App
