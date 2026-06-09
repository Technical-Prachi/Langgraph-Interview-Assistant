"use client";

import { useState } from "react";

export default function InterviewBox() {
  const [role, setRole] = useState("");
  const [question, setQuestion] = useState("");
  const [history, setHistory] = useState<any[]>([]);
  const [interviewComplete, setInterviewComplete] = useState(false);
  const [sessionId, setSessionId] = useState("");
  const [report, setReport] = useState<any>(null);

  const speak = (text: string) => {
    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = "en-US";
    window.speechSynthesis.speak(speech);
  };

  // ---------------------
  // START INTERVIEW
  // ---------------------

  const startInterview = async () => {
    setHistory([]);
    setInterviewComplete(false);
    setReport(null);

    const res = await fetch(
      "http://127.0.0.1:8000/start",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          role,
        }),
      }
    );

    const data = await res.json();

    setSessionId(data.session_id);
    setQuestion(data.question);

    speak(data.question);
  };

  // ---------------------
  // ANSWER QUESTION
  // ---------------------

  const startAnswering = () => {
    const SpeechRecognition =
      (window as any).SpeechRecognition ||
      (window as any).webkitSpeechRecognition;

    const recognition = new SpeechRecognition();

    recognition.lang = "en-US";

    recognition.onresult = async (event: any) => {
      const userAnswer =
        event.results[0][0].transcript;

      const res = await fetch(
        "http://127.0.0.1:8000/evaluate",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            session_id: sessionId,
            question,
            answer: userAnswer,
          }),
        }
      );

      const data = await res.json();

      setHistory((prev) => [
        ...prev,
        {
          question,
          answer: userAnswer,
          score: data.score,
          feedback: data.feedback,
          improvement: data.improvement,
        },
      ]);

      // Interview Complete
      if (data.interview_complete) {
        setInterviewComplete(true);
        setReport(data.report);
        setQuestion("");

        speak("Interview Complete");

        return;
      }

      // Next Question from LangGraph
      setQuestion(data.question);

      if (data.question) {
        speak(data.question);
      }
    };

    recognition.start();
  };

  return (
    <div className="bg-white/10 backdrop-blur-xl p-6 rounded-2xl border border-white/20">

      {/* ROLE INPUT */}

      <input
        className="w-full p-3 rounded-xl bg-white text-black border"
        placeholder="Backend Developer / Frontend Developer / Python Developer"
        value={role}
        onChange={(e) => setRole(e.target.value)}
      />

      <button
        onClick={startInterview}
        className="w-full mt-4 bg-blue-600 hover:bg-blue-700 p-3 rounded-xl"
      >
        Start Interview 🚀
      </button>

      {/* CURRENT QUESTION */}

      {question && (
        <div className="mt-6 bg-black/30 p-4 rounded-xl">

          <h2 className="text-green-400 font-bold text-lg">
            Current Question
          </h2>

          <p className="mt-2">
            {question}
          </p>

          <button
            onClick={startAnswering}
            className="mt-4 bg-red-500 hover:bg-red-600 p-3 rounded-xl"
          >
            🎤 Answer Now
          </button>

        </div>
      )}

      {/* HISTORY */}

      {history.map((item, index) => (
        <div
          key={index}
          className="mt-6 bg-black/40 p-5 rounded-xl border border-gray-700"
        >

          <h2 className="text-green-400 font-bold text-lg">
            Q{index + 1}
          </h2>

          <p className="mt-2">
            {item.question}
          </p>

          <h3 className="text-yellow-400 mt-4 font-semibold">
            Answer
          </h3>

          <p>
            {item.answer}
          </p>

          <h3 className="text-blue-400 mt-4 font-semibold">
            Feedback
          </h3>

          <div className="whitespace-pre-wrap">
            {item.feedback}
          </div>

          <p className="mt-3">
            <strong>Score:</strong>{" "}
            {item.score}
          </p>

          <div className="mt-2">
            <strong>Improvement:</strong>
            <div className="whitespace-pre-wrap">
              {item.improvement}
            </div>
          </div>

        </div>
      ))}

      {/* INTERVIEW COMPLETE */}

      {interviewComplete && (
        <>
          <div className="mt-8 bg-green-600 p-4 rounded-xl text-center font-bold text-xl">
            🎉 Interview Complete
          </div>

          {report && (
            <div className="mt-6 bg-black/40 p-5 rounded-xl">

              <h2 className="text-2xl font-bold text-green-400">
                Final Report
              </h2>

              <p className="mt-3">
                <strong>Overall Score:</strong>{" "}
                {report.overall_score}
              </p>

              <div className="mt-5">

                <h3 className="text-blue-400 font-semibold">
                  Strengths
                </h3>

                {report.strengths?.map(
                  (
                    item: string,
                    index: number
                  ) => (
                    <p key={index}>
                      ✅ {item}
                    </p>
                  )
                )}

              </div>

              <div className="mt-5">

                <h3 className="text-red-400 font-semibold">
                  Weaknesses
                </h3>

                {report.weaknesses?.map(
                  (
                    item: string,
                    index: number
                  ) => (
                    <p key={index}>
                      ❌ {item}
                    </p>
                  )
                )}

              </div>

            </div>
          )}
        </>
      )}

    </div>
  );
}