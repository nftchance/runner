import AccordionPanel from "../Accordion/AccordionPanel";
import Page from "../Page/Page";

import { FAQ_ITEMS } from "../Constants/constants";
import "./FAQ.css";

const FAQ = () => {
    return (
        <Page>
            <div className="faq-headline">
                <h1>Join us in the run towards a better future</h1>
                <h5>
                    Runner is an open source and community led service business automation tool. 
                    Modernize your business with automation, asynchronous task completion, 
                    customer onboarding forms and more.
                </h5>
            </div>
            <div className="faq-accordion">
                {FAQ_ITEMS.map((item, index) => (
                    <AccordionPanel
                        key={`panel-${index}`}
                        title={item.question}
                        detail={item.answer}
                        index={index}
                    />
                ))}
            </div>
        </Page>
    )
}

export default FAQ;