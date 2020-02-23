import React from 'react';
import EmojiEmotionsIcon from '@material-ui/icons/EmojiEmotions';
import { Card, Typography, Slider, createMuiTheme, ThemeProvider } from '@material-ui/core';
import { useStyles } from '../styles/theme';
import socketIOClient from "socket.io-client";
import { useEffect } from 'react';
import { useState } from 'react';

const colors = ['#0cb528', '#3db126', '#55ad24', '#67a822', '#76a420', '#839f1e', '#8f9a1c', '#99951a', '#a48f18',
    '#ad8a16', '#b68314', '#bf7d13', '#c87612', '#d06e10', '#d7650f', '#df5c0f', '#e7500e', '#ee430e', '#f5300e', '#fc0e0e'].reverse();

export default function Status() {
    const classes = useStyles();
    const [value, setValue] = useState(50);
    const [color, setColor] = useState(colors[9]);

    document.body.style.backgroundColor = color;
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
    })

    useEffect(() => {
        const socket = socketIOClient('http://localhost:5000');
        socket.on('stats', async data => {
            const info = JSON.parse(data);
            const idx = parseInt(Math.min(info.ratio * 20, 19));
            const newValue = parseInt(info.ratio * 100);

            setValue(newValue);
            setColor(colors[idx]);
        })
    }, []);

    return (
        <Card elevation={3} className={`${classes.card} ${classes.status}`}>
            <EmojiEmotionsIcon className={classes.statusIcon} />
            <Typography variant="h4">{`${value}%`}</Typography>
            <ThemeProvider theme={sliderTheme}>
                <Slider value={value} className={classes.slider} />
            </ThemeProvider>
        </Card>
    );
}
