import { Link } from "react-router-dom";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

import { URL_CONSTANTS, FOOTER_ITEMS } from "@components/Constants/constants";

import "./Footer.css";

const Footer = () => {
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
                            <a className="footer-link opaque" target="_blank" rel="noreferrer" href={URL_CONSTANTS.twitter}>
                                <div className="img-container">
                                    <FontAwesomeIcon icon={["fa-brands", "fa-twitter"]} />
                                </div>
                            </a>

                            <a className="footer-link opaque" target="_blank" rel="noreferrer" href={URL_CONSTANTS.discord}>
                                <div className="img-container">
                                    <FontAwesomeIcon icon={["fa-brands", "fa-discord"]} />
                                </div>
                            </a>

                            <a className="footer-link opaque" target="_blank" rel="noreferrer" href={URL_CONSTANTS.github}>
                                <div className="img-container">
                                    <FontAwesomeIcon icon={["fa-brands", "fa-github"]} />
                                </div>
                            </a>
                        </div>
                    </div>
                </div>

                {FOOTER_ITEMS.map((category, index) => (
                    <div className="footer-items opaque" key={`${Object.keys(category)}`} style={{gridArea: `item-${index}`}}>
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