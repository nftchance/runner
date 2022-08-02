import { Button } from '@mui/material';
import { StyledEngineProvider } from '@mui/material/styles';

import "./PrimaryButton.css"

const PrimaryButton = (props) => {
    const {
        text,
        onClick,
        disabled,
        style
    } = props;

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