import { Button } from '@mui/material';
import { StyledEngineProvider } from '@mui/material/styles';

import "./PrimaryButton.css"

const PrimaryButton = ({text, onClick, disabled, style}) => {
    return (
        <StyledEngineProvider injectFirst>
            <Button
                className="btn-primary"
                onClick={onClick}
                disabled={disabled ? true : false}
                sx={{style}}
            >
                <span className="text">{text}</span>
            </Button>
        </StyledEngineProvider>
    )
}

export default PrimaryButton;