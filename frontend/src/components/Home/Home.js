import { useState } from "react";
import { useNavigate } from "react-router-dom";

import Page from "@components/Page/Page";
import PrimaryButton from "@components/Buttons/PrimaryButton";
import SecondaryButton from "@components/Buttons/SecondaryButton";
import TextFieldInline from "@components/TextFields/TextFieldInline";
import ModuleCard from "@components/Cards/ModuleCard";
import GhostCard from "@components/Cards/GhostCard";
import VolumeGraph from "@components/StyledAssets/VolumeGraph";

import hero from "@images/landing/hero.svg";
// import volume from "@images/landing/volume.svg";
import dashboard from "@images/landing/dashboard.svg";

import { 
    LANDING_CATEGORIES, LANDING_MODULES, LANDING_DASHBOARD_TABS 
} from "@components/Constants/copy";

import "./Home.css";

const Home = () => {
    let navigate = useNavigate();

    const [ emailField, setEmailField ] = useState("")
    const [ joinWaitlistMsg, setJoinWaitlistMsg ] = useState("Join Waitlist");
    const [ dashboardTab, setDashboardTab ] = useState("Maintenance");

    function isValidEmail(email) {
        return /\S+@\S+\.\S+/.test(email);
    }

    const handleJoinWaitlist = () => {
        if (!isValidEmail(emailField))
            setJoinWaitlistMsg("Invalid Email");
        else
            setJoinWaitlistMsg("✓ Joined")
    }

    return (
        <Page>
            <div className="home">
                <div className="hero-text">
                    <h1 data-testid="hero-title">Revolutionize your service business<br /> with</h1>
                    <h1 className="yellow"> automation tools of 2032.</h1>
                    <div className="shadow-text">No we're not time travelers.</div>

                    <h5>
                        Runner is an open source and community led service business automation tool. 
                        Modernize your business with automation, asynchronous task completion, 
                        customer onboarding forms and more.
                    </h5>

                    <div className="email-signup">
                        <TextFieldInline
                            placeholder="Email address..."
                            value={emailField}
                            onChange={(event) => setEmailField(event.target.value)}
                        />
                        <PrimaryButton
                            text={joinWaitlistMsg}
                            onClick={handleJoinWaitlist}
                        />
                    </div>
                </div>
                <img id="hero-img" src={hero} alt="Hero" />

                <div className="categories">
                    <h3>Modernize your business operations and services</h3>
                    <div className="categories-grid">
                        {LANDING_CATEGORIES.map((category, index) => (
                            <div key={`${category.title}`} style={{gridArea: `item-${index}`}}>
                                <GhostCard
                                    title={category.title}
                                    description={category.description}
                                    icon={category.icon}
                                    buttonText={"Learn more"}
                                    buttonOnClick={() => navigate(category.link)}
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
                        <SecondaryButton
                            text="View all features"
                            onClick={() => navigate("/features")}
                        />
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
                                    primaryBtnText="Enable"
                                    primaryBtnOnClick={() => navigate(mod.linkTo)}
                                    secondaryBtnText="Launch demo"
                                    secondaryBtnOnClick={() => navigate(mod.linkTo)}
                                />
                            </div>
                        ))}
                    </div>
                </div>

                <div className="dashboard">
                    <h3 className="dashboard-headline">
                        Run your business without leaving the dashboard
                    </h3>
                    <div className="side-by-side">
                        <img id="dashboard-img" src={dashboard} alt="Dashboard" />

                        <div className="dashboard-info">
                            <div className="dashboard-tabs">
                                <div className="dashboard-tab">
                                    <button 
                                        className={dashboardTab === "Organization" ? "active" : ""}
                                        onClick={() => setDashboardTab("Organization")}
                                    >
                                        <p>Organization</p>
                                    </button>
                                </div>
                                <div className="dashboard-tab">
                                    <button 
                                        className={dashboardTab === "Services" ? "active" : ""}                                        
                                        onClick={() => setDashboardTab("Services")}
                                    >
                                        <p>Services</p>
                                    </button>
                                </div>
                                <div className="dashboard-tab">
                                    <button 
                                        className={dashboardTab === "Maintenance" ? "active" : ""}                                                                            
                                        onClick={() => setDashboardTab("Maintenance")}
                                    >
                                        <p>Maintenance</p>
                                    </button>
                                </div>
                            </div>

                            {LANDING_DASHBOARD_TABS.map((tab) => (
                                <div 
                                    key={tab.tab}
                                    className={dashboardTab === tab.tab ? "tab-info" : "tab-info hidden"}
                                >
                                    <GhostCard
                                        title={tab.title}
                                        description={tab.description}
                                        buttonText={tab.buttonText}
                                        buttonOnClick={() => navigate(tab.linkTo)}
                                        titleStyle={{fontSize: "20px"}}
                                        noIcon={true}
                                    />
                                </div>
                            ))

                            }
                        </div>
                    </div>

                </div>

                <div className="governance">
                    <div className="governance-headline">
                        <h3>Volume driven platform governance and influence</h3>
                        <p className="formula">
                            {"$RUNNER Earned / Job = ($ Volume <= 21750) ** 1.25 / 1000"}
                        </p>
                    </div>

                    <h6>
                        Runner turbocharges the best service business to reach new and incredible heights. 
                        In tandem with this, the businesses running the largest amounts of volume have the 
                        largest say and impact in the platforms future.
                    </h6>
                        
                    <div className="btn-wrapper">
                        <PrimaryButton
                            text="View Governance Portal"
                            onClick={() => navigate("/roadmap")}
                        />
                        <SecondaryButton
                            text="Learn More"
                            onClick={() => navigate("/governance")}
                        />
                    </div>

                    {/* <img id="volume-img" src={volume} alt="Volume graph" /> */}
                    <VolumeGraph />
                </div>

                <div className="cta">
                    <h1>Prevent your business from withering.</h1>
                    <h1 className="yellow">Modernize it now.</h1>

                    <div className="cta-email email-signup">
                        <TextFieldInline
                            placeholder={"Email address..."}
                            value={emailField}
                            onChange={(event) => setEmailField(event.target.value)}
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