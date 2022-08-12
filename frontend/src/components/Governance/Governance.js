import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { HelmetProvider, Helmet } from "react-helmet-async";

import Page from "@components/Page/Page";
import ProposalCard from "@components/Cards/ProposalCard";
import PrimaryButton from "@components/Buttons/PrimaryButton";
import CustomSelect from "@components/Select/CustomSelect";

import { PROPOSAL_DATA } from "@components/Constants/copy";
import { SEO_CONSTANTS } from "@components/Constants/constants";
import "./Governance.css"

const Governance = () => {
    let navigate = useNavigate();

    const [ filtering, setFiltering ] = useState("In Progress");
    const [ sorting, setSorting ] = useState("");
    const [ proposalData, setProposalData ] = useState();

    // These are just placeholder, not sure what sort methods we want to provide or what the field will actually be.
    const sortingMethods = [
        {
            title: 'Oldest',
            method: '-created_at',
        },
        {
            title: 'Newest',
            method: 'created_at',
        },
        {
            title: 'Least Time Remaining',
            method: '-votes',
        },
        {
            title: 'Most Time Remaining',
            method: 'votes',
        },
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

    useEffect(() => {
        // TODO: fetch from backend
        setProposalData(PROPOSAL_DATA);
        console.log(sorting, filtering)
    }, [sorting, filtering])

    return (
        <>
            <HelmetProvider>
                <Helmet>
                    <title>{SEO_CONSTANTS.governance?.title}</title>
                    <meta name="og:title" content={SEO_CONSTANTS.governance?.title} />

                    <meta name="description" content={SEO_CONSTANTS.governance?.description} />
                    <meta name="og:description" content={SEO_CONSTANTS.governance?.description} />

                    <meta property="og:url" content={`${window.location.href}`} />
                </Helmet>
            </HelmetProvider>
        
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
                                        className={filtering === method.title ? "active" : ""}                                        
                                        onClick={() => setFiltering(method.title)}
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
                                    onChange={(event) => setSorting(event.target.value)}
                                />
                            </div>
                        </div>
                    </div>

                    <div className="governance-proposals">
                        {proposalData?.map((proposal, index) => (
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
        </>
    )
}

export default Governance;