import { Button } from "@mui/material";

import "./SecondaryButton.css"

const SecondaryButton = ({text, onClick, disabled, style}) => {
    return (
        <Button
            className="btn-secondary"
            onClick={onClick}
            disabled={disabled}
            sx={{style}}
        >
            <span className="text">{text}</span>
        </Button>
    )
}

export default SecondaryButton;