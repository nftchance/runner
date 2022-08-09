import SecondaryButton from "@components/Buttons/SecondaryButton";

import "./ProposalCard.css";

const ProposalCard = (
    {
        title,
        description,
        tags,
        votingPercents,
        buttonText,
        buttonOnClick,
    }
) => {
    return (
        <div className="proposal-card">
            <div className="proposal-info">
                <div className="proposal-tags">
                    {tags.map((tag) => (
                        <div className="tag" key={`tag${tag}`}>
                            <p className="tag-text">{tag}</p>
                        </div>
                    ))}
                </div>
                <h3 className="proposal-title">{title}</h3>
                <p className="proposal-desc">{description}</p>
            </div>

            <div className="votes-bar">
                <div className="yes-votes" style={{width: `${votingPercents[0]}%`}}/>
                <div className="no-votes" style={{width: `${votingPercents[1]}%`}}/>
                <div className="missing-votes" />
            </div>

            <div className="proposal-actions">
                <div className="action-btns">
                    <SecondaryButton
                        text={buttonText}
                        onClick={buttonOnClick}
                    />
                </div>
            </div>
        </div>
    )
}

export default ProposalCard;