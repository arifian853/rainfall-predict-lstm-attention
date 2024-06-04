import { Route, Routes } from "react-router-dom"
import { Home } from "./pages/Home"
import './App.css'
import { Prediction } from "./pages/Prediction"

function App() {

  return (
    <>
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/predict-lstm' element={<Prediction />} />
      </Routes>
    </>
  )
}

export default App
