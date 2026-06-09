"use client";

import InterviewBox from "./components/InterviewBox";

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-900 text-white flex items-center justify-center p-6">
      
      <div className="w-full max-w-3xl">
        <h1 className="text-4xl font-bold text-center mb-6">
          🎤 AI Interview Coach
        </h1>

        <p className="text-center text-gray-400 mb-10">
          Practice real interview with AI voice + feedback
        </p>

        <InterviewBox />
      </div>

    </main>
  );
}