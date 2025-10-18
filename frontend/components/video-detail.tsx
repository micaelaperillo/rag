"use client";

import { Button } from "@/components/ui/button";
import {
  ArrowLeft,
  Play,
  Clock,
  Calendar,
  List,
  BookOpen,
  ExternalLink,
  Sparkles,
} from "lucide-react";
import { generateVideoLinks } from "@/lib/video-utils";

interface VideoDetailProps {
  video: {
    video_id: string;
    video_title: string;
    video_date: string;
    video_duration: string;
    playlist_id: string;
    playlist_name: string;
    source: string;
    reason: string;
    level: string;
  };
  onBack: () => void;
}

export function VideoDetail({ video, onBack }: VideoDetailProps) {
  const links = generateVideoLinks(video);

  return (
    <div className="min-h-screen p-4 md:p-8">
      <div className="max-w-6xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-700">
        {/* Back Button */}
        <Button
          onClick={onBack}
          variant="ghost"
          className="glass-card hover:bg-white/10 text-foreground mb-6"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Search
        </Button>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Video Player */}
            <div className="glass-card rounded-2xl overflow-hidden">
              <div className="relative aspect-video bg-secondary/50">
                <iframe
                  src={links.embedUrl}
                  title={video.video_title}
                  className="w-full h-full"
                  frameBorder="0"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                  allowFullScreen
                />
              </div>
            </div>

            {/* Video Info */}
            <div className="glass-card rounded-2xl p-6 space-y-4">
              <h1 className="text-3xl font-bold text-foreground text-balance">
                {video.video_title}
              </h1>

              <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
                <div className="flex items-center gap-2">
                  <Clock className="w-4 h-4" />
                  <span>{video.video_duration}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Calendar className="w-4 h-4" />
                  <span>{video.video_date}</span>
                </div>
                <div className="flex items-center gap-2">
                  <ExternalLink className="w-4 h-4" />
                  <span className="font-mono text-xs">
                    ID: {video.video_id}
                  </span>
                </div>
              </div>

              <div className="pt-4 border-t border-white/10">
                <div className="relative z-10 space-y-3">
                  <div className="flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-purple-400 drop-shadow-[0_0_4px_rgba(192,132,252,0.7)]" />
                    <h4 className="font-semibold text-sm bg-gradient-to-r from-purple-300 to-pink-400 bg-clip-text text-transparent">
                      Why this video is for you
                    </h4>
                  </div>
                  <p className="text-sm text-muted-foreground leading-relaxed mb-4">
                    {video.reason}
                  </p>
                </div>

                <div className="flex gap-3">
                  <Button
                    onClick={() => window.open(links.videoUrl, "_blank")}
                    className="bg-primary hover:bg-primary/90 text-primary-foreground"
                  >
                    <ExternalLink className="w-4 h-4 mr-2" />
                    Watch on YouTube
                  </Button>
                  <Button
                    variant="outline"
                    onClick={() => window.open(links.playlistUrl, "_blank")}
                  >
                    <ExternalLink className="w-4 h-4 mr-2" />
                    View Playlist
                  </Button>
                </div>
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
                  <p className="text-xs text-muted-foreground uppercase tracking-wide mb-1">
                    Source
                  </p>
                  <p className="text-foreground font-medium">{video.source}</p>
                </div>

                <div>
                  <p className="text-xs text-muted-foreground uppercase tracking-wide mb-1">
                    Playlist Name
                  </p>
                  <div>
                    <p className="text-foreground font-medium">{video.playlist_name}</p>
                  </div>
                </div>

                <div>
                  <p className="text-xs text-muted-foreground uppercase tracking-wide mb-1">
                    Level
                  </p>
                  <p className="text-foreground font-medium">{video.level}</p>
                </div>
              </div>

              <Button
                className="w-full mt-4 bg-accent hover:bg-accent/90 text-accent-foreground rounded-xl"
                onClick={() => window.open(links.playlistUrl, "_blank")}
              >
                View Full Playlist
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
