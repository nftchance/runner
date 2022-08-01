import { useState } from "react"

import { IconButton } from "@mui/material";
import CloseIcon from '@mui/icons-material/Close';

import "./NavbarMessage.css"

const NavbarMessage = (props) => {
    const { message, directTo } = props;
    const [ closed, setClosed ] = useState(false);

    const handleClose = () => {
        setClosed(true);
    }

    return (
        <>
            {!closed &&
                <div className="msg-container">
                    <a target="_blank" rel="noreferrer" href={directTo}>
                        <p>
                            {message}
                        </p>
                    </a>

                    <div className="close">
                        <IconButton size="small" onClick={handleClose}>
                            <CloseIcon fontSize="inherit"/>
                        </IconButton>
                    </div>
                </div>
            }
        </>
    )
}

export default NavbarMessage;