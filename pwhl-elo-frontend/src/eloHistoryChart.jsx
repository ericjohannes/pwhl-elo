import { useEffect, useMemo, useRef, useState } from "react";
import * as d3 from "d3";
import { scaleDiscontinuous, discontinuityRange } from "@d3fc/d3fc-discontinuous-scale";

import chartableWphlElos from "./assets/chartable_wphl_elos.json"

import {convertAndCapitalize} from "./utils"


const NUMTICKSH = 9;
const NUMTICKSV = 6;

// create a time parser function that works for our time format
const customTimeParser = d3.timeParse("%Y-%m-%dT%H:%M:%S.%fZ");
const MARGIN = { top: 30, right: 30, bottom: 50, left: 50 };

const colors = {
    "minnesota": "rgb(37, 14, 98)",
    "boston": "#04812c",
    "montréal": "#044c99",
    "new_york": "#0BC5EA",
    "toronto": "#fcc60d",
    "ottawa": "#ee2f09",
    "seattle": "#8cb7c9",
    "vancouver": "#af6c45",
}

const legendItem = (key, color, i) =>{
    // returns one item for a legend. color should be a hex code
    return (
        <div key={"legendItem" + i} className="legend-item">
            <p key={"legendLabel" + i} className="legend-label">{convertAndCapitalize(key)}</p>
            <div key={"colorSwatch" + i} className="color-swatch" style={{"backgroundColor": color}}></div>
        </div>
    )

}
const legend = (colorMap)=>{
    return (
        <div className="line-chart-legend">
       {
            Object.entries(colorMap).map((entry,i)=>{
                return(legendItem(entry[0], entry[1], i))
            })
        }
        </div>
    )
}

const convertToBufferedArray = (offseason) =>{
    const buffer = 10; // days
    const startBuffed = new Date(offseason.start.getTime());
    startBuffed.setDate(startBuffed.getDate() + buffer);
    const endBuffed = new Date(offseason.end.getTime());
    endBuffed.setDate(endBuffed.getDate() - buffer);
    return [startBuffed, endBuffed]
}
const LineChart = ({ width, height, data }) => {

    const end = new Date(data.max_date);
    const start = new Date(data.min_date); // make this the min of the data

    const offSeasons = [
        { // between seasons 1 and 2
            start: new Date(2024, 4, 30),
            end: new Date(2024, 10, 19),
        },
        { // between seasons 2 and 3
            start: new Date(2025, 4, 27),
            end:  new Date(2025, 10, 12),
        }
    ]
    
    const offSeasonsGaps = offSeasons.map((offseason)=>convertToBufferedArray(offseason));

    const domain =[data.min_elo, data.max_elo] // should be [dataMin, dataMax]
    const axesRef = useRef(null);
    const boundsWidth = width - MARGIN.right - MARGIN.left;
    const boundsHeight = height - MARGIN.top - MARGIN.bottom;

    // read the data
    // build the scales and axes
    const xDiscontinuousScale = scaleDiscontinuous(d3.scaleTime())
        .discontinuityProvider(
            discontinuityRange(...offSeasonsGaps)
        )
        .domain([start, end])
        .range([0, boundsWidth]);

    // Y axis
    const yScale = useMemo(() => {
        return d3.scaleLinear().domain(domain).range([boundsHeight, 0]);
    }, [height]);

    const lineBuilder = d3
        .line()
        .x((d) => {
            return xDiscontinuousScale(new Date(d.date))
        }).y((d) => {
            return yScale(d.elo)
        });
        

    // Render the X and Y axis using d3.js, not react
    useEffect(() => {
        const svgElement = d3.select(axesRef.current);
        svgElement.selectAll("*").remove();
        const xAxisGenerator = d3.axisBottom(xDiscontinuousScale);
        svgElement
            .append("g")
            .attr("transform", "translate(0," + boundsHeight + ")")
            .call(xAxisGenerator.ticks(NUMTICKSH, "%m/%d/%y"))
            .selectAll("text")  
            .style("text-anchor", "start")
            .attr("dx", "5px")
            .attr("dy", "5px")
            .attr("transform", "rotate(45)"); // How many ticks are targeted

        const yAxisGenerator = d3.axisLeft(yScale);
        svgElement.append("g").call(yAxisGenerator.ticks(NUMTICKSV));
    }, [xDiscontinuousScale, yScale, boundsHeight]);

    // build the lines

    return (
        <div>
            <svg width={width} height={height}>
                <g
                    width={boundsWidth}
                    height={boundsHeight}
                    ref={axesRef}
                    transform={`translate(${[MARGIN.left, MARGIN.top].join(",")})`}
                />
                {
                    data.data.map((team)=>{
                        const linePath = lineBuilder(team.games);                        
                        return(
                            <path
                                key={team.team + team.season + "elo"}
                                d={linePath}
                                stroke={colors[team.team]}
                                fill="none"
                                strokeWidth={2}
                                transform={`translate(${[MARGIN.left, MARGIN.top].join(",")})`}
                            />
                        )
                    })
                }
            </svg>
            {legend(colors)}
        </div>
    );
};

export const eloHistoryChart = () => {
    const [dimensions, setDimensions] = useState({ width: 500, height: 300 });
    const containerRef = useRef(null);

    useEffect(() => {
        const handleResize = () => {
            if (containerRef.current) {
                const containerWidth = containerRef.current.offsetWidth;
                // Use container width but cap at a maximum for desktop
                const width = Math.min(containerWidth - 40, 800); // 40px for padding, max 800px
                const height = Math.max(300, width * 0.6); // Maintain aspect ratio, min 300px
                setDimensions({ width, height });
            }
        };

        // Initial size
        handleResize();

        // Add resize listener
        window.addEventListener('resize', handleResize);
        
        // Cleanup
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    return (
        <section ref={containerRef}>
            <h1 className="oswald-bold">History of PWHL Elo Ratings</h1>

            {LineChart({width: dimensions.width, height: dimensions.height, data: chartableWphlElos})}
        </section>
    );
}