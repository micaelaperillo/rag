import { z } from "zod"
import { Recommendation } from "./Recommendation"

export const RecommendationList = z.object({
    recommendations: z.array(Recommendation),
})