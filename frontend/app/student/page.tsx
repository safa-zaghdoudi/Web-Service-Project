"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Search, Star, Trash2 } from "lucide-react"
import { toast } from "react-hot-toast"
import api from "../../services/api"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import type { Residency, Review } from "@/types"

export default function StudentDashboard() {
  const [residencies, setResidencies] = useState<Residency[]>([])
  const [searchId, setSearchId] = useState("")
  const [application, setApplication] = useState({
    residency_id: "",
    preferred_roommate: "",
    disease_status: "None",
  })
  const [review, setReview] = useState({
    residency_id: "",
    rating: 5,
    review_text: "",
  })
  const [userReviews, setUserReviews] = useState<Review[]>([])
  const router = useRouter()

  useEffect(() => {
    fetchAllResidencies()
    fetchUserReviews()
  }, [])

  const fetchAllResidencies = async () => {
    try {
      const response = await api.get("/residencies")
      setResidencies(response.data)
    } catch (error) {
      toast.error("Failed to fetch residencies")
    }
  }

  const fetchUserReviews = async () => {
    try {
      const response = await api.get("/reviews")
      setUserReviews(response.data)
    } catch (error) {
      toast.error("Failed to fetch reviews")
    }
  }

  const fetchResidencyById = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!searchId) {
      toast.error("Please enter a residency ID")
      return
    }
    try {
      const response = await api.get(`/residencies/${searchId}`)
      setResidencies([response.data])
      toast.success("Residency found")
    } catch (error) {
      toast.error("Residency not found")
    }
  }

  const handleApply = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await api.post("/residencies/apply", application)
      toast.success("Application submitted successfully")
      setApplication({ residency_id: "", preferred_roommate: "", disease_status: "None" })
    } catch (error) {
      toast.error("Failed to submit application")
    }
  }

  const handleReviewSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await api.post("/reviews", review)
      toast.success("Review submitted successfully")
      setReview({ residency_id: "", rating: 5, review_text: "" })
      fetchUserReviews()
    } catch (error) {
      toast.error("Failed to submit review")
    }
  }

  const handleDeleteReview = async (reviewId: string) => {
    try {
      await api.delete(`/reviews/${reviewId}`)
      toast.success("Review deleted successfully")
      fetchUserReviews()
    } catch (error) {
      toast.error("Failed to delete review")
    }
  }

  const handleLogout = () => {
    localStorage.removeItem("token")
    router.push("/")
  }

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Student Dashboard</h1>
        <Button variant="destructive" onClick={handleLogout}>
          Logout
        </Button>
      </div>

      {/* Search Section */}
      <Card>
        <CardHeader>
          <CardTitle>Search Residencies</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={fetchResidencyById} className="space-y-4">
            <div className="flex gap-2">
              <Input placeholder="Enter Residency ID" value={searchId} onChange={(e) => setSearchId(e.target.value)} />
              <Button type="submit">
                <Search className="h-4 w-4 mr-2" />
                Search
              </Button>
            </div>
            <Button type="button" variant="outline" onClick={fetchAllResidencies} className="w-full">
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
                  <TableCell>{residency.Address}</TableCell>
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
                onValueChange={(value: string) =>
                  setApplication((prev) => ({
                    ...prev,
                    residency_id: value,
                  }))
                }
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

            <Button type="submit" className="w-full">
              Submit Application
            </Button>
          </form>
        </CardContent>
      </Card>

      {/* Review Form */}
      <Card>
        <CardHeader>
          <CardTitle>Write a Review</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleReviewSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label>Select Residency</Label>
              <Select
                value={review.residency_id}
                onValueChange={(value: string) =>
                  setReview((prev) => ({
                    ...prev,
                    residency_id: value,
                  }))
                }
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
              <Label>Rating</Label>
              <Select
                value={review.rating.toString()}
                onValueChange={(value: string) =>
                  setReview((prev) => ({
                    ...prev,
                    rating: Number.parseInt(value, 10),
                  }))
                }
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select a rating" />
                </SelectTrigger>
                <SelectContent>
                  {[1, 2, 3, 4, 5].map((rating) => (
                    <SelectItem key={rating} value={rating.toString()}>
                      {rating} {rating === 1 ? "Star" : "Stars"}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label>Review</Label>
              <Textarea
                placeholder="Write your review here..."
                value={review.review_text}
                onChange={(e) => setReview({ ...review, review_text: e.target.value })}
                required
                className="min-h-[100px]"
              />
            </div>

            <Button type="submit" className="w-full">
              Submit Review
            </Button>
          </form>
        </CardContent>
      </Card>

      {/* User Reviews */}
      <Card>
        <CardHeader>
          <CardTitle>Your Reviews</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Residency</TableHead>
                <TableHead>Rating</TableHead>
                <TableHead>Review</TableHead>
                <TableHead>Date</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {userReviews.map((review) => (
                <TableRow key={review._id}>
                  <TableCell>
                    {residencies.find((r) => r._id === review.residency_id)?.Residency || review.residency_id}
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center">
                      {review.rating} <Star className="h-4 w-4 ml-1 fill-yellow-400 text-yellow-400" />
                    </div>
                  </TableCell>
                  <TableCell>{review.review_text}</TableCell>
                  <TableCell>{new Date(review.timestamp).toLocaleDateString()}</TableCell>
                  <TableCell>
                    <Button variant="destructive" size="sm" onClick={() => handleDeleteReview(review._id)}>
                      <Trash2 className="h-4 w-4" />
                    </Button>
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

