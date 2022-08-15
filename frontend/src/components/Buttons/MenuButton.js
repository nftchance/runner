import { useState, memo } from "react";

import { IconButton, Menu, MenuItem } from "@mui/material";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import "./MenuButton.css";

const MenuButton = ({icon, menuItems, handleMenu}) => {
    const [ anchorEl, setAnchorEl ] = useState(null);
    const open = anchorEl ? true : false;

    return (
        <>
            <IconButton 
                className="menu-btn"
                id="menu-btn"
                aria-controls={open && "menu"}
                aria-haspopup="true"
                aria-expanded={open && true}
                onClick={(event) => setAnchorEl(event.currentTarget)}
                disableRipple
            >
                <FontAwesomeIcon 
                    className="menu-icon" 
                    icon={icon} 
                />
            </IconButton>

            <Menu
                id="menu"
                anchorEl={anchorEl}
                open={open}
                onClose={() => setAnchorEl(null)}
                disableAutoFocusItem
                MenuListProps={{
                    "aria-labelledby": "menu-btn",
                }}
            >
                {menuItems.map((item) => (
                    <MenuItem 
                        key={item}
                        onClick={() => handleMenu(item)}
                    >
                        {item}
                    </MenuItem>
                ))}
            </Menu>
        </>
    )
}

export default memo(MenuButton);