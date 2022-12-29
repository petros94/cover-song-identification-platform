import PropTypes from 'prop-types';
import { useEffect, useState } from 'react';

// material-ui
import { useTheme } from '@mui/material/styles';
import { Avatar, Button, CardActions, CardContent, Divider, Grid, Menu, Stack, Typography } from '@mui/material';

// project imports
import MainCard from 'ui-component/cards/MainCard';
import SkeletonPopularCard from 'ui-component/cards/Skeleton/PopularCard';
import { gridSpacing } from 'store/constant';

import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import { getAllSongs, predictPair } from 'networking';
import AnimateButton from 'ui-component/extended/AnimateButton';
import CircularProgress from '@mui/material/CircularProgress';

function ComboBox({ value, setValue, options }) {
    return (
        <Autocomplete
            disablePortal
            id="combo-box-demo"
            options={options}
            value={value}
            onChange={(event, newValue) => {
                setValue(newValue);
            }}
            sx={{ minWidth: 200, maxWidth: 300 }}
            renderInput={(params) => <TextField {...params} label="Song title" />}
            ListboxProps={
                {
                    style: {
                        maxHeight: '200px'
                    }
                }
            }
        />
    );
}

// ==============================|| DASHBOARD DEFAULT - POPULAR CARD ||============================== //

const CompareCoversCard = ({ isLoading, songList }) => {
    const theme = useTheme();

    const [result, setResult] = useState(null)
    const [song1, setSong1] = useState(null)
    const [song2, setSong2] = useState(null)
    const [uploadPending, setUploadPending] = useState(false)

    const handleCompare = () => {
        console.log(`Comparing ${song1.value}, ${song2.value}`)
        setUploadPending(true)
        predictPair(song1.value._id, song2.value._id).then(res => setResult(res))
            .then(res => {
                setUploadPending(false)
            }).catch(ex => setUploadPending(false))
    }

    return (
        <>
            {isLoading ? (
                <SkeletonPopularCard />
            ) : (
                <MainCard content={false}>
                    <CardContent>
                        <Grid container spacing={gridSpacing}>
                            <Grid item xs={12}>
                                <Grid container alignContent="center" justifyContent="space-between">
                                    <Grid item>
                                        <Typography variant="h4">Cover check</Typography>
                                    </Grid>
                                </Grid>
                            </Grid>
                            <Grid item xs={12}>
                                <Typography>
                                    Select two songs from the database to check if they are covers or not.
                                </Typography>
                            </Grid>
                            <Grid container item xs={12}>
                                <Grid container item xs={6}>
                                    <Grid item>
                                        <Typography variant="h5">
                                            Song 1
                                        </Typography>
                                    </Grid>
                                    <Grid item xs={12} sx={{ mr: 5, mt: 2, mb: 2 }}>
                                        <ComboBox options={songList} value={song1} setValue={setSong1} />
                                    </Grid>
                                </Grid>
                                <Grid container item xs={6}>
                                    <Grid item>
                                        <Typography variant="h5">
                                            Song 2
                                        </Typography>
                                    </Grid>
                                    <Grid item xs={12} sx={{ mr: 5, mt: 2, mb: 2 }}>
                                        <ComboBox options={songList} value={song2} setValue={setSong2} />
                                    </Grid>
                                </Grid>
                            </Grid>
                            {result && (
                                <>
                                    <Grid item xs={12}>
                                        <Typography display="inline" variant="h5">
                                            {`Result: `}
                                        </Typography>
                                        <Typography display="inline" fontWeight={500} sx={{ color: result.is_cover ? 'green' : 'red' }}>
                                            {result.is_cover ? 'covers' : 'not covers'}
                                        </Typography>
                                    </Grid>
                                    <Grid item xs={12}>
                                        <Typography display="inline" variant="h5">
                                            {`Distance: `}
                                        </Typography>
                                        <Typography display="inline">
                                            {result.dist.toFixed(3)}
                                        </Typography>
                                    </Grid>
                                </>
                            )}
                        </Grid>
                    </CardContent>
                    <CardActions sx={{ p: 1.25, pt: 0, pb: 2, justifyContent: 'center' }}>
                        {!uploadPending ?
                            (<AnimateButton>
                                <Button sx={{ p: 1, pl: 10, pr: 10 }}
                                    color="secondary"
                                    variant="contained"
                                    disableElevation
                                    onClick={handleCompare}>
                                    Compare
                                </Button>
                            </AnimateButton>) :
                            (<Stack alignItems="center">
                                <CircularProgress color="secondary" />
                            </Stack>)
                        }
                    </CardActions>
                </MainCard>
            )
            }
        </>
    );
};

CompareCoversCard.propTypes = {
    isLoading: PropTypes.bool
};

export default CompareCoversCard;
