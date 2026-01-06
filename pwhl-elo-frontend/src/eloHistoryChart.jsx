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

const createXScales = (data, offSeasons, boundsWidth)=>{
    const end = new Date(data.max_date);
    const start = new Date(data.min_date); // make this the min of the data

    const offSeasonsGaps = offSeasons.map((offseason)=>convertToBufferedArray(offseason));
    const xDiscontinuousScale = scaleDiscontinuous(d3.scaleTime())
        .discontinuityProvider(
            discontinuityRange(...offSeasonsGaps)
        )
        .domain([start, end])
        .range([0, boundsWidth]);

    const xScales = {
        all: xDiscontinuousScale,
        seasons: [],
    }
    // loop through offseasons and use start end to make 
    if(offSeasons.length > 0){
        for(let i=0; i<=offSeasons.length; i++){
            let domain = []
            if(i==0){
                // uses start and offSeasons[0].start
                domain =[start, offSeasons[i].start] 
            }
            else if(i==offSeasons.length){
                // if i == 2, uses offSeasons[1].end and end
                domain =[offSeasons[i - 1].end, end] 
            } else { 
                // if i == 1, uses offSeasons[0].end and offSeasons[1].start
                domain =[offSeasons[i - 1].end, offSeasons[i].start] 
            }
            
            xScales.seasons.push(d3.scaleTime().domain(domain).range([0, boundsWidth]));

        }
        
                    
    }
    
    
    return xScales;

}

const Tooltip = ({ tooltip }) => {
    if (!tooltip) return null;

    return (
        <div
            style={{
                position: 'absolute',
                left: tooltip.x + 10,
                top: tooltip.y - 10,
                backgroundColor: 'white',
                border: '2px solid #333',
                borderRadius: '4px',
                padding: '8px 12px',
                pointerEvents: 'none',
                fontSize: '14px',
                boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
                zIndex: 1000,
                textAlign: 'left',
            }}
        >
            <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>
                {convertAndCapitalize(tooltip.team)}
            </div>
            <div><strong>Date:</strong> {new Date(tooltip.date).toLocaleDateString()}</div>
            <div><strong>Elo:</strong> {Math.round(tooltip.elo)}</div>
        </div>
    );
};

const LineChart = ({ width, height, data, selectedSeason, xScales }) => {
    const domain =[data.min_elo, data.max_elo] // should be [dataMin, dataMax]
    const axesRef = useRef(null);
    const [tooltip, setTooltip] = useState(null);
    const [isMobile, setIsMobile] = useState(false);
    const boundsWidth = width - MARGIN.right - MARGIN.left;
    const boundsHeight = height - MARGIN.top - MARGIN.bottom;

    // Detect if mobile
    useEffect(() => {
        const checkMobile = () => {
            setIsMobile(window.innerWidth <= 768 || 'ontouchstart' in window);
        };
        checkMobile();
        window.addEventListener('resize', checkMobile);
        return () => window.removeEventListener('resize', checkMobile);
    }, []);

    // Get the appropriate scale based on selected season
    const xScale = selectedSeason === 'all' 
        ? xScales.all 
        : xScales.seasons[parseInt(selectedSeason) - 1];

    // Y axis
    const yScale = useMemo(() => {
        return d3.scaleLinear().domain(domain).range([boundsHeight, 0]);
    }, [height]);

    const lineBuilder = d3
        .line()
        .x((d) => {
            return xScale(new Date(d.date))
        }).y((d) => {
            return yScale(d.elo)
        });

    // Function to find closest point on a line to mouse position
    const findClosestPoint = (mouseX, mouseY, teamData) => {
        let closestPoint = null;
        let minDistance = Infinity;

        teamData.games.forEach((game) => {
            const x = xScale(new Date(game.date));
            const y = yScale(game.elo);
            const distance = Math.sqrt(Math.pow(x - mouseX, 2) + Math.pow(y - mouseY, 2));
            
            if (distance < minDistance && distance < 20) { // 20px threshold
                minDistance = distance;
                closestPoint = {
                    ...game,
                    team: teamData.team,
                    x: x + MARGIN.left,
                    y: y + MARGIN.top,
                };
            }
        });

        return closestPoint;
    };

    const handleMouseMove = (e) => {
        if (isMobile) return; // Don't handle mouse events on mobile

        const svg = e.currentTarget;
        const rect = svg.getBoundingClientRect();
        const mouseX = e.clientX - rect.left - MARGIN.left;
        const mouseY = e.clientY - rect.top - MARGIN.top;

        let closest = null;
        let minDist = Infinity;

        data.data.forEach((team) => {
            const point = findClosestPoint(mouseX, mouseY, team);
            if (point) {
                const dist = Math.sqrt(
                    Math.pow(point.x - mouseX - MARGIN.left, 2) + 
                    Math.pow(point.y - mouseY - MARGIN.top, 2)
                );
                if (dist < minDist) {
                    minDist = dist;
                    closest = point;
                }
            }
        });

        setTooltip(closest);
    };

    const handleClick = (e) => {
        if (!isMobile) return; // Only handle clicks on mobile

        const svg = e.currentTarget;
        const rect = svg.getBoundingClientRect();
        const mouseX = e.clientX - rect.left - MARGIN.left;
        const mouseY = e.clientY - rect.top - MARGIN.top;

        let closest = null;
        let minDist = Infinity;

        data.data.forEach((team) => {
            const point = findClosestPoint(mouseX, mouseY, team);
            if (point) {
                const dist = Math.sqrt(
                    Math.pow(point.x - mouseX - MARGIN.left, 2) + 
                    Math.pow(point.y - mouseY - MARGIN.top, 2)
                );
                if (dist < minDist) {
                    minDist = dist;
                    closest = point;
                }
            }
        });

        setTooltip(closest);
    };

    const handleMouseLeave = () => {
        if (!isMobile) {
            setTooltip(null);
        }
    };
        

    // Render the X and Y axis using d3.js, not react
    useEffect(() => {
        const svgElement = d3.select(axesRef.current);
        svgElement.selectAll("*").remove();
        const xAxisGenerator = d3.axisBottom(xScale);
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
    }, [xScale, yScale, boundsHeight]);

    // build the lines

    return (
        <div style={{ position: 'relative' }}>
            <svg 
                width={width} 
                height={height}
                onMouseMove={handleMouseMove}
                onMouseLeave={handleMouseLeave}
                onClick={handleClick}
                style={{ cursor: isMobile ? 'pointer' : 'default' }}
            >
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
                                style={{ pointerEvents: 'none' }}
                            />
                        )
                    })
                }
            </svg>
            <Tooltip tooltip={tooltip} />
            {legend(colors)}
        </div>
    );
};

export const eloHistoryChart = () => {
    const [dimensions, setDimensions] = useState({ width: 500, height: 300 });
    const [selectedSeason, setSelectedSeason] = useState('all');
    const containerRef = useRef(null);

    // Calculate xScales based on dimensions
    const xScales = useMemo(() => {
        const boundsWidth = dimensions.width - MARGIN.right - MARGIN.left;
        return createXScales(chartableWphlElos, offSeasons, boundsWidth);
    }, [dimensions.width]);

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
            
            {xScales.seasons.length > 0 && (
                <div style={{ marginBottom: '20px' }}>
                    <label htmlFor="season-select" style={{ marginRight: '10px' }}>
                        Select Season:
                    </label>
                    <select 
                        id="season-select"
                        value={selectedSeason} 
                        onChange={(e) => setSelectedSeason(e.target.value)}
                        style={{ 
                            padding: '5px 10px', 
                            fontSize: '14px',
                            borderRadius: '4px',
                            border: '1px solid #ccc'
                        }}
                    >
                        <option value="all">All Seasons</option>
                        {xScales.seasons.map((_, index) => (
                            <option key={index} value={index + 1}>
                                Season {index + 1}
                            </option>
                        ))}
                    </select>
                </div>
            )}

            {LineChart({
                width: dimensions.width, 
                height: dimensions.height, 
                data: chartableWphlElos,
                selectedSeason,
                xScales
            })}
        </section>
    );
}