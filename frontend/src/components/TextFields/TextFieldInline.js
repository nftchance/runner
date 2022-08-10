import { Input } from "@mui/material";
import { StyledEngineProvider } from "@mui/material/styles";

import "./TextFieldInline.css"

const TextFieldInline = ({placeholder, value, onChange, style}) => {
    return (
        <StyledEngineProvider injectFirst>
            <Input
                className="text-field-inline"
                placeholder={placeholder}
                value={value}
                onChange={onChange}
                sx={{style}}
            />
        </StyledEngineProvider>
    )
}

export default TextFieldInline;