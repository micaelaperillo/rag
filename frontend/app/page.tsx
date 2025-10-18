"use client"

import { ContextForm } from "@/components/context-form"
import { VideoSearch } from "@/components/video-search"
import { VideoDetail } from "@/components/video-detail"
import { useStore } from "@/store/useStore"

export default function Home() {
  const { userContext, selectedVideo, setUserContext, setSelectedVideo, reset } = useStore()

  return (
    <main className="min-h-screen gradient-bg relative overflow-hidden">
      <div className="relative z-10">
        {!userContext ? (
          <ContextForm onSubmit={setUserContext} />
        ) : selectedVideo ? (
          <VideoDetail video={selectedVideo} onBack={() => setSelectedVideo(null)} />
        ) : (
          <VideoSearch context={userContext} onReset={reset} onVideoSelect={setSelectedVideo} />
        )}
      </div>
    </main>
  )
}
