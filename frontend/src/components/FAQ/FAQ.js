import { HelmetProvider, Helmet } from "react-helmet-async";

import AccordionPanel from "@components/Accordion/AccordionPanel";
import Page from "@components/Page/Page";

import { FAQ_ITEMS } from "@components/Constants/copy";
import { SEO_CONSTANTS } from "@components/Constants/constants";

import "./FAQ.css";

const FAQ = () => {
    return (
        <>
            <HelmetProvider>
                <Helmet>
                    <title>{SEO_CONSTANTS.faq.title}</title>
                    <meta name="og:title" content={SEO_CONSTANTS.faq.title} />
                    <meta name="og:description" content={SEO_CONSTANTS.faq.title} />

                    <meta name="description" content={SEO_CONSTANTS.faq.description} />
                    <meta name="og:description" content={SEO_CONSTANTS.faq.description} />
                    <meta name="twitter:description" content={SEO_CONSTANTS.faq.description} />

                    <meta property="og:url" content={`${window.location.href}`} />
                </Helmet>
            </HelmetProvider>

            <Page>
                <div className="headline">
                    <h1>Join us in the run towards a better future <br />of service business management.</h1>
                    <h5 className="subtitle">
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
        </>
    )
}

export default FAQ;