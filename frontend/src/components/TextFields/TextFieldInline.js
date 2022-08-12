import { Input } from "@mui/material";

import "./TextFieldInline.css"

const TextFieldInline = ({placeholder, value, onChange, style}) => {
    return (
        <Input
            className="text-field-inline"
            placeholder={placeholder}
            value={value}
            onChange={onChange}
            sx={{style}}
        />
    )
}

export default TextFieldInline;