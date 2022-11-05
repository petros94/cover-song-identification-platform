// assets
import { IconMusic, IconSortDescending } from '@tabler/icons';

// constant
const icons = { IconMusic, IconSortDescending };

// ==============================|| DASHBOARD MENU ITEMS ||============================== //

const songs = {
    id: 'songs',
    title: 'Songs',
    type: 'group',
    children: [
        {
            id: 'default2',
            title: 'Songs',
            type: 'item',
            url: '/dashboard/default',
            icon: icons.IconMusic,
            breadcrumbs: false
        },
        {
            id: 'default22',
            title: 'Rank',
            type: 'item',
            url: '/songs/rank',
            icon: icons.IconSortDescending,
            breadcrumbs: false
        }
    ]
};

export default songs;
