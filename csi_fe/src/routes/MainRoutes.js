import { lazy } from 'react';

// project imports
import MainLayout from 'layout/MainLayout';
import Loadable from 'ui-component/Loadable';

// dashboard routing
const DashboardDefault = Loadable(lazy(() => import('views/dashboard/Default')));
const SongsRank = Loadable(lazy(() => import('views/songs/rank')));
const ManageSongs = Loadable(lazy(() => import('views/songs/manage')));


// ==============================|| MAIN ROUTING ||============================== //

const MainRoutes = {
    path: '/',
    element: <MainLayout />,
    children: [
        {
            path: '/',
            element: <DashboardDefault />
        },
        {
            path: 'dashboard',
            children: [
                {
                    path: 'default',
                    element: <DashboardDefault />
                }
            ]
        },
        {
            path: 'songs',
            children: [
                {
                    path: 'rank',
                    element: <SongsRank />
                },
                {
                    path: 'manage',
                    element: <ManageSongs />
                }
            ]
        }
    ]
};

export default MainRoutes;
