import React from 'react';
import Button from '@material-ui/core/Button';


export const PrimaryButton = ({children, style, ...otherProps}) => (
    <Button
        variant="contained"
        color="primary"
        style={Object.assign({color: '#ffffff', fontSize: '14px'}, style || {})}
        {...otherProps}
    >
      {children}
    </Button>
);


export const SecondaryButton = ({children, style, ...otherProps}) => {
  const styles = {
    fontSize: '14px'
  };

  if (otherProps.size === 'small')
    styles.padding = '0';

  if (otherProps.variant === 'contained')
    styles.color = '#ffffff';

  return (
      <Button
          color="secondary"
          style={Object.assign(styles, style || {})}
          {...otherProps}
      >
        {children}
      </Button>
  );
};
