"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import Image from "next/image"
import { toast } from "react-hot-toast"
import api from "../../services/api"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import type { User } from "@/types"

export default function Register() {
  const [formData, setFormData] = useState<User>({
    username: "",
    password: "",
    role: "student",
    first_name: "",
    last_name: "",
    year_of_study: "",
    university: "",
  })
  const [isLoading, setIsLoading] = useState(false)
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      await api.post("/auth/register", formData)
      toast.success("Registration successful")
      router.push("/")
    } catch (error: any) {
      toast.error(error.response?.data?.message || "Registration failed")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <div className="mx-auto w-32 h-32 relative mb-4">
            <Image
              src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-JvGvbn4V0MsyR9YoIFFBCTWWttelQq.png"
              alt="Ministry Logo"
              fill
              className="object-contain"
            />
          </div>
          <CardTitle className="text-2xl">Register</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="username">Username</Label>
              <Input
                id="username"
                type="text"
                required
                value={formData.username}
                onChange={(e) => setFormData({ ...formData, username: e.target.value })}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                required
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="role">Role</Label>
              <Select
                value={formData.role}
                onValueChange={(value: "admin" | "student") => {
                  setFormData({
                    username: formData.username,
                    password: formData.password,
                    role: value,
                    first_name: "",
                    last_name: "",
                    year_of_study: "",
                    university: "",
                  })
                }}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select your role" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="student">Student</SelectItem>
                  <SelectItem value="admin">Administrator</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="first_name">First Name</Label>
              <Input
                id="first_name"
                type="text"
                required
                value={formData.first_name || ""}
                onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="last_name">Last Name</Label>
              <Input
                id="last_name"
                type="text"
                required
                value={formData.last_name || ""}
                onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
              />
            </div>

            {formData.role === "student" && (
              <>
                <div className="space-y-2">
                  <Label htmlFor="year_of_study">Year of Study</Label>
                  <Input
                    id="year_of_study"
                    type="text"
                    required
                    value={formData.year_of_study || ""}
                    onChange={(e) => setFormData({ ...formData, year_of_study: e.target.value })}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="university">University</Label>
                  <Input
                    id="university"
                    type="text"
                    required
                    value={formData.university || ""}
                    onChange={(e) => setFormData({ ...formData, university: e.target.value })}
                  />
                </div>
              </>
            )}

            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading ? "Registering..." : "Register"}
            </Button>

            <div className="text-center mt-4">
              <Link href="/" className="text-sm text-blue-600 hover:text-blue-800">
                Already have an account? Login
              </Link>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

