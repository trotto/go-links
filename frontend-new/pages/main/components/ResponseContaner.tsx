import { Link } from '../../../types'
import styled from '@emotion/styled'
import { LinkItem } from './LinkItem'

const StyledDiv = styled.div(() => ({
  border: '1px solid',
  borderRadius: '4px',
  '.header': {
    display: 'flex',
    justifyContent: 'center',
    padding: '26px',
    backgroundColor: '#fff',
    fontSize: '20px',
    fontWeight: 600,
  },
}))

export enum ResponseType {
  SUCCESS = 'success',
  ERROR = 'error',
}

interface Props {
  link: Link
  type: ResponseType
  message: string
}

export const ResponseContainer = ({ link, message }: Props) => {
  return (
    <StyledDiv>
      <div className='header'>{message}</div>
      <LinkItem link={link}></LinkItem>
    </StyledDiv>
  )
}
