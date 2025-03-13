import "./App.css"
import {projectionTable} from "./projectionTable"
import {eloHistoryChart} from "./eloHistoryChart"
import {eloRatingTable} from "./eloRatingTable"

function App() {

  return (
    <>
      {eloRatingTable()}
      {projectionTable()}
      {eloHistoryChart()}

      <p className="quattrocento-regular">See the <a href="https://github.com/ericjohannes/pwhl-elo">code for this project</a>.</p>
      <p className="quattrocento-regular">Created with 🧮 by <a href="https://ericjblom.com/">Eric Blom</a>.</p>
    </>
  )
}

export default App
