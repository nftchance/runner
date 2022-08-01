import "./Navbar.css"
import NavbarMessage from "./NavbarMessage";

const Navbar = () => {
    const message = "Runner is currently in Beta | Read the latest article";
    const directTo = "https://www.medium.com"

    return (
        <>
            <NavbarMessage message={message} directTo={directTo} />
            
            <nav>
                <ul>
                    <li>
                        <div className="img-container">
                            <img src="/badge.svg" alt="Runner badge" />
                        </div>
                        <h5>runner</h5>
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

                    <li>
                        <p>Star on GitHub</p>
                    </li>

                    <li>
                        <div className="img-container">
                            <img src="/twitter-white.png" alt="Twitter logo" />
                        </div>
                    </li>

                    <li>
                        <div className="img-container">
                            <img src="/discord-white.png" alt="Discord logo" />
                        </div>
                    </li>
                </ul>
            </nav>
        </>
    )
}

export default Navbar;