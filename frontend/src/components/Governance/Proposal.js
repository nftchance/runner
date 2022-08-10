import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { HelmetProvider, Helmet } from "react-helmet-async";

import Page from "@components/Page/Page";
import AccordionPanel from "@components/Accordion/AccordionPanel";
import PrimaryButton from "@components/Buttons/PrimaryButton";
import MenuButton from "@components/Buttons/MenuButton";

import badge from "@images/badge.png";
import "./Proposal.css";
// import { URL_CONSTANTS } from "@components/Constants/constants";

const Proposal = () => {
    const params = useParams();
    const [ proposalData, setProposalData ] = useState();

    const proposalActions = ["Do Something", "Do Something Else"]
    const proposalIndicatorColors = {
        'Open': 'green',
    }

    const votePercentages = [
        (proposalData?.votes_for / proposalData?.votes_total * 100).toFixed(2),
        (proposalData?.votes_against / proposalData?.votes_total * 100).toFixed(2),
        (proposalData?.votes_abstain / proposalData?.votes_total * 100).toFixed(2)
    ]


    useEffect(() => {
        // TODO: fetch from API
        // const url = `${URL_CONSTANTS.api}/proposal/${params.id}`
        // const request = new Request(url, {
        //     method: 'GET',
        //     cache: 'default'
        // })
        // fetch(request)
        //     .then((response) => response.json())
        //     .then((response) => {
        //         // setProposalData(response)
        //     })
        //     .catch((error) => {
        //         console.log('Error getting proposal data', error)
        //     })
        
        
        // Using dummy data prior to merging backend and frontend, 
        // also applying a delay to see how the component renders without data.
        setTimeout(() => {
            setProposalData(
                {
                    "id": 1,
                    "status": "Open",
                    "votes_for": 39,
                    "votes_against": 59,
                    "votes_abstain": 3,
                    "votes_total": 500,
                    "approved": false,
                    "title": "My First Proposal",
                    "description": "This is my first proposal. I hope you like it.\r\n\r\nPS: Postgres kicked my ass tonight",
                    "closed_at": "2022-09-09T06:40:28.645222Z",
                    "created_at": "2022-08-10T06:40:28.646132Z",
                    "updated_at": "2022-08-10T06:40:28.646160Z",
                    "proposed_by": 1,
                    "votes": []
                }
            )
        }, 2000)
    }, [params])

    const handleMenuAction = (action) => {
        console.log('Menu Action: ', action)
    }

    const handleVote = () => {
        return
    }

    return (
        <>
            <HelmetProvider>
                <Helmet>
                    <title>{`runner | [RP${params.id}] ${proposalData?.title ? proposalData.title : ''}`}</title>
                    <meta name="og:title" content={`runner | [RP${params.id}]`} />
                    <meta name="og:description" content={`runner | [RP${params.id}]`} />

                    {/* TODO: Figure out if the description is general or the summary proposal
                    
                    <meta name="description" content={SEO_CONSTANTS.roadmap.description} />
                    <meta name="og:description" content={SEO_CONSTANTS.roadmap.description} />
                    <meta name="twitter:description" content={SEO_CONSTANTS.roadmap.description} /> 
                    */}

                    <meta property="og:url" content={`${window.location.href}`} />
                </Helmet>
            </HelmetProvider>

            <Page>
                <div className="proposal-grid">
                    <div className="proposal-details">
                        <div className="proposal-tags">
                            {proposalData?.tags?.map((tag) => (
                                <div className="tag" key={`tag${tag}`}>
                                    <p className="tag-text">{tag}</p>
                                </div>
                            ))}
                        </div>
                        <div className="proposal-title">
                            <h1>{`[RP${params.id}] ${proposalData?.title}`}</h1>
                            <div className="proposal-menu-btn">
                                <MenuButton
                                    icon={["fal", "fa-ellipsis"]}
                                    menuItems={proposalActions}
                                    handleMenu={handleMenuAction}
                                />
                            </div>
                        </div>
                        <h5>{ proposalData?.summary }</h5>

                        <div className="proposal-provider">
                            <div 
                                className="provider-icon-container"
                                style={{backgroundImage: `url(${badge})`}}
                            />
                            <span className="provider-name">runner</span>
                        </div>
                        
                        <AccordionPanel
                            title={"Details of this proposal"}
                            detail={proposalData?.description}
                            index={0}
                            open={true}
                        />
                    </div>
                    <div className="voting">
                        <div className="voting-info">
                            <h4>Information</h4>

                            <div className="voting-detail">
                                <p>Status</p>
                                <div className="voting-detail-info">
                                    <div 
                                        className={`status-indicator ${proposalIndicatorColors[proposalData?.status]}`}
                                    />
                                    <p>{proposalData?.status}</p>
                                </div>
                            </div>
                            
                            {/* <div className="voting-detail">
                                <p>Quorom</p>
                                <div className="voting-detail-info">
                                    <p>{proposalData?.quorom}</p>
                                </div>
                            </div> */}

                            <div className="voting-detail">
                                <p>Start Date</p>
                                <div className="voting-detail-info">
                                    <p>{proposalData?.created_at}</p>
                                </div>
                            </div>

                            <div className="voting-detail">
                                <p>End Date</p>
                                <div className="voting-detail-info">
                                    <p>{proposalData?.closed_at}</p>
                                </div>
                            </div>

                            <div className="voting-detail">
                                <p>Voting System</p>
                                <div className="voting-detail-info">
                                    <p>Basic Voting</p>
                                </div>
                            </div>
                        </div>

                        <div className="voting-results">
                            <h4>Current Results</h4>

                            <div className="voting-bar-header">
                                <p>For</p>
                                <p className="voting-percentage">
                                    {votePercentages[0]}%
                                </p>
                            </div>
                            <div className="voting-bar">
                                <div 
                                    className={`voting-progress ${proposalData?.votes_for === 0 ? 'hidden' : ''}`} 
                                    style={{width: `${votePercentages[0]}%`}} 
                                />
                                <div className="voting-progress-remaining" />
                            </div>

                            <div className="voting-bar-header">
                                <p>Against</p>
                                <p className="voting-percentage">
                                    {votePercentages[1]}%
                                </p>
                            </div>
                            <div className="voting-bar">
                                <div 
                                    className={`voting-progress ${proposalData?.votes_against === 0 ? 'hidden' : ''}`} 
                                    style={{width: `${votePercentages[1]}%`}} 
                                />
                                <div className="voting-progress-remaining" />
                            </div>

                            <div className="voting-bar-header">
                                <p>Abstain</p>
                                <p className="voting-percentage">
                                    {votePercentages[2]}%
                                </p>
                            </div>
                            <div className="voting-bar">
                                <div 
                                    className={`voting-progress ${proposalData?.votes_abstain === 0 ? 'hidden' : ''}`} 
                                    style={{width: `${votePercentages[2]}%`}}
                                />
                                <div className="voting-progress-remaining" />
                            </div>
                        </div>
                        <div className="voting-action">
                            <div className="voting-buttons">
                                <PrimaryButton
                                    text="Submit Vote"
                                    onClick={handleVote}
                                    style={{width: '105px'}}
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </Page>
        </>
    )
}

export default Proposal;