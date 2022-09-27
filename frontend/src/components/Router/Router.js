import { BrowserRouter, Route, Routes } from "react-router-dom";

import loadable from "@loadable/component";

import Loading from "@components/Loading/Loading";

const LoadableHome = loadable(() => import("@components/Home/Home"), { fallback: <Loading /> })
const LoadableRoadmap = loadable(() => import("@components/Roadmap/Roadmap"), { fallback: <Loading /> })
const LoadableGovernance = loadable(() => import("@components/Governance/Governance"), { fallback: <Loading /> })
const LoadableFAQ = loadable(() => import("@components/FAQ/FAQ"), { fallback: <Loading /> })
const LoadableProposal = loadable(() => import("@components/Governance/Proposal"), {fallback: <Loading />})

const Router = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route exact path="/" element={<LoadableHome />} />
                <Route path="/roadmap" element={<LoadableRoadmap />} />
                <Route path="/governance" element={<LoadableGovernance />} />
                <Route path="/faq" element={<LoadableFAQ />} />
                <Route path="/proposal/:id" element={<LoadableProposal />} />
            </Routes>
        </BrowserRouter>
    )
}

export default Router;