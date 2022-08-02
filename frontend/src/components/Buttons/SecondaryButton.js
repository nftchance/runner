import { Button } from '@mui/material';
import { StyledEngineProvider } from '@mui/material/styles';

import "./SecondaryButton.css"

const SecondaryButton = (props) => {
    const {
        text,
        onClick,
        disabled,
        style
    } = props;

    return (
        <StyledEngineProvider injectFirst>
            <Button
                className="btn-secondary"
                onClick={onClick}
                disabled={disabled ? true : false}
                sx={{style}}
            >
                <span className="btn-text">{text}</span>
            </Button>
        </StyledEngineProvider>
    )
}

export default SecondaryButton;