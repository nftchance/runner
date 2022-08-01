import StarBorderIcon from '@mui/icons-material/StarBorder';

import NavbarMessage from "./NavbarMessage";
import "./Navbar.css"

const Navbar = () => {
    const message = "Runner is currently in Beta | Read the latest article";
    const directTo = "https://www.medium.com"

    return (
        <>
            <NavbarMessage message={message} directTo={directTo} />
            
            <nav>
                <ul>
                    <li>
                        <div className="text-with-icon">
                            <div className="img-container">
                                <img id="badge" src="/badge.svg" alt="Runner badge" />
                            </div>
                            <h5>runner</h5>
                        </div>
                    </li>
                    <li>
                        <p>Roadmap</p>
                    </li>
                    <li>
                        <p>Governance</p>
                    </li>
                    <li>
                        <p>FAQ</p>
                    </li>
                </ul>

                <div className="nav-icons">

                    <div className="text-with-icon">
                        <div className="img-container">
                            <StarBorderIcon id="star" fontSize="small" sx={{color: '#707070'}} />
                        </div>
                        <p>Star on GitHub</p>
                    </div>

                    <div className="social-icons">
                        <div className="img-container">
                            <img src="/twitter-white.png" alt="Twitter logo" />
                        </div>

                        <div className="img-container">
                            <img src="/discord-white.png" alt="Discord logo" />
                        </div>
                    </div>
                </div>
            </nav>
        </>
    )
}

export default Navbar;