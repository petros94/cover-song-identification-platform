import React from 'react'
import { useEffect, useState } from 'react';
import { useSearchParams } from "react-router-dom";
import { useTheme } from '@mui/material/styles';

import { Avatar, Button, CardActions, CardContent, Divider, Grid, Menu, Stack, Typography, Switch } from '@mui/material';

import SkeletonPopularCard from 'ui-component/cards/Skeleton/PopularCard';
import MainCard from 'ui-component/cards/MainCard';

import { gridSpacing } from 'store/constant';
import { getAllSongs, getSong, predictRank, predictRankAggregated } from 'networking';
import ComboBox from 'ui-component/ComboBox';

import AnimateButton from 'ui-component/extended/AnimateButton';
import CircularProgress from '@mui/material/CircularProgress';
import KeyboardArrowUpOutlinedIcon from '@mui/icons-material/KeyboardArrowUpOutlined';
import Microphone from 'ui-component/Microphone';

const RankItem = ({ song }) => {
    const { title, dist, is_cover } = song;

    const theme = useTheme();

    return (
        <>
            <Grid container item direction="column">
                <Grid item>
                    <Grid container alignItems="center" justifyContent="space-between">
                        <Grid item>
                            <Typography variant="subtitle1" color="inherit">
                                {title}
                            </Typography>
                        </Grid>
                        <Grid item>
                            <Grid container alignItems="center" justifyContent="space-between">
                                <Grid item>
                                    <Typography variant="subtitle1" color="inherit">
                                        {((2 - dist) / 2 * 100).toFixed(1)}%
                                    </Typography>
                                </Grid>
                                {is_cover != null &&
                                    <Grid item>
                                        <Avatar
                                            variant="rounded"
                                            sx={{
                                                width: 16,
                                                height: 16,
                                                borderRadius: '5px',
                                                backgroundColor: is_cover ? theme.palette.success.light : theme.palette.error.light,
                                                color: is_cover ? theme.palette.success.dark : theme.palette.error.dark,
                                                ml: 2
                                            }}
                                        >
                                            <KeyboardArrowUpOutlinedIcon fontSize="small" color="inherit" />
                                        </Avatar>
                                    </Grid>
                                }
                            </Grid>
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
            <Divider sx={{ my: 1.5 }} />
        </>
    )
}

const Rank = () => {
    const [searchParams, setSearchParams] = useSearchParams();
    const [isLoading, setLoading] = useState(true);
    const [songList, setSongList] = useState([]);
    const [song, setSong] = useState(null)
    const [rankPending, setRankPending] = useState(false)
    const [rankList, setRankList] = useState([])
    const [sdm, setSdm] = useState(true);

    useEffect(() => {
        getAllSongs().then(res => {
            let options = res.map(it => ({ label: it.title, value: it }));
            setSongList(options);
            setLoading(false);
        }).catch(res => {
            setLoading(false);
        })

        const querySong = searchParams.get("query_song");
        if (querySong != null) {
            getSong(querySong).then(res => {
                setSong({ label: res.title, value: res });
                handleRank({ label: res.title, value: res });
            })
        }
    }, [])

    const handleRank = (selectedSong) => {
        setRankPending(true);

        if (sdm) {
            predictRankAggregated(selectedSong.value._id).then(res => {
                setRankList(res);
                setRankPending(false);
            }).catch(ex => {
                setRankPending(false);
            })
        }
        else {
            predictRank(selectedSong.value._id).then(res => {
                setRankList(res);
                setRankPending(false);
            }).catch(ex => {
                setRankPending(false);
            })
        }
    }

    return (
        <Grid container spacing={gridSpacing}>
            <Grid item xs={12}>
                {
                    isLoading ? (
                        <SkeletonPopularCard />
                    ) : (
                        <MainCard content={false}>
                            <CardContent>
                                <Grid container spacing={gridSpacing}>
                                    <Grid item xs={12}>
                                        <Grid container alignContent="center" justifyContent="space-between">
                                            <Grid item>
                                                <Typography variant="h4">Rank</Typography>
                                            </Grid>
                                            <Grid item>
                                                <Typography display="inline">
                                                    Per segment
                                                </Typography>
                                                <Switch
                                                    color="primary"
                                                    checked={sdm}
                                                    onChange={(e) => setSdm(e.target.checked)}
                                                    name="sdm"
                                                    size="small"
                                                />
                                            </Grid>
                                        </Grid>
                                    </Grid>
                                    <Grid container item xs={6}>
                                        <Grid item xs={12}>
                                            <Typography>
                                                Select a song from the database to see how it compares to other songs, in terms of similarity.
                                                A green icon next to a result indicates that it may be a cover of the selected song.
                                            </Typography>
                                        </Grid>
                                        <Grid item xs={12} sx={{ pt: 2 }}>
                                            <Typography variant="h5">
                                                Pick song
                                            </Typography>
                                        </Grid>
                                        <Grid container item xs={12} alignItems="center">
                                            <Grid item xs={6} sx={{ mr: 2, mt: 2, mb: 2 }}>
                                                <ComboBox options={songList} value={song} setValue={setSong} />
                                            </Grid>
                                            <Grid item xs>
                                                {!rankPending ?
                                                    (<AnimateButton>
                                                        <Button sx={{ p: 1, pl: 10, pr: 10 }}
                                                            color="secondary"
                                                            variant="contained"
                                                            disableElevation
                                                            onClick={() => handleRank(song)}>
                                                            Rank
                                                        </Button>
                                                    </AnimateButton>) :
                                                    (<Stack alignItems="center">
                                                        <CircularProgress color="secondary" />
                                                    </Stack>)
                                                }
                                            </Grid>
                                        </Grid>
                                    </Grid>
                                    <Divider />
                                    <Grid container item xs={12}>
                                        {rankList.map(it => <RankItem song={it} />)}
                                    </Grid>
                                </Grid>
                            </CardContent>
                        </MainCard>
                    )
                }
            </Grid>
            {/* <Grid item xs={12}>
                <Microphone />
            </Grid> */}
        </Grid>
    )
}

export default Rank;