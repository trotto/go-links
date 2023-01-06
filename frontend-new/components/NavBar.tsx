import { FC } from 'react'
import styled from '@emotion/styled'
import { TrottoLogo } from '../icons'
import { UserMenu } from './UserMenu'
import useSWR from 'swr'
import { fetcher } from '../utils/fetcher'

const StyledDiv = styled.div`
  display: flex;
  height: 64px;
  background-color: #f6f8fa;
  justify-content: space-between;
  align-items: center;
  padding: 0 80px;

  font-weight: 500;
  font-size: 24px;

  .left {
    display: flex;

    .logo {
      margin-right: 8px;
    }
  }

  .right {
    display: flex;
    align-items: center;
    font-weight: 400;
    font-size: 16px;

    .item {
      margin: 0 12px;
    }
  }
`

interface AdminLink {
  text: string
  url: string
}

export const NavBar: FC = () => {
  const { data: adminLinks } = useSWR(`/_admin_links`, fetcher<AdminLink[]>)
  return (
    <StyledDiv>
      <a className='left' href='/'>
        <div className='logo'>
          <TrottoLogo />
        </div>
        <div>Trotto</div>
      </a>
      <div className='right'>
        <a className='item' href='/documentation'>
          Documentation
        </a>
        {adminLinks?.map(({ url, text }) => (
          <a className='item' href={url} key={url}>
            {text}
          </a>
        ))}
        <div className='item'>
          <UserMenu />
        </div>
      </div>
    </StyledDiv>
  )
}
