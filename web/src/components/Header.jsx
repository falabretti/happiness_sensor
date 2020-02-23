import React from 'react';
import { Card, Typography } from '@material-ui/core';
import { useStyles } from '../styles/theme';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faLaughBeam } from '@fortawesome/free-solid-svg-icons'

export default function Header() {
    const classes = useStyles();

    return (
        <Card elevation={3} className={`${classes.card} ${classes.header}`} >
            <FontAwesomeIcon icon={faLaughBeam} className={classes.headerIcon} />
            <Typography variant="h3" style={{ fontSize: 70 }}>Sorria!</Typography>
        </Card>
    );
}
