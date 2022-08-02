import { Link } from "react-router-dom"
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

import { URL_CONSTANTS } from "../Constants/constants";

import "./Navbar.css"

const Navbar = () => {
    return (
        <nav>
            <ul>
                <li>
                    <Link className="link" to="/">
                        <div className="text-with-icon">
                            <div className="img-container">
                                <img id="badge" src="/badge.svg" alt="Runner badge" />
                            </div>
                            <h5>runner</h5>
                        </div>
                    </Link>
                </li>
                <li>
                    <Link className="link" to="/roadmap">
                        <p className="nav-item">Roadmap</p>
                    </Link>
                </li>
                <li>
                    <Link className="link" to="/governance">
                        <p className="nav-item">Governance</p>
                    </Link>
                </li>
                <li>
                    <Link className="link" to="/FAQ">
                        <p className="nav-item">FAQ</p>
                    </Link>
                </li>
            </ul>

            <div className="nav-icons">
                <a className="link" target="_blank" rel="noreferrer" href={URL_CONSTANTS.github}>
                    <div className="text-with-icon">
                        <div className="img-container">
                            <FontAwesomeIcon icon={["fal", "star"]} style={{color: 'inherit'}} />
                        </div>
                        <p className="nav-item">Star on GitHub</p>
                    </div>
                </a>

                <div className="social-icons">
                    <a className="link" target="_blank" rel="noreferrer" href={URL_CONSTANTS.discord}>
                        <div className="img-container">
                            <FontAwesomeIcon icon={["fa-brands", "fa-discord"]} />
                        </div>
                    </a>

                    <a className="link" target="_blank" rel="noreferrer" href={URL_CONSTANTS.twitter}>
                        <div className="img-container">
                            <FontAwesomeIcon icon="fa-brands fa-twitter" />
                        </div>
                    </a>
                </div>
            </div>
        </nav>
    )
}

export default Navbar;