import { makeStyles } from "@material-ui/core";

export const useStyles = makeStyles(theme => ({
    content: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center'
    },
    header: {
        width: '350px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
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
        display: 'flex',
        flexDirection: 'column',
    },
    status: {
        display: 'flex',
        alignItems: 'center',
        padding: theme.spacing(3)
    },
    statusIcon: {
        fontSize: '100px',
        marginRight: theme.spacing(3),
    },
    headerIcon: {
        fontSize: '70px',
        marginRight: theme.spacing(3),
    },
    slider: {
        width: '100%'
    },
    valueText: {
        marginRight: theme.spacing(3)
    }
}));
