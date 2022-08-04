import { useState } from "react"

import { IconButton } from "@mui/material";
import CloseIcon from '@mui/icons-material/Close';

import "./SystemMessage.css"

const SystemMessage = ({message, directTo}) => {
    const [ closed, setClosed ] = useState(false);

    const handleClose = () => {
        setClosed(true);
    }

    return (
        <>
            {!closed &&
                <div className="system-msg-container">
                    <div className="system-msg-link">
                        <a target="_blank" rel="noreferrer" href={directTo}>
                            <p className="system-msg">
                                {message}
                            </p>
                        </a>
                    </div>

                    <div className="close">
                        <IconButton className="close-btn" size="small" onClick={handleClose}>
                            <CloseIcon fontSize="inherit"/>
                        </IconButton>
                    </div>
                </div>
            }
        </>
    )
}

export default SystemMessage;