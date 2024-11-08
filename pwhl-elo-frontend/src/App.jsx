// import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import './App.css'
import pwhl_final_elos from './assets/pwhl_final_elos.json'


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
  console.log(pwhl_final_elos)
  console.log(compareFn)
  console.log(Object.entries(pwhl_final_elos).sort(compareFn))
  return (
    <>
      {/* <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div> */}
      <h1>PWHL Team Elo Ratings</h1>
      <table>
        <thead>
          <tr>
            <th>Team</th>
            <th>Rating</th>
          </tr>
        </thead>
        <tbody>
          {
            // Object.entries(pwhl_final_elos).map(x=>console.log(x))
            Object.entries(pwhl_final_elos).sort(compareFn).map((entry, i)=>{
              return(
                <tr>
                  <td>{entry[0]}</td>
                  <td>{entry[1]}</td>

                </tr>
              )
            })
          }
        </tbody>
      </table>
    </>
  )
}

export default App
