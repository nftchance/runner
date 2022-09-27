import { Button } from '@mui/material';

import "./PrimaryButton.css"

const PrimaryButton = ({text, onClick, disabled, style}) => {
    return (
        <Button
            className="btn-primary"
            onClick={onClick}
            disabled={disabled}
            sx={style}
        >
            <span className="text">{text}</span>
        </Button>
    )
}

export default PrimaryButton;