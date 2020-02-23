import React from 'react';
import { Card, Typography } from '@material-ui/core';
import { useStyles } from '../styles/theme';

export default function Header() {
    const classes = useStyles();

    return (
        <Card elevation={3} className={`${classes.card} ${classes.header}`} >
            <Typography variant="h3">Sorria!</Typography>
        </Card>
    );
}
