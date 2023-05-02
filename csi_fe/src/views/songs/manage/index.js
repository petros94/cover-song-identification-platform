import React from 'react'
import { Avatar, Button, CardActions, CardContent, Divider, Grid, Menu, Stack, Typography, Switch } from '@mui/material';

import MainCard from 'ui-component/cards/MainCard';

import { gridSpacing } from 'store/constant';
import SongTable from 'views/songs/manage/songTable'


const ManageSongs = () => {
    return (
        <Grid container spacing={gridSpacing}>
            <Grid item xs={12}>
                <MainCard content={false}>
                    <CardContent>
                        <Grid container spacing={gridSpacing}>
                            <Grid item xs={12}>
                                <Typography variant="h4">Songs</Typography>
                            </Grid>
                            <Grid item xs={8}>
                                <Typography>
                                    The following is a list of all the songs stored in database. Add new songs using the YouTube widget in the Home page.
                                    Also check out the Rank page, where you can select a song from database and see potential cover songs.
                                </Typography>
                            </Grid>
                            <Grid item xs={12}>
                                <SongTable />
                            </Grid>
                        </Grid>
                    </CardContent>
                </MainCard>
            </Grid>
        </Grid>
    )
}

export default ManageSongs;