import { useState } from "react";
import { Link } from "react-router-dom";

import Page from "../Page/Page";
import PrimaryButton from "../Buttons/PrimaryButton";
import SecondaryButton from "../Buttons/SecondaryButton";
import TextFieldInline from "../TextFields/TextFieldInline";
import ModuleCard from "../Cards/ModuleCard";
import GhostCard from "../Cards/GhostCard";

import { LANDING_CATEGORIES, LANDING_MODULES } from "@components/Constants/constants";
import "./Home.css";

const Home = () => {
    const [ joinWaitlistMsg, setJoinWaitlistMsg ] = useState('Join Waitlist')

    const handleJoinWaitlist = () => {
        // validate email? or handle on backend
        var valid = true;
        if (!valid) 
            setJoinWaitlistMsg('Invalid Email!');
        else
            setJoinWaitlistMsg('✔️ Joined')
    }

    return (
        <Page>
            <div className="home">
                <div className="hero">
                    <div className="hero-text">
                        <h1>Revolutionize your service business with</h1>
                        <h1 className="yellow"> automation tools of 2032.</h1>
                        <div className="shadow-text">No we're not time travelers.</div>

                        <h5 className="subtitle">
                            Runner is an open source and community led service business automation tool. 
                            Modernize your business with automation, asynchronous task completion, 
                            customer onboarding forms and more.
                        </h5>

                        <div className='email-signup'>
                            <TextFieldInline
                                placeholder='Email address...'
                            />
                            <PrimaryButton
                                text={joinWaitlistMsg}
                                onClick={handleJoinWaitlist}
                            />
                        </div>
                    </div>
                </div>
                <img id="hero-img" src="/hero.svg" alt="Hero" />

                <div className="categories">
                    <h3>Modernize your business operations and services</h3>
                    <div className="categories-grid">
                        {LANDING_CATEGORIES.map((category, index) => (
                            <div key={`${category.title}`} style={{gridArea: `item-${index}`}}>
                                <GhostCard
                                    title={category.title}
                                    description={category.description}
                                    icon={category.icon}
                                    buttonText={'Learn more'}
                                    buttonRedirect={category.link}
                                />
                            </div>
                        ))}
                    </div>

                </div>

                <div className="modules-headline">
                    <h3>What is unlocked with runner?</h3>
                    <h5 className="modules-desc">
                        Driven by an ethos of optimizing the time-consuming and 
                        high-impacts of your service business unlocks entirely new models.
                    </h5>

                    <div className="modules-btn">
                        <Link className="link-wrapper" to="/features">
                            <SecondaryButton
                                text='View all features'
                            />
                        </Link>
                    </div>
                </div>

                <div className="modules">
                    <div className="modules-grid">
                        {LANDING_MODULES.map((mod, index) => (
                            <div key={`${mod.title}`}>
                                <ModuleCard
                                    title={mod.title}
                                    description={mod.description}
                                    provider={mod.provider}
                                    providerLogo={mod.providerLogo}
                                    primaryBtnText='Enable'
                                    // primaryBtnOnClick={}
                                    secondaryBtnText='Launch demo'
                                    // secondaryBtnOnClick={}
                                />
                            </div>
                        ))}
                    </div>
                </div>

                <div className="dashboard">
                    <h3>Run your business without leaving the dashboard</h3>

                </div>

                {/* DELETE THIS */}
                <div style={{marginTop: '300px'}} />

                <div className="governance">
                    <h3>Volume driven platform governance and influence</h3>
                    <h6>
                        Runner turbocharges the best service business to reach new and incredible heights. 
                        In tandem with this, the businesses running the largest amounts of volume have the 
                        largest say and impact in the platforms future.
                    </h6>
                    <p className="formula">
                        {'$RUNNER Earned / Job = ($ Volume <= 21750) ** 1.25 / 100000'}
                    </p>

                    <Link className="link-wrapper" to="/governance">
                        <PrimaryButton
                            text='View Governance Portal'
                        />
                    </Link>
                    <Link className="link-wrapper" to="/governance">
                        <SecondaryButton
                            text='Learn More'
                        />
                    </Link>

                    <img id="volume-img" src="/volume.svg" alt="Volume graph" />
                </div>

                {/* DELETE THIS */}
                <div style={{marginTop: '300px'}} />

                <div className="cta">
                    <h1>Prevent your business from withering.</h1>
                    <br />
                    <h1 className="yellow">Modernize it now.</h1>

                    <div className='email-signup'>
                        <TextFieldInline
                            placeholder={'Email address...'}
                        />
                        <PrimaryButton
                            text={joinWaitlistMsg}
                            onClick={handleJoinWaitlist}
                        />
                    </div>
                </div>
            </div>
        </Page>
    )
}

export default Home;