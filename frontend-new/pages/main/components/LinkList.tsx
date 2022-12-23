import { Link, User } from 'types'

import { LinkItem } from './LinkItem'

interface Props {
  links?: Link[]
  user?: User
}

export const LinkList = ({ links, user }: Props) => {
  return (
    <div>
      {links?.map((link) => (
        <LinkItem key={link.id} link={link} canEdit={user && link.owner === user.email} />
      ))}
    </div>
  )
}
