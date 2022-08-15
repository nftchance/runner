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

const VolumeBar = ({bar, min, max, idx, hovered, setHovered}) => {
    return (
        <div 
            className={`bar-grid-col ${hovered === idx ? 'hovered' : ''}`}
            onMouseEnter={setHovered}
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
        </div>
    )
}

export default VolumeBar;