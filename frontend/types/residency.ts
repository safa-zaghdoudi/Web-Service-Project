export interface Residency {
  _id: string
  'Residency-Type': string
  City: string
  Residency: string
  Address: string
  Telephone: string
  Available_transportation: string
}

export interface StudentApplication {
  username: string
  residency_id: string
  preferred_roommate: string
  disease_status: string
  status: 'pending' | 'approved' | 'rejected'
}

export interface User {
  _id: string
  username: string
  password: string
  role: 'admin' | 'student'
}