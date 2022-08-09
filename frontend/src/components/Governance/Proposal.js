// import { useParams } from "react-router-dom";

import Page from "@components/Page/Page";
import AccordionPanel from "@components/Accordion/AccordionPanel";

import "./Proposal.css";

const Proposal = () => {
    // TODO: Fetch proposal info
    // const params = useParams();

    const proposalData = {
        title: '[RP1] Mobile-First Front-End Design',
        description: "With the majority of services being render in-field, the user-experience is key to securing the highest level of impact from the utilization of better tools.",
        detail: "TL/DR: To get Lil Nouns a wardrobe across all metaverse and social platforms.\n\nTo be able to Lil Nounify yourself in every medium should be our number one goal. While the below plan does involve some rarity in its distribution mechanics, the main goal is to have as many Lil Noun “wearables”; whether in Metaverse, Office meeting settings?, Tik-Tok, Snap Chat, Instagram, etc, etc. I believe this aspect DIRECTLY falls under PROLIFERATION tenant.\n\nHaving FashionVerse Fashion House push out a major Collection like this will essentially blitz all socials over the next 2 Months. It will also allow us to tweak our future plans as we see how this unfolds and who steps up to participate because of this.\n\nI think the value proposition can be summed up in the article below by Zeneca_33\n\nImpossible Expectations\n\nIf you haven’t read this latest piece from Zeneca_33, it discusses a lot about how to manage, or not manage, impossible expectations. This wearable schedule is an attempt to bridge some of this expectations gap held among different participants in the NFT space. AND have some FUN while we are doing it!A little bit of rarity for lower numbers.",
        tags: [
            'Dashboard',
            'UX'
        ], 
        votingPercents: [60, 25],
        status: 'In Progress',
        statusIndicatorColor: 'green',
        quorom: '421k $RUNNER',
        
    }

    return (
        <Page>
            <div className="side-by-side">
                <div className="proposal-details">
                    <div className="proposal-tags">
                        {proposalData.tags.map((tag) => (
                            <div className="tag" key={`tag${tag}`}>
                                <p className="tag-text">{tag}</p>
                            </div>
                        ))}
                    </div>
                    <h1>{ proposalData.title }</h1>
                    <h5>{ proposalData.description }</h5>

                    <div className="proposal-provider">
                        <div className="provider-icon-container">
                            <img src={'/badge.svg'} alt='Runner' />
                        </div>
                        <span className="provider-name">runner</span>
                    </div>
                    
                    <AccordionPanel
                        title={"Details of this proposal"}
                        detail={proposalData.detail}
                        index={0}
                        open={true}
                    />
                </div>
                <div className="voting">

                </div>
            </div>
        </Page>
    )
}

export default Proposal;