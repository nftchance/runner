import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

import Page from "@components/Page/Page";
import ProposalCard from "@components/Cards/ProposalCard";
import PrimaryButton from "@components/Buttons/PrimaryButton";

import { PROPOSAL_DATA } from "@components/Constants/copy";
import "./Governance.css"

// NOTE: For these cards, I'm going to try a different styling method
//      We're going to have a fixed width and height and use a flex box 
//      to emulate a responsive grid with a lot less css.
//      Need to have description text wrap with an ellipsis if too long
// The code for that is simply:
// .governance-proposals {
//     display: flex;
//     flex-flow: row wrap;
//     gap: 20px;
//     justify-content: center;
// } with the proposal card width at a fixed pixel amount
// However, the extra room just looks fucky, and when justifying to the center, the tabs look fucky.
// Probably just going to have to go with grid, but need to figure out how to keep the cards from being
// different heights with their varying length descriptions.

const Governance = () => {
    let navigate = useNavigate();

    const [ filterTab, setFilterTab ] = useState("In Progress");
    // Using placeholder data before API integration
    const [ proposalData, setProposalData ] = useState(PROPOSAL_DATA);
    const [ sorting, setSorting ] = useState('created_at');

    // These are just placeholder, not sure what sort methods we want to provide or what the field will actually be.
    const sortingMethods = {
        'Newest': 'created_at',
        'Oldest': '-created_at',
        'Most Support': 'votes',
        'Least Support': '-votes'
    }

    const handleFilterTabChange = (tab) => {
        setFilterTab(tab);
        
        // TODO: API get current proposals with selected filter
        setProposalData(PROPOSAL_DATA)
    }

    const handleSortChange = (sort) => {
        setSorting(sortingMethods[sort])
    }

    return (
        <Page>
            <div className="headline">
                <h1>Play an active role in determining the <br />future of runner.</h1>
                <h5 className="subtitle">
                    Runner is an open source and community led service business automation tool. 
                    Modernize your business with automation, asynchronous task completion, 
                    customer onboarding forms and more.
                </h5>
                <PrimaryButton
                    text="Submit a proposal"
                    onClick={() => navigate("/proposals")}
                />
            </div>
            <div className="governance">
                <div className="governance-tabs">
                    <div className="filter-tabs">
                        <div className="filter-tab">
                            <button 
                                className={filterTab === "Pending" ? "active" : ""}                                        
                                onClick={() => handleFilterTabChange("Pending")}
                            >
                                <p>Pending</p>
                            </button>
                        </div>
                        <div className="filter-tab">
                            <button 
                                className={filterTab === "In Progress" ? "active" : ""}                                        
                                onClick={() => handleFilterTabChange("In Progress")}
                            >
                                <p>In Progress</p>
                            </button>
                        </div>
                        <div className="filter-tab">
                            <button 
                                className={filterTab === "Concluded" ? "active" : ""}                                        
                                onClick={() => handleFilterTabChange("Concluded")}
                            >
                                <p>Concluded</p>
                            </button>
                        </div>
                    </div>
                    <div className="gap-tab" />
                    <div className="sort-tabs">
                        <div className="sort-tab">
                            <p>Sort By</p>
                            <FontAwesomeIcon
                                className="expand-icon" 
                                icon={["fal", "angle-down"]}
                            />
                        </div>
                    </div>
                </div>

                <div className="governance-proposals">
                    {proposalData.map((proposal, index) => (
                        <ProposalCard
                            key={`proposal-${index}`}
                            title={proposal.title}
                            description={proposal.description}
                            tags={proposal.tags}
                            votingPercents={proposal.votingPercents}
                            buttonText="View proposal"
                            buttonOnClick={() => navigate(proposal.linkTo)}
                        />
                    ))}
                </div>
            </div>
        </Page>
    )
}

export default Governance;