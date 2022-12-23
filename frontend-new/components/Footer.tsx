import styled from '@emotion/styled'
import { FC } from 'react'

import { GithubLogo } from 'app/icons'

const StyledDiv = styled.div`
  display: flex;
  height: 64px;
  background-color: #f6f8fa;
  align-items: center;
  justify-content: center;

  .item {
    margin: 12px;
  }
`

export const Footer: FC = () => {
  return (
    <StyledDiv>
      <div className='item'>
        <a href='https://github.com/trotto/go-links'>
          <GithubLogo />
        </a>
      </div>
      <div className='item'>
        <a href={'/pricing'}>Pricing</a>
      </div>
      <div className='item'>
        <a href={'/privacy'}>Privacy</a>
      </div>
      <div className='item'>
        <a href={'/terms'}>Terms</a>
      </div>
      <div className='item'>
        <a href={'/contact'}>Contact us</a>
      </div>
    </StyledDiv>
  )
}
