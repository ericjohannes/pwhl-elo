import "./App.css"
import {convertAndCapitalize, pubDateString} from "./utils"
import {projectionTable} from "./projectionTable"
import {eloHistoryChart} from "./eloHistoryChart"
import {ratingTable} from "./eloRatingTable"

function App() {

  return (
    <>
      {ratingTable()}
      {projectionTable()}
      {eloHistoryChart()}

      <p className="quattrocento-regular">See the <a href="https://github.com/ericjohannes/pwhl-elo">code for this project</a>.</p>
      <p className="quattrocento-regular">Created with 🧮 by <a href="https://ericjblom.com/">Eric Blom</a>.</p>
    </>
  )
}

export default App
