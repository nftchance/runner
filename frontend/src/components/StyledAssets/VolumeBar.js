import { memo } from "react";
import styled from "styled-components";

const BarContainer = styled.div`
    &:hover {
        &:before {
            content: "${(props) => props.bar.runner}";
        }
        &:after {
            content: "${(props) => props.bar.volume}";
        }
    }
    &:last-child {
        &:after {
            content: "${(props) => props.max}";
        }
    }
    &:first-child {
        &:after {
            content: "${(props) => props.min}";
        }
    }
`;

const Bar = styled.div`
    height: ${(props) => props.height};
`

const VolumeBar = ({bar, min, max}) => {
    return (
        <BarContainer 
            className="bar-container"
            bar={bar}
            min={min}
            max={max}
        >
            <div className="before-line" />
            <Bar height={bar.height} className="bar" />
        </BarContainer>
    )
}

export default memo(VolumeBar);