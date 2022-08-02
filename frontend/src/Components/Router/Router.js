import { BrowserRouter, Route, Routes } from "react-router-dom"

import Home from "../Home/Home"
import Roadmap from "../Roadmap/Roadmap"

const Router = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route exact path="/" element={<Home />} />
                <Route path="/roadmap" element={<Roadmap />} />
            </Routes>
        </BrowserRouter>
    )
}

export default Router;