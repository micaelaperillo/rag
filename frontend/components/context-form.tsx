"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Sparkles, GraduationCap, Target } from "lucide-react"

interface ContextFormProps {
  onSubmit: (context: {
    age: string
    education: string
    interests: string[]
    learningGoal: string
  }) => void
}

const educationLevels = [
  "Elementary School",
  "Middle School",
  "High School",
  "Undergraduate",
  "Graduate",
  "Professional",
]

const interestOptions = [
  "Science",
  "Mathematics",
  "History",
  "Literature",
  "Technology",
  "Arts",
  "Music",
  "Languages",
  "Business",
  "Health",
]

export function ContextForm({ onSubmit }: ContextFormProps) {
  const [age, setAge] = useState("")
  const [education, setEducation] = useState("")
  const [interests, setInterests] = useState<string[]>([])
  const [learningGoal, setLearningGoal] = useState("")

  const toggleInterest = (interest: string) => {
    setInterests((prev) => (prev.includes(interest) ? prev.filter((i) => i !== interest) : [...prev, interest]))
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (age && education && interests.length > 0 && learningGoal) {
      onSubmit({ age, education, interests, learningGoal })
    }
  }

  const isValid = age && education && interests.length > 0 && learningGoal

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-2xl animate-in fade-in slide-in-from-bottom-4 duration-700">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full glass-card mb-4">
            <Sparkles className="w-8 h-8 text-primary" />
          </div>
          <h1 className="text-5xl font-bold mb-3 text-balance bg-gradient-to-br from-foreground to-foreground/60 bg-clip-text text-transparent">
            Discover Your Learning Path
          </h1>
          <p className="text-lg text-muted-foreground text-balance">
            Tell us about yourself to get personalized educational content
          </p>
        </div>

        {/* Form Card */}
        <form onSubmit={handleSubmit} className="glass-card rounded-3xl p-8 space-y-8">
          {/* Age Input */}
          <div className="space-y-3">
            <Label htmlFor="age" className="text-base font-medium flex items-center gap-2">
              <GraduationCap className="w-5 h-5 text-primary" />
              Age
            </Label>
            <input
              id="age"
              type="number"
              min="5"
              max="100"
              value={age}
              onChange={(e) => setAge(e.target.value)}
              placeholder="Enter your age"
              className="w-full px-4 py-3 rounded-xl glass-input text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all"
            />
          </div>

          {/* Education Level */}
          <div className="space-y-3">
            <Label className="text-base font-medium">Education Level</Label>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {educationLevels.map((level) => (
                <button
                  key={level}
                  type="button"
                  onClick={() => setEducation(level)}
                  className={`px-4 py-3 rounded-xl text-sm font-medium transition-all ${
                    education === level
                      ? "bg-primary text-primary-foreground shadow-lg shadow-primary/25"
                      : "glass-input text-foreground hover:bg-white/10"
                  }`}
                >
                  {level}
                </button>
              ))}
            </div>
          </div>

          {/* Interests */}
          <div className="space-y-3">
            <Label className="text-base font-medium">
              Interests <span className="text-muted-foreground text-sm">(Select multiple)</span>
            </Label>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {interestOptions.map((interest) => (
                <button
                  key={interest}
                  type="button"
                  onClick={() => toggleInterest(interest)}
                  className={`px-4 py-3 rounded-xl text-sm font-medium transition-all ${
                    interests.includes(interest)
                      ? "bg-accent text-accent-foreground shadow-lg shadow-accent/25"
                      : "glass-input text-foreground hover:bg-white/10"
                  }`}
                >
                  {interest}
                </button>
              ))}
            </div>
          </div>

          {/* Learning Goal */}
          <div className="space-y-3">
            <Label htmlFor="goal" className="text-base font-medium flex items-center gap-2">
              <Target className="w-5 h-5 text-primary" />
              Learning Goal
            </Label>
            <textarea
              id="goal"
              value={learningGoal}
              onChange={(e) => setLearningGoal(e.target.value)}
              placeholder="What would you like to learn? (e.g., 'Understand quantum physics basics' or 'Improve my Spanish speaking skills')"
              rows={3}
              className="w-full px-4 py-3 rounded-xl glass-input text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all resize-none"
            />
          </div>

          {/* Submit Button */}
          <Button
            type="submit"
            disabled={!isValid}
            className="w-full py-6 text-lg font-semibold rounded-xl bg-primary hover:bg-primary/90 text-primary-foreground shadow-lg shadow-primary/25 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            Continue to Search
          </Button>
        </form>
      </div>
    </div>
  )
}
