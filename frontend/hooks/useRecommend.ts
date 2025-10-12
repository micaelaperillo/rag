import { RECOMMEND_ENDPOINT } from "@/api/endpoints"
import { RecommendationList } from "@/types/RecommendationList"
import { useMutation, UseMutationResult } from "react-query"
import { z } from "zod"

interface RecommendProps {
    query: string
    user_preferences: string
}

const baseUrl = process.env.NEXT_PUBLIC_BACKEND_URL


const useRecommend = (): UseMutationResult<z.infer<typeof RecommendationList>, Error, RecommendProps> => {
    return useMutation({
        mutationFn: async ({ query, user_preferences }: RecommendProps) => {
            const response = await fetch(baseUrl+RECOMMEND_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query, user_preferences })
            })
            const data = await response.json()
            return RecommendationList.parse(data)
        }
    })
}

export default useRecommend