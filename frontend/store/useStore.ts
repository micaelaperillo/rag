import { create } from 'zustand'
import { Recommendation } from '@/types/Recommendation';
import { RecommendationList } from '@/types/RecommendationList';

interface UserContext {
  age: string;
  education: string;
  interests: string[];
  learningGoal: string;
}

interface AppState {
  userContext: UserContext | null;
  recommendations: RecommendationList | null;
  selectedVideo: Recommendation | null;
  searchQuery: string;
  hasSearched: boolean;
  setUserContext: (context: UserContext) => void;
  setRecommendations: (recommendations: RecommendationList) => void;
  setSelectedVideo: (video: Recommendation | null) => void;
  setSearchQuery: (query: string) => void;
  setHasSearched: (hasSearched: boolean) => void;
  reset: () => void;
  backToSearch: () => void;
}

export const useStore = create<AppState>((set) => ({
  userContext: null,
  recommendations: null,
  selectedVideo: null,
  searchQuery: "",
  hasSearched: false,
  setUserContext: (context) => set({ userContext: context }),
  setRecommendations: (recommendations) => set({ recommendations }),
  setSelectedVideo: (video) => set({ selectedVideo: video }),
  setSearchQuery: (query) => set({ searchQuery: query }),
  setHasSearched: (hasSearched) => set({ hasSearched }),
  reset: () => set({ userContext: null, selectedVideo: null, recommendations: null, searchQuery: "", hasSearched: false }),
  backToSearch: () => set({ selectedVideo: null }),
}));
