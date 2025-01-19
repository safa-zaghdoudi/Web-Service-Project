'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Search, Edit, Trash2, Plus, Save } from 'lucide-react'
import { toast } from 'react-hot-toast'
import api from '../../services/api'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Label } from "@/components/ui/label"
import type { Residency } from '@/types/residency'

export default function AdminDashboard() {
  const [residencies, setResidencies] = useState<Residency[]>([])
  const [searchId, setSearchId] = useState('')
  const [newResidency, setNewResidency] = useState({
    'Residency-Type': 'Public University Residency',
    City: '',
    Residency: '',
    Address: '',
    Telephone: '',
    Available_transportation: ''
  })
  const [editingId, setEditingId] = useState<string | null>(null)
  const [editForm, setEditForm] = useState({
    'Residency-Type': '',
    City: '',
    Residency: '',
    Address: '',
    Telephone: '',
    Available_transportation: ''
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

  const handleAddResidency = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await api.post('/residencies', newResidency)
      toast.success('Residency added successfully')
      setNewResidency({
        'Residency-Type': 'Public University Residency',
        City: '',
        Residency: '',
        Address: '',
        Telephone: '',
        Available_transportation: ''
      })
      fetchAllResidencies()
    } catch (error) {
      toast.error('Failed to add residency')
    }
  }

  const startEdit = (residency: Residency) => {
    setEditingId(residency._id)
    setEditForm({
      'Residency-Type': residency['Residency-Type'],
      City: residency.City,
      Residency: residency.Residency,
      Address: residency.Address,
      Telephone: residency.Telephone,
      Available_transportation: residency.Available_transportation || ''
    })
  }

  const handleUpdate = async (id: string) => {
    try {
      await api.put(`/residencies/${id}`, editForm)
      toast.success('Residency updated successfully')
      setEditingId(null)
      fetchAllResidencies()
    } catch (error) {
      toast.error('Failed to update residency')
    }
  }

  const handleDelete = async (id: string) => {
    if (!window.confirm('Are you sure you want to delete this residency?')) return
    try {
      await api.delete(`/residencies/${id}`)
      toast.success('Residency deleted successfully')
      fetchAllResidencies()
    } catch (error) {
      toast.error('Failed to delete residency')
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    router.push('/')
  }

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Admin Dashboard</h1>
        <Button variant="destructive" onClick={handleLogout}>Logout</Button>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Search Form */}
        <Card>
          <CardHeader>
            <CardTitle>Search Residency</CardTitle>
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

        {/* Add New Residency Form */}
        <Card>
          <CardHeader>
            <CardTitle>Add New Residency</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleAddResidency} className="space-y-4">
              <div className="space-y-2">
                <Label>City</Label>
                <Input
                  value={newResidency.City}
                  onChange={(e) => setNewResidency({ ...newResidency, City: e.target.value })}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label>Residency Name</Label>
                <Input
                  value={newResidency.Residency}
                  onChange={(e) => setNewResidency({ ...newResidency, Residency: e.target.value })}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label>Address</Label>
                <Input
                  value={newResidency.Address}
                  onChange={(e) => setNewResidency({ ...newResidency, Address: e.target.value })}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label>Telephone</Label>
                <Input
                  value={newResidency.Telephone}
                  onChange={(e) => setNewResidency({ ...newResidency, Telephone: e.target.value })}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label>Available Transportation</Label>
                <Input
                  value={newResidency.Available_transportation}
                  onChange={(e) => setNewResidency({ ...newResidency, Available_transportation: e.target.value })}
                />
              </div>
              <Button type="submit" className="w-full">
                <Plus className="h-4 w-4 mr-2" />
                Add Residency
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>

      {/* Residencies Table */}
      <Card>
        <CardHeader>
          <CardTitle>Residencies List</CardTitle>
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
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {residencies.map((residency) => (
                <TableRow key={residency._id}>
                  <TableCell>
                    {editingId === residency._id ? (
                      <Input
                        value={editForm.Residency}
                        onChange={(e) => setEditForm({ ...editForm, Residency: e.target.value })}
                      />
                    ) : (
                      residency.Residency
                    )}
                  </TableCell>
                  <TableCell>
                    {editingId === residency._id ? (
                      <Input
                        value={editForm.City}
                        onChange={(e) => setEditForm({ ...editForm, City: e.target.value })}
                      />
                    ) : (
                      residency.City
                    )}
                  </TableCell>
                  <TableCell>
                    {editingId === residency._id ? (
                      <Input
                        value={editForm.Address}
                        onChange={(e) => setEditForm({ ...editForm, Address: e.target.value })}
                      />
                    ) : (
                      residency.Address
                    )}
                  </TableCell>
                  <TableCell>
                    {editingId === residency._id ? (
                      <Input
                        value={editForm.Telephone}
                        onChange={(e) => setEditForm({ ...editForm, Telephone: e.target.value })}
                      />
                    ) : (
                      residency.Telephone
                    )}
                  </TableCell>
                  <TableCell>
                    {editingId === residency._id ? (
                      <Input
                        value={editForm.Available_transportation}
                        onChange={(e) => setEditForm({ ...editForm, Available_transportation: e.target.value })}
                      />
                    ) : (
                      residency.Available_transportation
                    )}
                  </TableCell>
                  <TableCell>
                    {editingId === residency._id ? (
                      <div className="flex gap-2">
                        <Button onClick={() => handleUpdate(residency._id)}>Save</Button>
                        <Button variant="outline" onClick={() => setEditingId(null)}>Cancel</Button>
                      </div>
                    ) : (
                      <div className="flex gap-2">
                        <Button variant="outline" onClick={() => startEdit(residency)}>
                          <Edit className="h-4 w-4" />
                        </Button>
                        <Button variant="destructive" onClick={() => handleDelete(residency._id)}>
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}

