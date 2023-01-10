import { css } from '@emotion/react'

export const globalStyles = css`
  @import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');

  html,
  body {
    padding: 0;
    margin: 0;
    font-family: 'Poppins', sans-serif;
    font-size: 14px;
    line-height: 21px;

    color: #000000;
  }

  * {
    box-sizing: border-box;
  }

  a {
    outline: none;
    text-decoration: none;
    color: #000000;
  }

  p {
    margin: 0;
  }
`
