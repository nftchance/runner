import { BrowserRouter, Route, Routes } from "react-router-dom"

import Home from "../Home/Home"
import Roadmap from "../Roadmap/Roadmap"
import FAQ from "../FAQ/FAQ"

const Router = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route exact path="/" element={<Home />} />
                <Route path="/roadmap" element={<Roadmap />} />
                <Route path="/faq" element={<FAQ />} />
            </Routes>
        </BrowserRouter>
    )
}

export default Router;