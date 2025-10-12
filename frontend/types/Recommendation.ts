import { z } from "zod"

export const Recommendation = z.object({
    video_id: z.string(),
    video_title: z.string(),
    video_date: z.string(),
    video_duration: z.string(),
    playlist_id: z.string(),
    playlist_name: z.string(),
    source: z.string(),
    reason: z.string(),
    level: z.string(),
})