import { useNavigate } from "react-router-dom";

import Page from "../Page/Page";
import PrimaryButton from "../Buttons/PrimaryButton";
import SecondaryButton from "../Buttons/SecondaryButton";
import TaskCard from "../Cards/TaskCard";

import { URL_CONSTANTS, ROADMAP_TASKS } from "../Constants/constants";
import "./Roadmap.css";

const Roadmap = () => {
    let navigate = useNavigate();

    return (
        <Page>
            <div className="roadmap">
                <div className="roadmap-headline">
                    <h1>Join us in the run towards a better future</h1>
                    <h5>
                        Runner is an open source and community led service business automation tool. 
                        Modernize your business with automation, asynchronous task completion, 
                        customer onboarding forms and more.
                    </h5>
                    <SecondaryButton
                        text={'View on Github'}
                        onClick={() => window.open(URL_CONSTANTS.github, '_blank', 'noreferrer')}
                    />
                    <PrimaryButton
                        text={'View Governance Portal'}
                        onClick={() => navigate('/governance')}
                    />

                    {ROADMAP_TASKS.map((task) => (
                        <TaskCard 
                            key={task.title}
                            title={task.title}
                            status={task.status}
                            statusIndicatorColor={task.statusIndicatorColor}
                            buttonText='View task'
                            buttonOnClick={task.linkTo}
                        />
                    ))}
                </div>
            </div>
        </Page>
    )
}

export default Roadmap;