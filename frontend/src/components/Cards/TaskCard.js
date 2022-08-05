import SecondaryButton from "@components/Buttons/SecondaryButton";

import "./TaskCard.css"

// NOTE: Maybe try to find a way to break out taskCard to allow it to handle TaskCard usage.

const TaskCard = (
    {
        title, 
        description,
        status, 
        statusIndicatorColor, 
        buttonText,
        buttonOnClick
    }
) => {
    return (
        <div className="task-card">
            <div className="task-info">
                <h4 className="task-title">{title}</h4>
                <p className="task-desc">{description}</p>

                <div className="task-status">
                    <div 
                        className={`status-indicator ${statusIndicatorColor}`}
                    />
                    <span className="status-text">{status}</span>
                </div>
            </div>

            <div className="task-actions">
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

export default TaskCard;