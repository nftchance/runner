import { Select, MenuItem } from "@mui/material";
import { StyledEngineProvider } from '@mui/material/styles';
import { KeyboardArrowDown } from '@mui/icons-material';

import "./CustomSelect.css";

const CustomSelect = ({selected, placeholder, options, onChange}) => {
    return (
        <StyledEngineProvider injectFirst>
            <div className="select-container">
                <Select
                    className="custom-select"
                    variant="standard"
                    value={selected}
                    onChange={onChange}
                    IconComponent={KeyboardArrowDown}
                    displayEmpty
                    renderValue={(selected) => {
                        if (!selected) return <p className="option-text">{placeholder}</p>
                        else return <p className="option-text">{selected}</p>
                    }}
                >
                    {options.map((option) => (
                        <MenuItem 
                            key={option.title} 
                            className="select-option"
                            value={option.title}
                        >
                            {option.title}
                        </MenuItem>
                    ))}
                </Select>
            </div>
        
        </StyledEngineProvider>
    )
}

export default CustomSelect;