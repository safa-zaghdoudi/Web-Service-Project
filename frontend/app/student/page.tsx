'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Search } from 'lucide-react'
import { toast } from 'react-hot-toast'
import api from '../../services/api'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import type { Residency } from '@/types/residency'

export default function StudentDashboard() {
  const [residencies, setResidencies] = useState<Residency[]>([])
  const [searchId, setSearchId] = useState('')
  const [application, setApplication] = useState({
    residency_id: '',
    preferred_roommate: '',
    disease_status: 'None'
  })
  const router = useRouter()

  useEffect(() => {
    fetchAllResidencies()
  }, [])

  const fetchAllResidencies = async () => {
    try {
      const response = await api.get('/residencies')
      setResidencies(response.data)
      toast.success('Residencies fetched successfully')
    } catch (error) {
      toast.error('Failed to fetch residencies')
    }
  }

  const fetchResidencyById = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!searchId) {
      toast.error('Please enter a residency ID')
      return
    }
    try {
      const response = await api.get(`/residencies/${searchId}`)
      setResidencies([response.data])
      toast.success('Residency found')
    } catch (error) {
      toast.error('Residency not found')
    }
  }

  const handleApply = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await api.post('/residencies/apply', application)
      toast.success('Application submitted successfully')
      setApplication({ residency_id: '', preferred_roommate: '', disease_status: 'None' })
    } catch (error) {
      toast.error('Failed to submit application')
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    router.push('/')
  }

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Student Dashboard</h1>
        <Button variant="destructive" onClick={handleLogout}>Logout</Button>
      </div>

      {/* Search Section */}
      <Card>
        <CardHeader>
          <CardTitle>Search Residencies</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={fetchResidencyById} className="space-y-4">
            <div className="flex gap-2">
              <Input
                placeholder="Enter Residency ID"
                value={searchId}
                onChange={(e) => setSearchId(e.target.value)}
              />
              <Button type="submit">
                <Search className="h-4 w-4 mr-2" />
                Search
              </Button>
            </div>
            <Button 
              type="button" 
              variant="outline" 
              onClick={fetchAllResidencies}
              className="w-full"
            >
              Show All Residencies
            </Button>
          </form>
        </CardContent>
      </Card>

      {/* Residencies Table */}
      <Card>
        <CardHeader>
          <CardTitle>Available Residencies</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Residency Name</TableHead>
                <TableHead>City</TableHead>
                <TableHead>Address</TableHead>
                <TableHead>Telephone</TableHead>
                <TableHead>Transportation</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {residencies.map((residency) => (
                <TableRow key={residency._id}>
                  <TableCell>{residency.Residency}</TableCell>
                  <TableCell>{residency.City}</TableCell>
                  <TableCell>{residency.Adress}</TableCell>
                  <TableCell>{residency.Telephone}</TableCell>
                  <TableCell>{residency.Available_transportation}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* Application Form */}
      <Card>
        <CardHeader>
          <CardTitle>Apply for Residency</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleApply} className="space-y-4">
            <div className="space-y-2">
              <Label>Select Residency</Label>
              <Select
                value={application.residency_id}
                onValueChange={(value) => setApplication({ ...application, residency_id: value })}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select a residency" />
                </SelectTrigger>
                <SelectContent>
                  {residencies.map((residency) => (
                    <SelectItem key={residency._id} value={residency._id}>
                      {residency.Residency} - {residency.City}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label>Preferred Roommate</Label>
              <Input
                placeholder="Enter preferred roommate's name (optional)"
                value={application.preferred_roommate}
                onChange={(e) => setApplication({ ...application, preferred_roommate: e.target.value })}
              />
            </div>

            <div className="space-y-2">
              <Label>Disease Status</Label>
              <Input
                placeholder="Enter any health conditions (or 'None')"
                value={application.disease_status}
                onChange={(e) => setApplication({ ...application, disease_status: e.target.value })}
                required
              />
            </div>

            <Button type="submit" className="w-full">Submit Application</Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

