import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

import TextButton from "../Buttons/TextButton";
import "./GhostCard.css"

const GhostCard = (
    {
        title, 
        description, 
        icon, 
        buttonText, 
        buttonOnClick, 
        titleStyle, 
        noIcon
}) => {
    return (
        <div className="ghost-card">
            <div className="title-line">
                {noIcon ?
                    <></>
                    :
                    <div className="icon-container">
                        <FontAwesomeIcon
                            className="ghost-icon"
                            icon={icon}
                        />
                    </div>
                }
                <h4 className="ghost-title" style={titleStyle}>
                    {title}
                </h4>
            </div>

            <h6 className="ghost-description">{description}</h6>
            <TextButton
                text={buttonText}
                onClick={buttonOnClick}
            />
        </div>
    )
}

export default GhostCard;