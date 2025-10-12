"use client"

import { Button } from "@/components/ui/button"
import { ArrowLeft, Play, Clock, Calendar, List, BookOpen, ExternalLink } from "lucide-react"

interface VideoDetailProps {
  video: {
    video_id: string
    title: string
    description: string
    date: string
    duration: string
    playlist_id: string
    thumbnail: string
    playlist: {
      source: string
      subject: string
      playlist_id: string
    }
  }
  onBack: () => void
}

export function VideoDetail({ video, onBack }: VideoDetailProps) {
  return (
    <div className="min-h-screen p-4 md:p-8">
      <div className="max-w-6xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-700">
        {/* Back Button */}
        <Button onClick={onBack} variant="ghost" className="glass-card hover:bg-white/10 text-foreground mb-6">
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Search
        </Button>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Video Player */}
            <div className="glass-card rounded-2xl overflow-hidden">
              <div className="relative aspect-video bg-secondary/50">
                <img
                  src={video.thumbnail || "/placeholder.svg"}
                  alt={video.title}
                  className="w-full h-full object-cover"
                />
                <div className="absolute inset-0 bg-black/40 flex items-center justify-center cursor-pointer hover:bg-black/30 transition-colors">
                  <div className="w-20 h-20 rounded-full bg-primary/90 flex items-center justify-center hover:scale-110 transition-transform">
                    <Play className="w-10 h-10 text-primary-foreground ml-1" />
                  </div>
                </div>
              </div>
            </div>

            {/* Video Info */}
            <div className="glass-card rounded-2xl p-6 space-y-4">
              <h1 className="text-3xl font-bold text-foreground text-balance">{video.title}</h1>

              <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
                <div className="flex items-center gap-2">
                  <Clock className="w-4 h-4" />
                  <span>{video.duration}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Calendar className="w-4 h-4" />
                  <span>{video.date}</span>
                </div>
                <div className="flex items-center gap-2">
                  <ExternalLink className="w-4 h-4" />
                  <span className="font-mono text-xs">ID: {video.video_id}</span>
                </div>
              </div>

              <div className="pt-4 border-t border-white/10">
                <h2 className="text-lg font-semibold text-foreground mb-2">Description</h2>
                <p className="text-muted-foreground leading-relaxed">{video.description}</p>
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Playlist Info */}
            <div className="glass-card rounded-2xl p-6 space-y-4">
              <div className="flex items-center gap-2 text-primary mb-4">
                <List className="w-5 h-5" />
                <h2 className="text-lg font-semibold">Playlist Information</h2>
              </div>

              <div className="space-y-3">
                <div>
                  <p className="text-xs text-muted-foreground uppercase tracking-wide mb-1">Source</p>
                  <p className="text-foreground font-medium">{video.playlist.source}</p>
                </div>

                <div>
                  <p className="text-xs text-muted-foreground uppercase tracking-wide mb-1">Subject</p>
                  <div className="inline-flex items-center gap-2 glass-input px-3 py-1.5 rounded-lg">
                    <BookOpen className="w-4 h-4 text-accent" />
                    <span className="text-foreground font-medium">{video.playlist.subject}</span>
                  </div>
                </div>

                <div>
                  <p className="text-xs text-muted-foreground uppercase tracking-wide mb-1">Playlist ID</p>
                  <p className="text-foreground font-mono text-sm">{video.playlist.playlist_id}</p>
                </div>
              </div>

              <Button className="w-full mt-4 bg-accent hover:bg-accent/90 text-accent-foreground rounded-xl">
                View Full Playlist
              </Button>
            </div>

            {/* Additional Info */}
            <div className="glass-card rounded-2xl p-6 space-y-3">
              <h3 className="font-semibold text-foreground">Video Details</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Video ID</span>
                  <span className="text-foreground font-mono text-xs">{video.video_id}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Playlist ID</span>
                  <span className="text-foreground font-mono text-xs">{video.playlist_id}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Duration</span>
                  <span className="text-foreground">{video.duration}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Published</span>
                  <span className="text-foreground">{video.date}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
