import { Link } from '../../../types'
import { LinkItem } from './LinkItem'

interface Props {
  links?: Link[]
}

export const LinkList = ({ links }: Props) => {
  return (
    <div>
      {links?.map((link) => (
        <LinkItem key={link.id} link={link} />
      ))}
    </div>
  )
}
