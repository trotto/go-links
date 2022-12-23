import { FC } from 'react'
import styled from '@emotion/styled'
import { TrottoLogo } from '../icons'
import { UserMenu } from './UserMenu'
import useSWR from 'swr'
import { fetcher } from '../utils/fetcher'
import { User } from '../types'

const StyledDiv = styled.div`
  display: flex;
  height: 64px;
  background-color: #f6f8fa;
  justify-content: space-between;
  align-items: center;
  padding: 0 80px;

  font-weight: 500;
  font-size: 24px;
`

const LeftLink = styled.a`
  display: flex;
  align-items: center;
  gap: 8px;
`

const RightContainer = styled.div`
  display: flex;
  align-items: center;
  font-weight: 400;
  font-size: 16px;

  .item {
    margin: 0 12px;
  }
`

interface AdminLink {
  text: string
  url: string
}

interface Props {
  user?: User
}

export const NavBar: FC<Props> = ({ user }) => {
  const { data: adminLinks } = useSWR(`/_admin_links`, fetcher<AdminLink[]>)
  return (
    <StyledDiv>
      <LeftLink className='left' href='/'>
        <div className='logo'>
          <TrottoLogo />
        </div>
        <div>Trotto</div>
      </LeftLink>
      <RightContainer>
        <a className='item' href='/documentation'>
          Documentation
        </a>
        {adminLinks?.map(({ url, text }) => (
          <a className='item' href={url} key={url}>
            {text}
          </a>
        ))}
        <div className='item'>{user && <UserMenu user={user} />}</div>
      </RightContainer>
    </StyledDiv>
  )
}
