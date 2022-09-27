import { memo } from "react";

import { Select, MenuItem } from "@mui/material";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import "./CustomSelect.css";

const CustomSelect = ({selected, placeholder, options, onChange}) => {

    const dropdownIcon = () => (
        <FontAwesomeIcon 
            className="chevron" 
            icon={["fal", "angle-down"]} 
        />
    )

    return (
        <div className="select-container">
            <Select
                className="custom-select"
                variant="standard"
                value={selected}
                onChange={onChange}
                IconComponent={dropdownIcon}
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
    )
}

export default memo(CustomSelect);