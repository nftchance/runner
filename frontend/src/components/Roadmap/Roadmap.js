import { useNavigate } from "react-router-dom";

import Page from "@components/Page/Page";
import PrimaryButton from "@components/Buttons/PrimaryButton";
import SecondaryButton from "@components/Buttons/SecondaryButton";
import TaskCard from "@components/Cards/TaskCard";

import { URL_CONSTANTS, ROADMAP_TASKS } from "@components/Constants/constants";
import RoadmapIndicator from "@images/roadmap-indicator.svg"
import "./Roadmap.css";

const Roadmap = () => {
    let navigate = useNavigate();

    return (
        <Page>
            <div className="roadmap-headline">
                <h1>Join us in the run towards a better future <br />of service business management.</h1>
                <h5>
                    Runner is an open source and community led service business automation tool. 
                    Modernize your business with automation, asynchronous task completion, 
                    customer onboarding forms and more.
                </h5>
                <SecondaryButton
                    text={'View on Github'}
                    onClick={() => window.open(URL_CONSTANTS.github, '_blank', 'noreferrer')}
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
                                    buttonText='View task'
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
                        text={'View Governance Portal'}
                        onClick={() => navigate('/governance')}
                    />
                </div>
            </div>
        </Page>
    )
}

export default Roadmap;