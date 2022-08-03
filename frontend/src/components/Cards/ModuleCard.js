import PrimaryButton from "../Buttons/PrimaryButton";
import SecondaryButton from "../Buttons/SecondaryButton";

import "./ModuleCard.css"

const ModuleCard = (props) => {
    const {
        title,
        description,
        provider,
        providerLogo,
        primaryBtnText,
        primaryBtnOnClick,
        secondaryBtnText,
        secondaryBtnOnClick,
    } = props;

    return (
        <div className="module-card">
            <div className="module-info">
                <h4 className="module-title">{title}</h4>
                <p className="module-desc">{description}</p>

                <div className="module-provider">
                    <div className="provider-icon-container">
                        <img src={providerLogo} alt={provider} />
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