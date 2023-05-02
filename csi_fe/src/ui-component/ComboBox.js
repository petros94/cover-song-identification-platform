import React from 'react'
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';


export default function ComboBox({ value, setValue, options }) {
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
    )
}