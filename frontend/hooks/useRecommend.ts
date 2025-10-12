import { RECOMMEND_ENDPOINT } from "@/api/endpoints"
import { useQuery } from "react-query"

interface RecommendProps {
    query: string
    userPreferences: string
}


const useRecommend = ({ query, userPreferences }: RecommendProps) => {
    return useQuery({
        queryKey: ['recommend'],
        queryFn: () => {
            return fetch(RECOMMEND_ENDPOINT, {
                method: 'POST',
                body: JSON.stringify({ query, userPreferences })
            }).then(res => res.json())
        }
    })
}

export default useRecommend