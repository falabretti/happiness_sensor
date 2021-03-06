import React from 'react';
import { Typography, Slider, createMuiTheme, ThemeProvider } from '@material-ui/core';
import { useStyles } from '../styles/theme';
import socketIOClient from "socket.io-client";
import { useEffect } from 'react';
import { useState } from 'react';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faLaughBeam, faFrown, faMeh } from '@fortawesome/free-solid-svg-icons'

// const colors = ['#0cb528', '#3db126', '#55ad24', '#67a822', '#76a420', '#839f1e', '#8f9a1c', '#99951a', '#a48f18',
//     '#ad8a16', '#b68314', '#bf7d13', '#c87612', '#d06e10', '#d7650f', '#df5c0f', '#e7500e', '#ee430e', '#f5300e', '#fc0e0e'].reverse();

const colors = ['#f2293a', '#fd582b', '#ff7d19', '#ff9f05', '#ffc00a', '#f2cd0a', '#e4da19', '#d4e62c', '#b6e12d', '#97dc32', '#75d639', '#4dcf42'];
const icons = [faFrown, faMeh, faLaughBeam];

export default function Status() {
    const classes = useStyles();
    const [value, setValue] = useState(50);
    const [color, setColor] = useState(colors[parseInt(colors.length / 2)]);
    const [icon, SetIcon] = useState(icons[1]);

    document.body.style.background = color;

    const sliderTheme = createMuiTheme({
        overrides: {
            MuiSlider: {
                thumb: {
                    display: 'none'
                },
                track: {
                    color: color,
                    height: '40px',
                    margin: '-20px 0',
                    transition: '1000ms ease !important'
                },
                rail: {
                    color: 'black ',
                    height: '40px',
                    margin: '-20px 0'
                }
            }
        }
    });

    useEffect(() => {
        const socket = socketIOClient('http://localhost:5000');
        socket.on('stats', async data => {
            const info = JSON.parse(data);
            const idx = parseInt(Math.min(info.ratio * colors.length, colors.length - 1));
            const iconIdx = parseInt(Math.min(info.ratio * 3, 2));
            const newValue = parseInt(info.ratio * 100);

            setValue(newValue);
            setColor(colors[idx]);
            SetIcon(icons[iconIdx]);
        })
    }, []);

    return (
        <div className={classes.status}>
            <FontAwesomeIcon icon={icon} className={classes.statusIcon} />

            <div style={{ width: '12em', textAlign: 'right' }}>
                <Typography variant="h3" className={classes.valueText}>{`${value}%`}</Typography>
            </div>

            <ThemeProvider theme={sliderTheme}>
                <Slider value={value} className={classes.slider} />
            </ThemeProvider>
        </div>
    );
}
