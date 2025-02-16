import { useEffect, useMemo, useRef } from "react";
import * as d3 from "d3";
import { scaleDiscontinuous, discontinuityRange } from "@d3fc/d3fc-discontinuous-scale";

import chartableWphlElos from "./assets/chartable_wphl_elos.json"
import {convertAndCapitalize} from "./utils"


const NUMTICKSH = 8;
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
}

const legendItem = (key, color, i) =>{
    // returns one item for a legend. color should be a hex code
    return (
        <div key={"legendItem" + i} className="legend-item">
            <p key={"legendLabel" + i} className="legend-label">{convertAndCapitalize(key)}</p>
            <div key={"colorSwatch" + i} className="color-swatch" style={{"background-color": color}}></div>
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

const LineChart = ({ width, height, data }) => {

    // TODO: should be max of data
    const end = new Date(data.max_date);
    const start = new Date(data.min_date); // make this the min of the data

    const offseasonBuffer = 10;
    const offseasonStart = new Date(2024, 4, 30);
    const offseasonEnd = new Date(2024, 10, 20);
    console.log("offseasonStart start", offseasonStart)
    console.log("offseasonEnd start", offseasonEnd)
    const offseasonStartBuffed = new Date(offseasonStart.setDate(offseasonStart.getDate() + offseasonBuffer));
    const offseasonEndBuffed = new Date(offseasonEnd.setDate(offseasonEnd.getDate() - offseasonBuffer));

    console.log("offseasonStart with buffer", offseasonStart)
    console.log("offseasonEnd with buffer", offseasonEnd)

    const domain =[data.min_elo, data.max_elo] // should be [dataMin, dataMax]
    const axesRef = useRef(null);
    const boundsWidth = width - MARGIN.right - MARGIN.left;
    const boundsHeight = height - MARGIN.top - MARGIN.bottom;
    // const boundsWidth = width;
    // const boundsHeight = height;
    // read the data
    // build the scales and axes
    const xScale = d3.scaleTime()
        .domain([start, end])
        .range([0, boundsWidth]);

    const xDiscontinuousScale = scaleDiscontinuous(d3.scaleTime())
        .discontinuityProvider(discontinuityRange([offseasonStartBuffed, offseasonEndBuffed]))
        .domain([start, end])
        .range([0, boundsWidth]);

    // Y axis
    const yScale = useMemo(() => {
        return d3.scaleLinear().domain(domain).range([boundsHeight, 0]);
    }, [height]);

    const lineBuilder = d3
        .line()
        .x((d) => xDiscontinuousScale(new Date(d.date)))
        .y((d) => yScale(d.elo))
        .defined(function(d) { 
            if(new Date(d.date) > offseasonStart && new Date(d.date) < offseasonEnd){
                return false;
            }
            return true;
        });;

    // Render the X and Y axis using d3.js, not react
    useEffect(() => {
        const svgElement = d3.select(axesRef.current);
        svgElement.selectAll("*").remove();
        const xAxisGenerator = d3.axisBottom(xDiscontinuousScale);
        svgElement
            .append("g")
            .attr("transform", "translate(0," + boundsHeight + ")")
            .call(xAxisGenerator.ticks(NUMTICKSH, "%m/%d/%y")); // How many ticks are targeted

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
                                key={team.team + "elo"}
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
    const width = 500;
    const height = 300;

    return (
        <section>
            <h1 className="oswald-bold">History of WPHL Elo Ratings</h1>

            {LineChart({width:width, height:height, data:chartableWphlElos})}
        </section>
    )
}