// assets
import { IconPolygon } from '@tabler/icons';

// constant
const icons = { IconPolygon };

// ==============================|| DASHBOARD MENU ITEMS ||============================== //

const model = {
    id: 'model',
    title: 'Model',
    type: 'group',
    children: [
        {
            id: 'default3',
            title: 'Model',
            type: 'item',
            url: '/dashboard/default',
            icon: icons.IconPolygon,
            breadcrumbs: false
        }
    ]
};

export default model;
