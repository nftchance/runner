import { useState, memo } from "react";
import { 
    Accordion, AccordionDetails, AccordionSummary 
} from "@mui/material";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

import "./AccordionPanel.css";

const AccordionPanel = ({title, detail, index, open}) => {
  const [expanded, setExpanded] = useState(open ? `panel-${index}` : false);

  const handleOpen = (panel) => (event, isExpanded) => {
    setExpanded(isExpanded ? panel : false);
  };

  const expandIcon = (
      <FontAwesomeIcon
          className="expand-icon" 
          icon={["fal", "angle-down"]} 
      />
  )

  return (
        <Accordion
            className="accordion"
            expanded={expanded === `panel-${index}`}
            onChange={handleOpen(`panel-${index}`)}
            disableGutters
        >
            <AccordionSummary
                className="accordion-summary"
                expandIcon={ expandIcon }
            >
                <h3>{title}</h3>
            </AccordionSummary>
            <AccordionDetails
                className="accordion-details"
            >
                <h6>{detail}</h6>
            </AccordionDetails>
        </Accordion>
  );
}

export default memo(AccordionPanel);