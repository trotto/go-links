import { FC } from 'react'

import { Link, User } from 'app/types'

import { LinkItem } from './LinkItem'

interface Props {
  links?: Link[]
  user?: User
}

export const LinkList: FC<Props> = ({ links, user }) => {
  return (
    <div>
      {links?.map((link) => (
        <LinkItem key={link.id} link={link} canEdit={user && link.owner === user.email} />
      ))}
    </div>
  )
}
