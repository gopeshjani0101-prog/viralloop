import React from 'react';
import { Brain, Sparkles, TrendingUp, Zap, CheckCircle2, History } from 'lucide-react';

export default function LearningMemory({ insights }) {
  return (
    <div className="space-y-6">
      {/* Header Explainer */}
      <div className="rounded-2xl border border-purple-500/30 bg-gradient-to-r from-purple-950/40 via-slate-900 to-indigo-950/30 p-6 backdrop-blur-xl">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2.5 rounded-xl bg-purple-600 text-white shadow-lg shadow-purple-600/30">
            <Brain className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-xl font-extrabold text-white tracking-wide">
              Agent Evolutionary Memory (Reinforcement Loop)
            </h2>
            <p className="text-xs text-slate-400">
              How Gemma 4 learns from real video analytics to optimize hooks, pacing, and retention for every new Short
            </p>
          </div>
        </div>

        <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
          <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
            <div className="font-bold text-purple-300 flex items-center gap-1.5 mb-1">
              <Zap className="w-3.5 h-3.5" />
              <span>1. Measure Retention</span>
            </div>
            <p className="text-slate-400">
              Monitors 0-3s swipe rate, average completion %, and comment debates for each posted video.
            </p>
          </div>

          <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
            <div className="font-bold text-pink-300 flex items-center gap-1.5 mb-1">
              <Sparkles className="w-3.5 h-3.5" />
              <span>2. Gemma 4 Reflection</span>
            </div>
            <p className="text-slate-400">
              Local LLM reflects on script nuances vs channel history to derive actionable tactical rules.
            </p>
          </div>

          <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
            <div className="font-bold text-emerald-300 flex items-center gap-1.5 mb-1">
              <TrendingUp className="w-3.5 h-3.5" />
              <span>3. Dynamic System Prompt</span>
            </div>
            <p className="text-slate-400">
              Heuristics are automatically injected into future generation prompts to compound viral success.
            </p>
          </div>
        </div>
      </div>

      {/* Rules List */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <History className="w-4 h-4 text-purple-400" />
            <h3 className="font-bold text-sm text-slate-200">
              Active Viral Rules & Evolutionary Memory ({insights.length})
            </h3>
          </div>
          <span className="text-xs text-slate-500 font-mono">Sorted by discovery order</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {insights.map((insight, idx) => (
            <div
              key={insight.id || idx}
              className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-purple-500/40 transition-all flex flex-col justify-between space-y-4 group"
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[11px] font-mono font-bold px-2.5 py-0.5 rounded-md bg-purple-950 border border-purple-800/80 text-purple-300">
                    Iteration #{insight.iteration}
                  </span>
                  <span className="text-[11px] font-semibold px-2 py-0.5 rounded-md bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 flex items-center gap-1">
                    <TrendingUp className="w-3 h-3" />
                    {insight.metric_improvement}
                  </span>
                </div>

                <h4 className="font-bold text-base text-white group-hover:text-purple-300 transition-colors">
                  {insight.rule_name}
                </h4>

                <p className="text-xs text-slate-300 mt-2 leading-relaxed">
                  {insight.rule_description}
                </p>
              </div>

              {/* Injected Prompt Snippet */}
              <div className="pt-3 border-t border-slate-800/80">
                <div className="text-[10px] font-mono font-bold uppercase tracking-wider text-slate-500 mb-1">
                  Active Prompt Rule:
                </div>
                <div className="text-[11px] font-mono text-purple-300/90 bg-slate-950/80 p-2.5 rounded-lg border border-slate-800/80">
                  {insight.applied_prompt_snippet}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
