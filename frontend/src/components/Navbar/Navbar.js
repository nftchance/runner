import { Link } from "react-router-dom"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"

import { URL_CONSTANTS } from "@components/Constants/constants";

import "./Navbar.css"

const Navbar = () => {
    return (
        <nav>
            <ul>
                <li>
                    <Link className="nav-link" to="/">
                        <div className="text-with-icon">
                            <div className="img-container">
                                <img id="nav-badge" src="/badge.svg" alt="Runner badge" />
                            </div>
                            <h4>runner</h4>
                        </div>
                    </Link>
                </li>
                <li>
                    <Link className="nav-link opaque" to="/roadmap">
                        <span className="nav-item">Roadmap</span>
                    </Link>
                </li>
                <li>
                    <Link className="nav-link opaque" to="/governance">
                        <span className="nav-item">Governance</span>
                    </Link>
                </li>
                <li>
                    <Link className="nav-link opaque" to="/FAQ">
                        <span className="nav-item">FAQ</span>
                    </Link>
                </li>
            </ul>

            <div className="nav-icons">
                <a className="nav-link opaque" target="_blank" rel="noreferrer" href={URL_CONSTANTS.github}>
                    <div className="text-with-icon">
                        <div className="img-container">
                            <FontAwesomeIcon icon={["fal", "star"]} style={{color: "inherit"}} />
                        </div>
                        <span className="nav-item">Star on GitHub</span>
                    </div>
                </a>

                <div className="social-icons">
                    <a className="nav-link opaque" target="_blank" rel="noreferrer" href={URL_CONSTANTS.discord}>
                        <div className="img-container">
                            <FontAwesomeIcon icon={["fa-brands", "fa-discord"]} />
                        </div>
                    </a>

                    <a className="nav-link opaque" target="_blank" rel="noreferrer" href={URL_CONSTANTS.twitter}>
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