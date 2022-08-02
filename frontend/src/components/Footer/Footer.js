import { Link } from "react-router-dom";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

import { URL_CONSTANTS } from "@components/Constants/constants";

import "./Footer.css";

const Footer = () => {
    const links = [
        {
            Product: [
                {
                    'title': 'Organizations',
                    'link': '/organizations',
                    'external': false
                },
                {
                    'title': 'Jobs',
                    'link': '/jobs',
                    'external': false
                },
                {
                    'title': 'Teams',
                    'link': '/teams',
                    'external': false
                },
                {
                    'title': 'Task Automation',
                    'link': '/task-automation',
                    'external': false
                },
                {
                    'title': 'Pricing',
                    'link': '/pricing',
                    'external': false
                },
            ]
        },
        {
            Resources: [
                {
                    'title': 'Community',
                    'link': '/community',
                    'external': false
                },
                {
                    'title': 'Brand Assets',
                    'link': '/brand',
                    'external': false
                },
                {
                    'title': 'Integrations',
                    'link': '/integrations',
                    'external': false
                },
                {
                    'title': 'System Status',
                    'link': '/system-status',
                    'external': false
                },
                {
                    'title': 'Support',
                    'link': '/support',
                    'external': false
                },
            ]
        },
        {
            Developers: [
                {
                    'title': 'Documentation',
                    'link': '/docs',
                    'external': false
                },
                {
                    'title': 'API Reference',
                    'link': '/docs/api',
                    'external': false
                },
                {
                    'title': 'Guides',
                    'link': '/guides',
                    'external': false
                },
                {
                    'title': 'Pre-Built Plugins',
                    'link': '/plugins',
                    'external': false
                },
            ]
        },
        {
            Company: [
                {
                    'title': 'Open Source',
                    'link': URL_CONSTANTS.github,
                    'external': true
                },
                {
                    'title': 'Terms of Service',
                    'link': '/terms-of-service',
                    'external': false
                },
                {
                    'title': 'Privacy Policy',
                    'link': '/privacy-policy',
                    'external': false
                },
            ]
        }
    ]

    return (
        <div className="footer">
            <div className="grid">
                <div className="footer-icons">
                    <div>
                        <Link className="footer-link" to="/">
                            <div className="text-with-icon">
                                <div className="img-container">
                                    <img id="footer-badge" src="/badge.svg" alt="Runner badge" />
                                </div>
                                <h3>runner</h3>
                            </div>
                        </Link>

                        <div className="footer-icons-social">
                            <a className="footer-link" target="_blank" rel="noreferrer" href={URL_CONSTANTS.twitter}>
                                <div className="img-container">
                                    <FontAwesomeIcon icon={["fa-brands", "fa-twitter"]} />
                                </div>
                            </a>

                            <a className="footer-link" target="_blank" rel="noreferrer" href={URL_CONSTANTS.discord}>
                                <div className="img-container">
                                    <FontAwesomeIcon icon={["fa-brands", "fa-discord"]} />
                                </div>
                            </a>

                            <a className="footer-link" target="_blank" rel="noreferrer" href={URL_CONSTANTS.github}>
                                <div className="img-container">
                                    <FontAwesomeIcon icon={["fa-brands", "fa-github"]} />
                                </div>
                            </a>
                        </div>
                    </div>
                </div>

                {links.map((category, index) => (
                    <div className="footer-items" key={`${Object.keys(category)}`} style={{gridArea: `item-${index}`}}>
                        <ul>
                            <li>
                                <h4>{Object.keys(category)}</h4>
                            </li>
                            {Object.values(category)[0].map((item, idx) => (
                                <li key={`${item.title}-${idx}`}>
                                    {item.external ? 
                                        <a href={item.link} className="footer-link" target='_blank' rel='noreferrer'>
                                            <p>{item.title}</p>
                                        </a>
                                        :
                                        <Link className="footer-link" to={item.link}>
                                            <p>{item.title}</p>
                                        </Link>
                                    }
                                </li>
                            ))}
                        </ul>
                    </div>
                ))}
            </div>

            <div className="footer-appendage">
                <p>©️ Runner Inc</p>
            </div>
        </div>
    )
}

export default Footer;