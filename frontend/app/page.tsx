"use client"

import { useState } from "react"
import { ContextForm } from "@/components/context-form"
import { VideoSearch } from "@/components/video-search"
import { VideoDetail } from "@/components/video-detail"

export default function Home() {
  const [userContext, setUserContext] = useState<{
    age: string
    education: string
    interests: string[]
    learningGoal: string
  } | null>(null)

  const [selectedVideo, setSelectedVideo] = useState<any>(null)

  const handleContextSubmit = (context: {
    age: string
    education: string
    interests: string[]
    learningGoal: string
  }) => {
    setUserContext(context)
  }

  const handleReset = () => {
    setUserContext(null)
    setSelectedVideo(null)
  }

  const handleVideoSelect = (video: any) => {
    setSelectedVideo(video)
  }

  const handleBackToSearch = () => {
    setSelectedVideo(null)
  }

  return (
    <main className="min-h-screen gradient-bg relative overflow-hidden">
      <div className="relative z-10">
        {!userContext ? (
          <ContextForm onSubmit={handleContextSubmit} />
        ) : selectedVideo ? (
          <VideoDetail video={selectedVideo} onBack={handleBackToSearch} />
        ) : (
          <VideoSearch context={userContext} onReset={handleReset} onVideoSelect={handleVideoSelect} />
        )}
      </div>
    </main>
  )
}
