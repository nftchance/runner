import { Link } from "react-router-dom";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

import { Button } from '@mui/material';
import { StyledEngineProvider } from '@mui/material/styles';

import "./TextButton.css"

const TextButton = (props) => {
    const {
        text,
        redirect,
        style
    } = props;

    return (
        <StyledEngineProvider injectFirst>
            <Link className="link-wrapper" to={redirect}>
                <Button
                    className="btn-text"
                    sx={{style}}
                >
                    <p className="text">{text}</p>
                    <FontAwesomeIcon 
                        className="chevron" 
                        icon={["fal", "angle-right"]} 
                        style={{color: 'inherit'}} 
                    />
                </Button>
            </Link>
        </StyledEngineProvider>
    )
}

export default TextButton;