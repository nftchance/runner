import { memo, useState } from "react"

import VolumeBar from "./VolumeBar";
import { VOLUME_BARS } from "@components/Constants/copy";

import "./VolumeGraph.css";

const VolumeGraph = () => {
    const [ hoveredItem, setHoveredItem ] = useState(13);

    return (
        <div id="vol-graph">
            <div className="bars">
                {VOLUME_BARS.map((bar, idx) => (
                    <VolumeBar 
                        key={`bar-${idx}`}
                        bar={bar} 
                        min={VOLUME_BARS[0].volume}
                        max={VOLUME_BARS[VOLUME_BARS.length-1].volume}
                        idx={idx}
                        hovered={hoveredItem}
                        setHovered={() => setHoveredItem(idx)}
                    />
                ))}
            </div>

            {/* <div className="axis">
                <span className="limit">VOLUME_BARS[0].volume</span>

            </div> */}
        </div>
    )
}

export default memo(VolumeGraph);