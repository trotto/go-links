export interface Link {
  created: string
  destination_url: string
  id: number
  mine: boolean
  modified: string 
  namespace?: string
  owner: string
  shortpath: string
  type?: string
  visits_count: number
}

export interface LinkCreateResponse extends Link {
  error: string
}

export interface LinkCreate {
  namespace: string
  shortpath: string
  destination: string
}

export interface LinkUpdate {
  destination: string
}
