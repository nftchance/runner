import PrimaryButton from "@components/Buttons/PrimaryButton";
import SecondaryButton from "@components/Buttons/SecondaryButton";

import "./ModuleCard.css";

const ModuleCard = (
    {
        title, 
        description, 
        provider, 
        providerLogo, 
        primaryBtnText, 
        primaryBtnOnClick, 
        secondaryBtnText, 
        secondaryBtnOnClick
    }
) => {
    return (
        <div className="module-card">
            <div className="module-info">
                <h4 className="module-title">{title}</h4>
                <p className="module-desc">{description}</p>

                <div className="module-provider">
                    <div 
                        className="provider-icon-container"
                        style={{backgroundImage: `url(${providerLogo})`}}
                    >
                    </div>
                    <span className="provider-name">{provider}</span>
                </div>
            </div>

            <div className="module-actions">
                <div className="action-btns">
                    <PrimaryButton
                        text={primaryBtnText}
                        onClick={primaryBtnOnClick}
                    />
                    <SecondaryButton
                        text={secondaryBtnText}
                        onClick={secondaryBtnOnClick}
                    />
                </div>
            </div>
        </div>
    )
}

export default ModuleCard;