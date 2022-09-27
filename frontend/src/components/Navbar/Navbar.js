import { useState, useRef } from "react";
import { Link } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useMediaQuery, IconButton, Slide } from "@mui/material";

import { URL_CONSTANTS } from "@components/Constants/constants";

import "./Navbar.css";

const Navbar = () => {
    const [ open, setOpen ] = useState(false);
    const navBreakpoint = useMediaQuery('(min-width: 900px)');
    const navRef = useRef(null);

    return (
        <nav>
            <div id="navbar">
                <div id="nav-logo">
                    <Link className="nav-link" to="/">
                        <div className="text-with-icon">
                            <div className="img-container">
                                <img data-testid="nav-badge" id="nav-badge" src="/badge.svg" alt="Runner badge" />
                            </div>
                            <h4>runner</h4>
                        </div>
                    </Link>
                </div>
                {navBreakpoint ?
                    <div className="nav-flex" id="nav-desktop">
                        <ul>
                            <li>
                                <Link className="nav-link" to="/roadmap">
                                    <span className="nav-item">Roadmap</span>
                                </Link>
                            </li>
                            <li>
                                <Link className="nav-link" to="/governance">
                                    <span className="nav-item">Governance</span>
                                </Link>
                            </li>
                            <li>
                                <Link className="nav-link" to="/FAQ">
                                    <span className="nav-item">FAQ</span>
                                </Link>
                            </li>
                        </ul>

                        <div className="nav-icons">
                            <a className="nav-link" target="_blank" rel="noreferrer" href={URL_CONSTANTS.github}>
                                <div className="text-with-icon">
                                    <div className="img-container">
                                        <FontAwesomeIcon icon={["fal", "star"]} style={{color: "inherit"}} />
                                    </div>
                                    <span className="nav-item">Star on GitHub</span>
                                </div>
                            </a>

                            <div className="social-icons">
                                <a className="nav-link" target="_blank" rel="noreferrer" href={URL_CONSTANTS.twitter}>
                                    <div className="img-container">
                                        <FontAwesomeIcon icon="fa-brands fa-twitter" />
                                    </div>
                                </a>

                                <a className="nav-link" target="_blank" rel="noreferrer" href={URL_CONSTANTS.discord}>
                                    <div className="img-container">
                                        <FontAwesomeIcon icon={["fa-brands", "fa-discord"]} />
                                    </div>
                                </a>
                            </div>
                        </div>
                    </div>
                    :
                    <div id="nav-mobile">
                        <div className="nav-link" id="nav-menu">
                            <IconButton 
                                id="nav-hamburger"
                                aria-describedby={"nav-mobile-popover"}
                                onClick={() => setOpen(!open)}
                            >
                                <FontAwesomeIcon
                                    icon={["fal", "fa-bars"]}
                                />
                            </IconButton>
                        </div>
                    </div>
                }
            </div>

            {!navBreakpoint && 
                <>
                    <div id="nav-popout" ref={navRef}>
                        <Slide direction="down" in={open} container={navRef.current}>
                            <div id="nav-mobile-grid">
                                <ul>
                                    <li>
                                        <h4>Pages</h4>
                                    </li>
                                    <li>
                                        <Link className="nav-link" to="/roadmap">
                                            <span className="nav-item">Roadmap</span>
                                        </Link>
                                    </li>
                                    <li>
                                        <Link className="nav-link" to="/governance">
                                            <span className="nav-item">Governance</span>
                                        </Link>
                                    </li>
                                    <li>
                                        <Link className="nav-link" to="/FAQ">
                                            <span className="nav-item">FAQ</span>
                                        </Link>
                                    </li>
                                </ul>

                                <ul>
                                    <li>
                                        <h4>Socials</h4>
                                    </li>
                                    <li>
                                        <a className="nav-link" target="_blank" rel="noreferrer" href={URL_CONSTANTS.github}>
                                            <div className="text-with-icon">
                                                <div className="img-container">
                                                    <FontAwesomeIcon icon={["fal", "star"]} style={{color: "inherit"}} />
                                                </div>
                                                <span className="nav-item">Star on GitHub</span>
                                            </div>
                                        </a>
                                    </li>
                                    <li>
                                        <a className="nav-link" target="_blank" rel="noreferrer" href={URL_CONSTANTS.twitter}>
                                            <div className="text-with-icon">
                                                <div className="img-container">
                                                    <FontAwesomeIcon icon="fa-brands fa-twitter" />
                                                </div>
                                                <span className="nav-item">Follow on Twitter</span>
                                            </div>
                                        </a>
                                    </li>
                                    <li>
                                        <a className="nav-link" target="_blank" rel="noreferrer" href={URL_CONSTANTS.discord}>
                                            <div className="text-with-icon">
                                                <div className="img-container">
                                                    <FontAwesomeIcon icon={["fa-brands", "fa-discord"]} />
                                                </div>
                                                <span className="nav-item">Join the Discord</span>
                                            </div>
                                        </a>
                                    </li>
                                </ul>
                            </div>
                        </Slide>
                    </div>

                    <Slide direction="up" in={open}>
                        <div id="nav-action-btn" className="system-msg-container">
                            <Link id="nav-action-link" to="/signup">
                                <span className="system-msg">Step into 2032</span>
                            </Link>
                        </div>
                    </Slide>
                </>
            }
        </nav>
    )
}

export default Navbar;