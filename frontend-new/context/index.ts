import { createContext } from 'react'

import { User } from 'app/types'

export interface AppContext {
  user?: User
}

export const Context = createContext<AppContext>({})
