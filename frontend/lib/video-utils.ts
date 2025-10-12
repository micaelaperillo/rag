/**
 * Utility functions for video-related operations
 */

export interface VideoInfo {
  video_id: string
  video_title: string
  video_date: string
  video_duration: string
  playlist_id: string
  playlist_name: string
  source: string
  reason: string
  level: string
}

/**
 * Generate YouTube video URL from video ID
 */
export function getYouTubeVideoUrl(videoId: string): string {
  return `https://www.youtube.com/watch?v=${videoId}`
}

/**
 * Generate YouTube playlist URL from playlist ID
 */
export function getYouTubePlaylistUrl(playlistId: string): string {
  return `https://www.youtube.com/playlist?list=${playlistId}`
}

/**
 * Generate YouTube embed URL for video player
 */
export function getYouTubeEmbedUrl(videoId: string): string {
  return `https://www.youtube.com/embed/${videoId}?autoplay=0&rel=0&modestbranding=1`
}

/**
 * Generate YouTube thumbnail URL
 */
export function getYouTubeThumbnailUrl(videoId: string, quality: 'default' | 'medium' | 'high' | 'standard' | 'maxres' = 'high'): string {
  const qualityMap = {
    default: 'default',
    medium: 'mqdefault',
    high: 'hqdefault',
    standard: 'sddefault',
    maxres: 'maxresdefault'
  }
  return `https://img.youtube.com/vi/${videoId}/${qualityMap[quality]}.jpg`
}

/**
 * Generate video and playlist links based on source
 */
export function generateVideoLinks(video: VideoInfo) {
  const { video_id, playlist_id, source } = video
  
  // For now, assume all videos are YouTube-based
  // In the future, this could be extended to support other platforms
  return {
    videoUrl: getYouTubeVideoUrl(video_id),
    playlistUrl: getYouTubePlaylistUrl(playlist_id),
    embedUrl: getYouTubeEmbedUrl(video_id),
    thumbnailUrl: getYouTubeThumbnailUrl(video_id, 'high')
  }
}

/**
 * Check if a video ID is a valid YouTube video ID
 */
export function isValidYouTubeVideoId(videoId: string): boolean {
  // YouTube video IDs are typically 11 characters long
  return /^[a-zA-Z0-9_-]{11}$/.test(videoId)
}

/**
 * Extract video ID from YouTube URL
 */
export function extractVideoIdFromUrl(url: string): string | null {
  const regex = /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)/
  const match = url.match(regex)
  return match ? match[1] : null
}
