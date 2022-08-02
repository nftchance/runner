import { Input } from '@mui/material';
import { StyledEngineProvider } from '@mui/material/styles';

import "./TextFieldInline.css"

const TextFieldInline = (props) => {
    const {
        placeholder,
        error,
        style
    } = props;

    return (
        <StyledEngineProvider injectFirst>
            <Input
                className="text-field-inline"
                placeholder={placeholder}
                error={error ? true : false}
                sx={{style}}
            />
        </StyledEngineProvider>
    )
}

export default TextFieldInline;