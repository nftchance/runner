import { useState } from "react";
import { useNavigate } from "react-router-dom";

import Page from "@components/Page/Page";
import ProposalCard from "@components/Cards/ProposalCard";
import PrimaryButton from "@components/Buttons/PrimaryButton";
import CustomSelect from "@components/Select/CustomSelect";

import { PROPOSAL_DATA } from "@components/Constants/copy";
import "./Governance.css"

const Governance = () => {
    let navigate = useNavigate();

    const [ filterTab, setFilterTab ] = useState("In Progress");
    const [ sorting, setSorting ] = useState('Sort By');
    // Using placeholder data before API integration
    const [ proposalData, setProposalData ] = useState(PROPOSAL_DATA);

    // These are just placeholder, not sure what sort methods we want to provide or what the field will actually be.
    const sortingMethods = [
        {
            title: 'Newest',
            method: 'created_at',
        },
        {
            title: 'Oldest',
            method: '-created_at',
        },
        {
            title: 'Most Support',
            method: 'votes',
        },
        {
            title: 'Least Support',
            method: '-votes',
        }
    ]

    const filterMethods = [
        {
            title: 'Pending'
        },
        {
            title: 'In Progress'
        },
        {
            title: 'Concluded'
        }
    ]

    const handleFilterTabChange = (tab) => {
        setFilterTab(tab);
        
        // TODO: API get current proposals with selected filter
        setProposalData(PROPOSAL_DATA)
    }

    const handleSortChange = (event) => {
        setSorting(event.target.value)
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
                        {filterMethods.map((method) => (
                            <div className="filter-tab" key={method.title}>
                                <button
                                    className={filterTab === method.title ? "active" : ""}                                        
                                    onClick={() => handleFilterTabChange(method.title)}
                                >
                                    <p>{method.title}</p>
                                </button>
                            </div>
                        ))}
                    </div>
                    <div className="gap-tab" />
                    <div className="sort-tabs">
                        <div className="sort-tab">
                            <CustomSelect
                                selected={sorting}
                                placeholder="Sort By"
                                options={sortingMethods}
                                onChange={handleSortChange}
                            />
                        </div>
                        {/* <div className="sort-tab">
                            <p>Sort By</p>
                            <FontAwesomeIcon
                                className="expand-icon" 
                                icon={["fal", "angle-down"]}
                            />
                        </div> */}
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