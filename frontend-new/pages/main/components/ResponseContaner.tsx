import { Link } from '../../../types'
import styled from '@emotion/styled'
import { LinkItem } from './LinkItem'

const StyledDiv = styled.div`
  margin-top: 24px;
  .header {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;

    height: 80px;
    border: 1px solid #dedede;

    font-weight: 700;
    font-size: 16px;
    line-height: 24px;
  }
`

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
