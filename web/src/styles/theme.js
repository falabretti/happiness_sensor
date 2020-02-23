import { makeStyles } from "@material-ui/core";

export const useStyles = makeStyles(theme => ({
    content: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center'
    },
    header: {
        width: '300px',
        textAlign: 'center'
    },
    card: {
        padding: theme.spacing(2),
        margin: theme.spacing(3)
    },
    stream: {
        padding: '.25em .25em',
        maxWidth: '100%',
        height: 'auto',
    },
    streamContainer: {
        display: 'flex'
    },
    status: {
        display: 'flex',
        alignItems: 'center',
        width: '60%',
        justifyContent: 'space-between'
    },
    statusIcon: {
        fontSize: '70px'
    },
    slider: {
        width: '75%'
    }
}));
