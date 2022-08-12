import { useState } from "react"

import { IconButton } from "@mui/material";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import "./SystemMessage.css"

const SystemMessage = ({message, linkTo}) => {
    const [ closed, setClosed ] = useState(false);

    return (
        <>
            {!closed &&
                <div className="system-msg-container">
                    <div className="system-msg-link">
                        <a target="_blank" rel="noreferrer" href={linkTo}>
                            <p className="system-msg">
                                {message}
                            </p>
                        </a>
                    </div>

                    <div className="close">
                        <IconButton className="close-btn" size="small" onClick={() => setClosed(true)}>
                            <FontAwesomeIcon
                                className="close-icon"
                                icon={["fal", "fa-x"]}
                            />
                        </IconButton>
                    </div>
                </div>
            }
        </>
    )
}

export default SystemMessage;