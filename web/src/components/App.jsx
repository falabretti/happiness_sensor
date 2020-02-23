import React from 'react';
import 'reset-css';
import Streaming from './Streaming';
import { Container } from '@material-ui/core';
import Header from './Header';
import Status from './Status';
import { useStyles } from '../styles/theme';
import '../styles/styles.css';

export default function App() {
    const classes = useStyles();

    return (
        <Container maxWidth="xl" className={classes.content}>
            <Header />
            <Streaming />
            <Status />
        </Container>
    );
}
