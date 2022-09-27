import styled from "styled-components";

const BarContainer = styled.div`
    &:before {
        display: none;
        content: "${(props) => props.bar.runner}";
        .before-line {
            display: none;
        }
    }
    &:after {
        display: none;
        content: "${(props) => props.bar.volume}";
    }
`;

const Bar = styled.div`
    height: ${(props) => props.height};
`

const BarGridCol = styled.div`
    &:last-child {
        .bar-container {
            &:after {
                display: ${(props) => props.hiddenLast ? 'hidden' : 'block'};
            }
        }
    }
    &:first-child {
        .bar-container {
            &:after {
                display: ${(props) => props.hiddenFirst ? 'hidden' : 'block'};
            }
        }
    }
`

const VolumeBar = ({bar, min, max, idx, hovered, setHovered}) => {
    return (
        <BarGridCol 
            className={`bar-grid-col ${hovered === idx ? 'hovered' : ''}`}
            onMouseEnter={setHovered}
            hiddenFirst={hovered < 2}
            hiddenLast={hovered > 25}
        >
            <BarContainer 
                className="bar-container"
                bar={bar}
                min={min}
                max={max}
                height={bar.height}
            >
                <div className={`before-line ${idx}`} />
                <Bar height={bar.height} className="bar" />
            </BarContainer>
        </BarGridCol>
    )
}

export default VolumeBar;