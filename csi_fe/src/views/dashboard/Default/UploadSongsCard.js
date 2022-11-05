import React from 'react'
import PropTypes from 'prop-types';
import { useState } from 'react';

// material-ui
import { useTheme, styled } from '@mui/material/styles';

// project imports
import AnimateButton from 'ui-component/extended/AnimateButton';

// project imports
import MainCard from 'ui-component/cards/MainCard';
import SkeletonTotalOrderCard from 'ui-component/cards/Skeleton/EarningCard';

// third party
import { Formik } from 'formik';

import {
    Box,
    Button,
    FormControl,
    Grid,
    OutlinedInput,
    Stack,
    Snackbar,
    Typography,
    useMediaQuery
} from '@mui/material';

import MuiAlert from '@mui/material/Alert';

import { postSong, getAllSongs } from 'networking'
import CircularProgress from '@mui/material/CircularProgress';

const Alert = React.forwardRef(function Alert(props, ref) {
    return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

const CardWrapper = styled(MainCard)(({ theme }) => ({
    backgroundColor: theme.palette.primary.dark,
    color: '#fff',
    overflow: 'hidden',
    position: 'relative',
    '&>div': {
        position: 'relative',
        zIndex: 5
    },
    '&:after': {
        content: '""',
        position: 'absolute',
        width: 210,
        height: 210,
        background: theme.palette.primary[800],
        borderRadius: '50%',
        zIndex: 1,
        top: -85,
        right: -95,
        [theme.breakpoints.down('sm')]: {
            top: -105,
            right: -140
        }
    },
    '&:before': {
        content: '""',
        position: 'absolute',
        zIndex: 1,
        width: 210,
        height: 210,
        background: theme.palette.primary[800],
        borderRadius: '50%',
        top: -125,
        right: -15,
        opacity: 0.5,
        [theme.breakpoints.down('sm')]: {
            top: -155,
            right: -70
        }
    }
}));

// ==============================|| DASHBOARD - TOTAL ORDER LINE CHART CARD ||============================== //

const SearchForm = ({ setSongList }) => {

    const theme = useTheme();
    const [uploadPending, setUploadPending] = useState(false)
    const [openSuccess, setOpenSuccess] = useState(false)
    const [openError, setOpenError] = useState(false)
    const [error, setError] = useState('')

    const handleClose = () => {
        setOpenSuccess(false)
        setOpenError(false)
    }

    return (
        <>
            <Snackbar sx={{ zIndex: 9999 }} open={openSuccess} autoHideDuration={6000} onClose={handleClose}>
                <Alert onClose={handleClose} severity="success" sx={{ width: '100%' }}>
                    Upload and analysis completed!
                </Alert>
            </Snackbar>
            <Snackbar sx={{ zIndex: 9999 }} open={openError} autoHideDuration={6000} onClose={handleClose}>
                <Alert onClose={handleClose} severity="error" sx={{ width: '100%' }}>
                    Error uploading song: {error}
                </Alert>
            </Snackbar>
            <Formik
                initialValues={{
                    search: ''
                }}
                onSubmit={async (values, { setErrors, setStatus, setSubmitting }) => {
                    setUploadPending(true)
                    postSong({ yt_link: values.search }).then(res => {
                        setUploadPending(false)
                        setOpenSuccess(true)

                        getAllSongs().then(res => {
                            let options = res.map(it => ({ label: it.title, value: it }));
                            setSongList(options);
                        })

                    }).catch(err => {
                        setUploadPending(false)
                        setError(JSON.stringify(err))
                        setOpenError(true)
                    })
                }}
            >
                {({ errors, handleBlur, handleChange, handleSubmit, isSubmitting, touched, values }) => (
                    <form noValidate onSubmit={handleSubmit}>
                        <Grid container justifyContent="space-evenly" alignItems="center" justifyItems="center">
                            <Grid item sx={{ mr: 1, mt: 1.75, mb: 0.75 }} xs={12}>
                                <FormControl fullWidth>
                                    <OutlinedInput
                                        disabled={uploadPending}
                                        id="outlined-adornment-email-login"
                                        value={values.search}
                                        name="search"
                                        onBlur={handleBlur}
                                        onChange={handleChange}
                                        label="Search"
                                        placeholder='Insert YouTube link here...'
                                        inputProps={{}}
                                    />
                                </FormControl>
                            </Grid>
                            <Grid item sx={{ mr: 1, mt: 1.75, mb: 0.75 }} xs={12}>
                                {!uploadPending ?
                                    (<AnimateButton>
                                        <Button
                                            disableElevation
                                            disabled={isSubmitting}
                                            fullWidth
                                            size="large"
                                            type="submit"
                                            variant="contained"
                                            style={{ backgroundColor: theme.palette.primary[800] }}
                                        >
                                            Upload and analyze
                                        </Button>
                                    </AnimateButton>) :
                                    (<Stack alignItems="center">
                                        <CircularProgress color="primary" />
                                    </Stack>)
                                }
                            </Grid>
                        </Grid>
                    </form>
                )}
            </Formik>
        </>
    )
}

const UploadSongsCard = ({ isLoading, setSongList }) => {
    const theme = useTheme();

    const [timeValue, setTimeValue] = useState(false);
    const handleChangeTime = (event, newValue) => {
        setTimeValue(newValue);
    };


    return (
        <>
            {isLoading ? (
                <SkeletonTotalOrderCard />
            ) : (
                <CardWrapper border={false} content={false}>
                    <Box sx={{ p: 2.25 }}>
                        <Grid container direction="column">
                            <Grid item>
                                <Grid container justifyContent="space-between">
                                    <Grid item>
                                        <Typography variant="h4" sx={{ color: '#fff' }}>
                                            New song
                                        </Typography>
                                        <Typography variant="subtitle2" sx={{ color: 'primary.light', mt: 0.25 }}>
                                            Upload and analyze a new song from YouTube
                                        </Typography>
                                    </Grid>
                                    <Grid item>
                                        <Button
                                            disableElevation
                                            variant={timeValue ? 'contained' : 'text'}
                                            size="small"
                                            sx={{ color: 'inherit' }}
                                            onClick={(e) => handleChangeTime(e, true)}
                                        >
                                            YouTube
                                        </Button>
                                    </Grid>
                                </Grid>
                            </Grid>
                            <Grid item sx={{ mb: 0.75 }}>
                                <SearchForm setSongList={setSongList} />
                            </Grid>
                        </Grid>
                    </Box>
                </CardWrapper>
            )}
        </>
    );
};

UploadSongsCard.propTypes = {
    isLoading: PropTypes.bool
};

export default UploadSongsCard;
