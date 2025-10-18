"use client"

import type React from "react"
import { useEffect } from "react"
import { Button } from "@/components/ui/button"
import {
  Search,
  ArrowLeft,
  Play,
  Clock,
  Star,
  TrendingUp,
  Loader2,
  Calendar,
  ExternalLink,
  Sparkles,
} from "lucide-react"
import useRecommend from "@/hooks/useRecommend"
import { generateVideoLinks } from "@/lib/video-utils"
import { useStore } from "@/store/useStore"

interface VideoSearchProps {
  context: {
    age: string
    education: string
    interests: string[]
    job: string
  }
  onReset: () => void
  onVideoSelect: (video: any) => void
}


export function VideoSearch({ context, onReset, onVideoSelect }: VideoSearchProps) {
  const { 
    searchQuery, 
    setSearchQuery, 
    hasSearched, 
    setHasSearched, 
    recommendations, 
    setRecommendations 
  } = useStore()

  // Convert context to user preferences string
  const userPreferences = `${context.age} years old, ${context.education} education level, interested in ${context.interests.join(', ')}, job: ${context.job}`
  
  const { data, isLoading, error, mutate: searchRecommendations } = useRecommend()

  useEffect(() => {
    if (data) {
      setRecommendations(data)
    }
  }, [data, setRecommendations])

  const handleSearch = (e: React.FormEvent | React.KeyboardEvent) => {
    e.preventDefault()
    if (searchQuery.trim()) {
      setHasSearched(true)
      searchRecommendations({
        query: searchQuery,
        user_preferences: userPreferences,
      })
    }
  }

  return (
    <div className="min-h-screen p-4 md:p-8">
      <div className="max-w-7xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-700">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <Button onClick={onReset} variant="ghost" className="glass-card hover:bg-white/10 text-foreground">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Change Personal info
          </Button>

          <div className="glass-card px-4 py-2 rounded-full">
            <p className="text-sm text-muted-foreground">
              Role: <span className="text-foreground font-medium">{context.job}</span>
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
            <div className="glass-card rounded-2xl p-2 flex items-start gap-2 shimmer">
              <Search className="w-5 h-5 text-muted-foreground ml-3 mt-4" />
              <textarea
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    handleSearch(e)
                  }
                }}
                placeholder="Describe hat would you like to learn? (e.g., 'Understand quantum physics basics', 'Improve my Python Skills')"
                className="flex-1 bg-transparent px-2 py-3 text-foreground placeholder:text-muted-foreground focus:outline-none resize-none text-base"
                rows={3}
              />
              <Button
                type="submit"
                className="bg-primary hover:bg-primary/90 text-primary-foreground rounded-xl px-6 shadow-lg shadow-primary/25 self-end mb-1"
                onClick={handleSearch}
              >
                Search
              </Button>
            </div>
          </form>

          {/* Interest Tags */}
          {/* <div className="flex flex-wrap justify-center gap-2 mt-6">
            {context.interests.map((interest) => (
              <button
                key={interest}
                onClick={() => setSearchQuery(interest)}
                className="glass-card px-4 py-2 rounded-full text-sm font-medium text-foreground hover:bg-white/10 transition-all"
              >
                {interest}
              </button>
            ))}
          </div> */}
        </div>

        {/* Results Section */}
        {/* <div className="space-y-6">
          {(isLoading || hasSearched || (recommendations?.recommendations?.length ?? 0) > 0) && (
            <div className="flex items-center gap-2 text-muted-foreground">
              <TrendingUp className="w-5 h-5" />
              <h2 className="text-lg font-medium">
                {hasSearched ? `Results for "${searchQuery}"` : "Recommended for You"}
              </h2>
            </div>
          )} */}

          {isLoading ? (
            <div className="flex flex-col items-center justify-center py-20 text-center">
              <Loader2 className="w-12 h-12 animate-spin text-primary mb-6" />
              <h2 className="text-2xl font-semibold text-foreground mb-2">
                Finding the perfect learning content tailored to you
              </h2>
              <p className="text-muted-foreground">
                Our RAG is analyzing your request and preferences...
              </p>
            </div>
          ) : error ? (
            <div className="glass-card rounded-2xl p-6 text-center">
              <p className="text-red-400 mb-2">Failed to load recommendations</p>
              <p className="text-sm text-muted-foreground">Please try again later</p>
            </div>
          ) : recommendations?.recommendations?.length > 0 ? (
            <div className="space-y-4">
              {recommendations.recommendations.map((recommendation: any, index: number) => {
                const links = generateVideoLinks(recommendation)
                return (
                  <div
                    key={recommendation.video_id}
                    className="glass-card rounded-2xl overflow-hidden hover:scale-[1.02] transition-transform duration-300 cursor-pointer group"
                    style={{ animationDelay: `${index * 100}ms` }}
                    onClick={() => onVideoSelect(recommendation)}
                  >
                    <div className="flex flex-col md:flex-row">
                      {/* Video Card */}
                      <div className="flex-1 p-6">
                        <div className="flex gap-4">
                          {/* Thumbnail */}
                          <div className="relative w-48 h-32 bg-secondary/50 rounded-xl overflow-hidden flex-shrink-0">
                            <img
                              src={links.thumbnailUrl}
                              alt={recommendation.video_title}
                              className="w-full h-full object-cover"
                              onError={(e) => {
                                e.currentTarget.src = "/placeholder.svg"
                              }}
                            />
                            <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                              <div className="w-12 h-12 rounded-full bg-primary/90 flex items-center justify-center">
                                <Play className="w-6 h-6 text-primary-foreground ml-1" />
                              </div>
                            </div>
                            <div className="absolute bottom-2 right-2 glass-card px-2 py-1 rounded text-xs font-medium flex items-center gap-1">
                              <Clock className="w-3 h-3" />
                              {recommendation.video_duration}
                            </div>
                          </div>

                          {/* Video Info */}
                          <div className="flex-1 space-y-3">
                            <h3 className="font-semibold text-foreground text-lg line-clamp-2 text-balance">
                              {recommendation.video_title}
                            </h3>
                            <div className="flex items-center gap-4 text-sm text-muted-foreground">
                              <span>{recommendation.source}</span>
                              <span>•</span>
                              <span>{recommendation.playlist_name}</span>
                              <span>•</span>
                              <span>{recommendation.level}</span>
                            </div>
                            <div className="flex items-center gap-2 text-sm">
                              <Calendar className="w-4 h-4 text-muted-foreground" />
                              <span className="text-muted-foreground">{recommendation.video_date}</span>
                            </div>
                            <div className="flex gap-2">
                              <Button
                                size="sm"
                                variant="outline"
                                className="text-xs"
                                onClick={(e) => {
                                  e.stopPropagation()
                                  window.open(links.videoUrl, "_blank")
                                }}
                              >
                                <ExternalLink className="w-3 h-3 mr-1" />
                                Watch
                              </Button>
                              <Button
                                size="sm"
                                variant="outline"
                                className="text-xs"
                                onClick={(e) => {
                                  e.stopPropagation()
                                  window.open(links.playlistUrl, "_blank")
                                }}
                              >
                                <ExternalLink className="w-3 h-3 mr-1" />
                                Playlist
                              </Button>
                            </div>
                          </div>
                        </div>
                      </div>

                      {/* AI Reasoning */}
                      <div className="md:w-80 p-6 border-l border-white/10 bg-primary/5 relative overflow-hidden">
                        <div className="absolute -right-20 -top-20 w-48 h-48 bg-purple-500/10 rounded-full blur-3xl opacity-50 group-hover:opacity-100 transition-opacity duration-500"></div>
                        <div className="relative z-10 space-y-3">
                          <div className="flex items-center gap-2">
                            <Sparkles className="w-5 h-5 text-purple-400 drop-shadow-[0_0_4px_rgba(192,132,252,0.7)]" />
                            <h4 className="font-semibold text-sm bg-gradient-to-r from-purple-300 to-pink-400 bg-clip-text text-transparent">
                              Why this video is for you
                            </h4>
                          </div>
                          <p className="text-sm text-muted-foreground leading-relaxed">
                            {recommendation.reason}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>
          ) : hasSearched ? (
            <div className="glass-card rounded-2xl p-6 text-center">
              <p className="text-muted-foreground mb-2">No recommendations found</p>
              <p className="text-sm text-muted-foreground">Try adjusting your search terms</p>
            </div>
          ) : null}
        </div>
      </div>
  )
}
