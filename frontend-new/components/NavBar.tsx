import styled from '@emotion/styled'
import { FC } from 'react'
import useSWR from 'swr'

import { TrottoLogo } from 'app/icons'
import { User } from 'app/types'
import { fetcher } from 'app/utils/fetcher'

import { UserMenu } from './UserMenu'

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
      <LeftLink href='/'>
        <div>
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
