import React from 'react';
import {getConfig} from '../../config/index';


export const SuccessMessage = ({children}) => (
  <div style={{color: getConfig('palette.success')}}>
    {children}
  </div>
);


export const ErrorMessage = ({children}) => (
  <div style={{color: getConfig('palette.error')}}>
    {children}
  </div>
);
