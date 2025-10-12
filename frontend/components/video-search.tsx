"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Search, ArrowLeft, Play, Clock, Star, TrendingUp } from "lucide-react"

interface VideoSearchProps {
  context: {
    age: string
    education: string
    interests: string[]
    learningGoal: string
  }
  onReset: () => void
  onVideoSelect: (video: any) => void
}

const mockVideos = [
  {
    video_id: "vid_001",
    title: "Introduction to Quantum Mechanics",
    description:
      "Explore the fascinating world of quantum mechanics in this comprehensive introduction. Learn about wave-particle duality, the uncertainty principle, and quantum superposition. Perfect for students beginning their journey into quantum physics.",
    date: "2024-01-15",
    duration: "12:34",
    playlist_id: "pl_physics_101",
    thumbnail: "/quantum-physics-visualization.png",
    views: "1.2M",
    rating: 4.8,
    channel: "Physics Explained",
    playlist: {
      source: "Khan Academy",
      subject: "Physics",
      playlist_id: "pl_physics_101",
    },
  },
  {
    video_id: "vid_002",
    title: "Understanding Neural Networks",
    description:
      "Dive deep into the architecture and functioning of neural networks. This video covers perceptrons, activation functions, backpropagation, and practical applications in modern AI systems.",
    date: "2024-02-20",
    duration: "18:45",
    playlist_id: "pl_ai_fundamentals",
    thumbnail: "/neural-network-diagram.png",
    views: "890K",
    rating: 4.9,
    channel: "AI Academy",
    playlist: {
      source: "MIT OpenCourseWare",
      subject: "Computer Science",
      playlist_id: "pl_ai_fundamentals",
    },
  },
  {
    video_id: "vid_003",
    title: "The History of Ancient Rome",
    description:
      "Journey through the rise and fall of one of history's greatest civilizations. From the founding of Rome to the fall of the Western Empire, discover the politics, culture, and military conquests that shaped the ancient world.",
    date: "2024-01-10",
    duration: "25:12",
    playlist_id: "pl_world_history",
    thumbnail: "/ancient-rome-colosseum.png",
    views: "2.1M",
    rating: 4.7,
    channel: "History Hub",
    playlist: {
      source: "CrashCourse",
      subject: "History",
      playlist_id: "pl_world_history",
    },
  },
  {
    video_id: "vid_004",
    title: "Advanced Calculus Concepts",
    description:
      "Master advanced calculus topics including multivariable calculus, vector calculus, and differential equations. Includes practical examples and problem-solving techniques for engineering and physics applications.",
    date: "2024-03-05",
    duration: "15:20",
    playlist_id: "pl_calculus_advanced",
    thumbnail: "/calculus-equations.jpg",
    views: "650K",
    rating: 4.6,
    channel: "Math Masters",
    playlist: {
      source: "3Blue1Brown",
      subject: "Mathematics",
      playlist_id: "pl_calculus_advanced",
    },
  },
]

export function VideoSearch({ context, onReset, onVideoSelect }: VideoSearchProps) {
  const [searchQuery, setSearchQuery] = useState("")
  const [results, setResults] = useState(mockVideos)

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    console.log("Searching for:", searchQuery, "with context:", context)
    const filtered = mockVideos.filter((video) => video.title.toLowerCase().includes(searchQuery.toLowerCase()))
    setResults(filtered.length > 0 ? filtered : mockVideos)
  }

  return (
    <div className="min-h-screen p-4 md:p-8">
      <div className="max-w-7xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-700">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <Button onClick={onReset} variant="ghost" className="glass-card hover:bg-white/10 text-foreground">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Change Context
          </Button>

          <div className="glass-card px-4 py-2 rounded-full">
            <p className="text-sm text-muted-foreground">
              Learning: <span className="text-foreground font-medium">{context.learningGoal}</span>
            </p>
          </div>
        </div>

        {/* Search Section */}
        <div className="mb-12">
          <div className="text-center mb-8">
            <h1 className="text-5xl md:text-6xl font-bold mb-4 text-balance bg-gradient-to-br from-foreground to-foreground/60 bg-clip-text text-transparent">
              Find Your Perfect Video
            </h1>
            <p className="text-lg text-muted-foreground text-balance">
              Curated educational content tailored for {context.education} level
            </p>
          </div>

          <form onSubmit={handleSearch} className="max-w-3xl mx-auto">
            <div className="glass-card rounded-2xl p-2 flex items-center gap-2 shimmer">
              <Search className="w-5 h-5 text-muted-foreground ml-3" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search for videos on any topic..."
                className="flex-1 bg-transparent px-2 py-3 text-foreground placeholder:text-muted-foreground focus:outline-none"
              />
              <Button
                type="submit"
                className="bg-primary hover:bg-primary/90 text-primary-foreground rounded-xl px-6 shadow-lg shadow-primary/25"
              >
                Search
              </Button>
            </div>
          </form>

          {/* Interest Tags */}
          <div className="flex flex-wrap justify-center gap-2 mt-6">
            {context.interests.map((interest) => (
              <button
                key={interest}
                onClick={() => setSearchQuery(interest)}
                className="glass-card px-4 py-2 rounded-full text-sm font-medium text-foreground hover:bg-white/10 transition-all"
              >
                {interest}
              </button>
            ))}
          </div>
        </div>

        {/* Results Section */}
        <div className="space-y-6">
          <div className="flex items-center gap-2 text-muted-foreground">
            <TrendingUp className="w-5 h-5" />
            <h2 className="text-lg font-medium">
              {searchQuery ? `Results for "${searchQuery}"` : "Recommended for You"}
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {results.map((video, index) => (
              <div
                key={video.video_id}
                onClick={() => onVideoSelect(video)}
                className="glass-card rounded-2xl overflow-hidden hover:scale-105 transition-transform duration-300 cursor-pointer group"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                {/* Thumbnail */}
                <div className="relative aspect-video bg-secondary/50">
                  <img
                    src={video.thumbnail || "/placeholder.svg"}
                    alt={video.title}
                    className="w-full h-full object-cover"
                  />
                  <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                    <div className="w-16 h-16 rounded-full bg-primary/90 flex items-center justify-center">
                      <Play className="w-8 h-8 text-primary-foreground ml-1" />
                    </div>
                  </div>
                  <div className="absolute bottom-2 right-2 glass-card px-2 py-1 rounded text-xs font-medium flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    {video.duration}
                  </div>
                </div>

                {/* Content */}
                <div className="p-4 space-y-3">
                  <h3 className="font-semibold text-foreground line-clamp-2 text-balance">{video.title}</h3>
                  <p className="text-sm text-muted-foreground">{video.channel}</p>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">{video.views} views</span>
                    <div className="flex items-center gap-1 text-accent">
                      <Star className="w-4 h-4 fill-current" />
                      <span className="font-medium">{video.rating}</span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
