import { useNavigate } from "react-router-dom";
import { HelmetProvider, Helmet } from "react-helmet-async";

import Page from "@components/Page/Page";
import PrimaryButton from "@components/Buttons/PrimaryButton";
import SecondaryButton from "@components/Buttons/SecondaryButton";
import TaskCard from "@components/Cards/TaskCard";
import RoadmapIndicator from "@images/roadmap-indicator.svg"

import { ROADMAP_TASKS } from "@components/Constants/copy";
import { URL_CONSTANTS, SEO_CONSTANTS } from "@components/Constants/constants";

import "./Roadmap.css";

const Roadmap = () => {
    let navigate = useNavigate();

    return (
        <>
            <HelmetProvider>
                <Helmet>
                    <title>{SEO_CONSTANTS.roadmap.title}</title>
                    <meta name="og:title" content={SEO_CONSTANTS.roadmap.title} />
                    <meta name="og:description" content={SEO_CONSTANTS.roadmap.title} />

                    <meta name="description" content={SEO_CONSTANTS.roadmap.description} />
                    <meta name="og:description" content={SEO_CONSTANTS.roadmap.description} />
                    <meta name="twitter:description" content={SEO_CONSTANTS.roadmap.description} />

                    <meta property="og:url" content={`${window.location.href}`} />
                </Helmet>
            </HelmetProvider>

            <Page>
                <div className="headline">
                    <h1 data-testid="headline-title">
                        Join us in the run towards a better future <br />of service business management.
                    </h1>
                    <h5 className="subtitle">
                        Runner is an open source and community led service business automation tool. 
                        Modernize your business with automation, asynchronous task completion, 
                        customer onboarding forms and more.
                    </h5>
                    <SecondaryButton
                        text={"View on Github"}
                        onClick={() => window.open(URL_CONSTANTS.github, "_blank", "noreferrer")}
                    />
                </div>
                <div className="roadmap">
                    <div className="roadmap-indicator">
                        <img src={RoadmapIndicator} alt="Roadmap Indicator" />
                    </div>
                    {ROADMAP_TASKS.map((version) => (
                        <div className="roadmap-version" key={version.version}>
                            <h3 className="version-subtitle">
                                {version.version}
                            </h3>
                            <h6 className="version-subtext">
                                {version.description}
                            </h6>
                            <div className="roadmap-tasks">
                                {version.tasks.map((task, index) => (
                                    <TaskCard 
                                        key={`${task.title}-${index}`}
                                        title={task.title}
                                        description={task.description}
                                        status={task.status}
                                        statusIndicatorColor={task.statusIndicatorColor}
                                        buttonText="View task"
                                        buttonOnClick={() => navigate(task.linkTo)}
                                    />
                                ))}
                            </div>
                        </div>
                    ))}

                    <div className="future">
                        <h3 className="version-subtitle">
                            Future
                        </h3>
                        <h6 className="version-subtext">
                            This is the end of the publicly available roadmap. You can 
                            see the state of active proposals by visiting the Governance 
                            section to vote on the direction of upcoming developments.
                        </h6>
                        <PrimaryButton
                            text={"View Governance Portal"}
                            onClick={() => navigate("/governance")}
                        />
                    </div>
                </div>
            </Page>
        </>
    )
}

export default Roadmap;