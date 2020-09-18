import React from 'react';
import Typography from '@material-ui/core/Typography';
import {getConfig} from '../../config/index';


export const SuccessMessage = ({children}) => (
  <div style={{color: getConfig('palette.success')}}>
    {children}
  </div>
);


export const ErrorMessage = ({children}) => (
  <Typography color="error">
    {children}
  </Typography>
);
