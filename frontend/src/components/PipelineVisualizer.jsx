import React, { useState } from 'react';
import { 
  Globe, 
  Brain, 
  Mic, 
  Film, 
  Share2, 
  CheckCircle2, 
  Clock, 
  AlertCircle, 
  Terminal, 
  Send,
  Sparkles
} from 'lucide-react';

const STAGES = [
  { id: 'Discovery', label: '1. Discovery', desc: 'Reddit & Trends Scanner', icon: Globe },
  { id: 'LLM Reasoning', label: '2. Gemma 4 Brain', desc: 'Hook & Script Virality', icon: Brain },
  { id: 'Asset Generation', label: '3. Neural Voice', desc: 'Edge-TTS & 9:16 Assets', icon: Mic },
  { id: 'Video Editing', label: '4. Video Compositor', desc: '1080x1920 Burned Captions', icon: Film },
  { id: 'Publishing', label: '5. Shorts & Learning', desc: 'YouTube & Heuristic Evolution', icon: Share2 }
];

export default function PipelineVisualizer({ pipelineStatus, onTriggerRun }) {
  const [customTopic, setCustomTopic] = useState('');
  const currentRun = pipelineStatus?.current_run;
  const isRunning = pipelineStatus?.is_running;
  const activeStep = currentRun?.current_step || 'Idle';
  const progress = currentRun?.progress || 0;
  const logs = currentRun?.logs || [];

  const getStepStatus = (stepId, index) => {
    if (!isRunning && currentRun?.status === 'completed') return 'completed';
    if (activeStep === stepId) return 'active';
    
    const stageIndex = STAGES.findIndex(s => s.id === stepId);
    const activeIndex = STAGES.findIndex(s => s.id === activeStep);
    
    if (activeIndex > stageIndex) return 'completed';
    return 'pending';
  };

  const handleCustomTrigger = (e) => {
    e.preventDefault();
    if (isRunning) return;
    onTriggerRun(customTopic.trim() || null);
    setCustomTopic('');
  };

  return (
    <div className="space-y-6">
      {/* Hero Pipeline Visualizer Card */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 backdrop-blur-xl relative overflow-hidden">
        {/* Glow ambient background */}
        <div className="absolute -top-24 -left-24 w-72 h-72 bg-purple-600/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute -bottom-24 -right-24 w-72 h-72 bg-pink-600/10 rounded-full blur-3xl pointer-events-none" />

        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6 relative z-10">
          <div>
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-purple-500 animate-pulse" />
              <h2 className="text-lg font-bold text-white tracking-wide">
                Autonomous Video Creation Pipeline
              </h2>
            </div>
            <p className="text-xs text-slate-400 mt-1">
              End-to-end loop: Trend Ingestion → Gemma 4 Reasoning → Voiceover & Subtitles → YouTube Shorts → Analytics Evolution
            </p>
          </div>

          {/* Quick Custom Topic Input */}
          <form onSubmit={handleCustomTrigger} className="flex items-center gap-2">
            <input
              type="text"
              value={customTopic}
              onChange={(e) => setCustomTopic(e.target.value)}
              placeholder="Inject custom topic or leave blank for auto..."
              disabled={isRunning}
              className="bg-slate-950/80 border border-slate-700/80 rounded-xl px-3.5 py-2 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-purple-500 w-64 md:w-80 transition-all disabled:opacity-50"
            />
            <button
              type="submit"
              disabled={isRunning}
              className="px-3.5 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 disabled:bg-slate-800 disabled:opacity-40 text-white text-xs font-semibold flex items-center gap-1.5 transition-all shadow-md shadow-purple-600/20"
            >
              <Send className="w-3.5 h-3.5" />
              <span>Launch</span>
            </button>
          </form>
        </div>

        {/* Progress Bar */}
        <div className="relative mb-8">
          <div className="flex items-center justify-between text-xs font-medium text-slate-400 mb-2">
            <span>Pipeline Execution: <strong className="text-slate-200">{activeStep}</strong></span>
            <span className="font-mono text-purple-400">{progress}%</span>
          </div>
          <div className="w-full h-2 rounded-full bg-slate-950 overflow-hidden border border-slate-800/80">
            <div 
              className="h-full bg-gradient-to-r from-purple-500 via-pink-500 to-amber-400 transition-all duration-500 ease-out rounded-full"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        {/* Stage Nodes Grid */}
        <div className="grid grid-cols-1 md:grid-cols-5 gap-3 relative z-10">
          {STAGES.map((stage, idx) => {
            const status = getStepStatus(stage.id, idx);
            const Icon = stage.icon;

            return (
              <div
                key={stage.id}
                className={`relative rounded-xl p-4 border transition-all duration-300 ${
                  status === 'active'
                    ? 'bg-purple-950/40 border-purple-500/80 shadow-lg shadow-purple-500/20 scale-[1.02]'
                    : status === 'completed'
                    ? 'bg-slate-950/70 border-emerald-500/40'
                    : 'bg-slate-950/40 border-slate-800/60 opacity-60'
                }`}
              >
                <div className="flex items-center justify-between mb-3">
                  <div className={`p-2 rounded-lg ${
                    status === 'active'
                      ? 'bg-purple-600 text-white'
                      : status === 'completed'
                      ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                      : 'bg-slate-800 text-slate-400'
                  }`}>
                    <Icon className="w-4 h-4" />
                  </div>

                  {status === 'completed' ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  ) : status === 'active' ? (
                    <span className="relative flex h-3 w-3">
                      <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-purple-400 opacity-75" />
                      <span className="relative inline-flex rounded-full h-3 w-3 bg-purple-500" />
                    </span>
                  ) : (
                    <Clock className="w-3.5 h-3.5 text-slate-500" />
                  )}
                </div>

                <div className="font-bold text-xs text-slate-200">{stage.label}</div>
                <div className="text-[11px] text-slate-400 mt-0.5">{stage.desc}</div>

                {/* Sub status tag */}
                <div className="mt-3">
                  <span className={`text-[10px] font-mono font-medium px-2 py-0.5 rounded-md ${
                    status === 'active'
                      ? 'bg-purple-500/20 text-purple-300 border border-purple-500/30'
                      : status === 'completed'
                      ? 'bg-emerald-500/10 text-emerald-400'
                      : 'bg-slate-900 text-slate-500'
                  }`}>
                    {status === 'active' ? 'PROCESSING' : status === 'completed' ? 'DONE' : 'QUEUED'}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Terminal Live Event Log */}
      <div className="rounded-2xl border border-slate-800 bg-slate-950 p-4 font-mono text-xs shadow-inner">
        <div className="flex items-center justify-between border-b border-slate-800 pb-2 mb-3">
          <div className="flex items-center gap-2 text-slate-400">
            <Terminal className="w-4 h-4 text-purple-400" />
            <span className="font-semibold text-slate-300">Live Agent Execution Telemetry</span>
          </div>
          <span className="text-[10px] text-slate-500 font-sans">
            {logs.length} logged events
          </span>
        </div>

        <div className="max-h-48 overflow-y-auto space-y-1.5 pr-2">
          {logs.length === 0 ? (
            <div className="text-slate-600 italic py-2">
              Ready to execute. Click "Run Single Loop" or enable "Auto Loop" to launch pipeline.
            </div>
          ) : (
            logs.map((log, i) => (
              <div key={i} className="flex items-start gap-2 text-slate-300 leading-relaxed">
                <span className="text-slate-500 select-none">
                  [{new Date(log.time).toLocaleTimeString()}]
                </span>
                <span className="text-purple-400 font-semibold select-none">
                  [{log.step}]
                </span>
                <span className="text-slate-200">{log.message}</span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
