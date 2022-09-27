import { Button } from '@mui/material';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

import "./TextButton.css"

const TextButton = ({text, onClick, style}) => {
    return (
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
    )
}

export default TextButton;