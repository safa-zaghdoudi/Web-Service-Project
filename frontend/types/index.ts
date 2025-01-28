export interface User {
  username: string
  password: string
  role: "admin" | "student"
  first_name?: string
  last_name?: string
  year_of_study?: string
  university?: string
}

export interface AdminData extends User {
  first_name: string
  last_name: string
}

export interface StudentData extends User {
  first_name: string
  last_name: string
  year_of_study: string
  university: string
}

export interface Residency {
  _id: string
  "Residency-Type": string
  City: string
  Residency: string
  Address: string
  Telephone: string
  Available_transportation: string
}

export interface Application {
  _id: string
  username: string
  residency_id: string
  preferred_roommate: string
  disease_status: string
  status: "pending" | "approved" | "rejected"
}

export interface Review {
  _id: string
  username: string
  residency_id: string
  rating: number
  review_text: string
  timestamp: string
}

