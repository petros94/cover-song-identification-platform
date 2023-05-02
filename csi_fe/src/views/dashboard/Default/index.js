import { useEffect, useState } from 'react';

// material-ui
import { Grid } from '@mui/material';

// project imports
import SongsCountCard from './SongsCountCard';
import CompareCoversCard from './CompareCoversCard';
import UploadSongsCard from './UploadSongsCard';
import TotalIncomeDarkCard from './TotalIncomeDarkCard';
import TotalIncomeLightCard from './TotalIncomeLightCard';
import TotalGrowthBarChart from './TotalGrowthBarChart';
import { gridSpacing } from 'store/constant';
import { getAllSongs } from 'networking';

// ==============================|| DEFAULT DASHBOARD ||============================== //

const Dashboard = () => {
    const [isLoading, setLoading] = useState(true);
    const [songList, setSongList] = useState([]);

    useEffect(() => {
        getAllSongs().then(res => {
            let options = res.map(it => ({ label: it.title, value: it }));
            setSongList(options);
            setLoading(false);
        }).catch(res => {
            setLoading(false);
        })
    }, [])

    return (
        <Grid container spacing={gridSpacing}>
            <Grid item xs={12}>
                <Grid container spacing={gridSpacing}>
                    <Grid item lg={4} md={6} sm={6} xs={12}>
                        <SongsCountCard isLoading={isLoading} />
                    </Grid>
                    <Grid item lg={4} md={6} sm={6} xs={12}>
                        <UploadSongsCard isLoading={isLoading} setSongList={setSongList} />
                    </Grid>
                    {/* <Grid item lg={4} md={12} sm={12} xs={12}>
                        <Grid container spacing={gridSpacing}>
                            <Grid item sm={6} xs={12} md={6} lg={12}>
                                <TotalIncomeDarkCard isLoading={isLoading} />
                            </Grid>
                            <Grid item sm={6} xs={12} md={6} lg={12}>
                                <TotalIncomeLightCard isLoading={isLoading} />
                            </Grid>
                        </Grid>
                    </Grid> */}
                </Grid>
            </Grid>
            <Grid item xs={12} md={8}>
                <CompareCoversCard isLoading={isLoading} songList={songList} />
            </Grid>
            {/* <Grid item xs={12}>
                <Grid container spacing={gridSpacing}>
                    <Grid item xs={12} md={8}>
                        <TotalGrowthBarChart isLoading={isLoading} />
                    </Grid>
                    <Grid item xs={12} md={4}>
                        <PopularCard isLoading={isLoading} />
                    </Grid>
                </Grid>
            </Grid> */}
        </Grid>
    );
};

export default Dashboard;
