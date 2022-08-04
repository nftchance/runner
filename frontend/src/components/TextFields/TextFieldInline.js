import { Input } from '@mui/material';
import { StyledEngineProvider } from '@mui/material/styles';

import "./TextFieldInline.css"

const TextFieldInline = ({placeholder, style}) => {
    return (
        <StyledEngineProvider injectFirst>
            <Input
                className="text-field-inline"
                placeholder={placeholder}
                sx={{style}}
            />
        </StyledEngineProvider>
    )
}

export default TextFieldInline;