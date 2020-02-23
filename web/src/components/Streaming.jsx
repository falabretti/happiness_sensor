import React from 'react';
import { Paper } from '@material-ui/core';
import { useStyles } from '../styles/theme';
import Status from './Status';

export default function Streaming() {
    const classes = useStyles();

    return (
        <Paper elevation={3} className={classes.streamContainer}>
            <img alt="streaming" src="http://localhost:5000/video_feed" className={classes.stream} />
            <Status />
        </Paper>
    );
}
