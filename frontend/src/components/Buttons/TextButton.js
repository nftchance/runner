import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

import { Button } from '@mui/material';
import { StyledEngineProvider } from '@mui/material/styles';

import "./TextButton.css"

const TextButton = ({text, onClick, style}) => {
    return (
        <StyledEngineProvider injectFirst>
            <Button
                className="btn-text"
                onClick={onClick}
                sx={{style}}
            >
                <span className="text">{text}</span>
                <FontAwesomeIcon 
                    className="chevron" 
                    icon={["fal", "angle-right"]} 
                    style={{color: 'inherit'}} 
                />
            </Button>
        </StyledEngineProvider>
    )
}

export default TextButton;