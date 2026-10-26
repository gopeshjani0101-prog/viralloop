import React from 'react';
import { 
  Play, 
  Pause, 
  RotateCw, 
  Settings, 
  Sparkles, 
  Video, 
  BarChart3, 
  Brain, 
  Layers
} from 'lucide-react';

export default function Navbar({
  activeTab,
  setActiveTab,
  pipelineStatus,
  onTriggerRun,
  onToggleAutonomous,
  onOpenSettings,
  videoCount,
  ruleCount
}) {
  const isRunning = pipelineStatus?.is_running;
  const isAuto = pipelineStatus?.autonomous_mode;
  const currentStep = pipelineStatus?.current_run?.current_step || 'Idle';

  return (
    <header className="border-b border-slate-800 bg-slate-950/80 backdrop-blur-md sticky top-0 z-40 px-6 py-3.5">
      <div className="max-w-7xl mx-auto flex items-center justify-between gap-4">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-purple-600 via-pink-500 to-amber-400 flex items-center justify-center shadow-lg shadow-purple-500/20">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-xl tracking-tight bg-gradient-to-r from-white via-slate-200 to-purple-300 bg-clip-text text-transparent">
                ViralLoop
              </span>
              <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-purple-950/80 border border-purple-800 text-purple-300 uppercase tracking-wider">
                Autonomous AI
              </span>
            </div>
            <p className="text-xs text-slate-400 font-medium">Self-Improving Shorts Studio</p>
          </div>
        </div>

        {/* Tab Navigation */}
        <nav className="flex items-center gap-1 bg-slate-900/90 p-1 rounded-xl border border-slate-800">
          <button
            onClick={() => setActiveTab('studio')}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-sm font-medium transition-all ${
              activeTab === 'studio'
                ? 'bg-purple-600 text-white shadow-md shadow-purple-600/30'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
            }`}
          >
            <Layers className="w-4 h-4" />
            <span>Studio</span>
            {isRunning && (
              <span className="w-2 h-2 rounded-full bg-amber-400 animate-ping ml-1" />
            )}
          </button>

          <button
            onClick={() => setActiveTab('library')}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-sm font-medium transition-all ${
              activeTab === 'library'
                ? 'bg-purple-600 text-white shadow-md shadow-purple-600/30'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
            }`}
          >
            <Video className="w-4 h-4" />
            <span>Shorts</span>
            <span className="px-1.5 py-0.2 rounded-full bg-slate-800 text-slate-300 text-xs">
              {videoCount}
            </span>
          </button>

          <button
            onClick={() => setActiveTab('analytics')}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-sm font-medium transition-all ${
              activeTab === 'analytics'
                ? 'bg-purple-600 text-white shadow-md shadow-purple-600/30'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
            }`}
          >
            <BarChart3 className="w-4 h-4" />
            <span>Analytics</span>
          </button>

          <button
            onClick={() => setActiveTab('learning')}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-sm font-medium transition-all ${
              activeTab === 'learning'
                ? 'bg-purple-600 text-white shadow-md shadow-purple-600/30'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
            }`}
          >
            <Brain className="w-4 h-4" />
            <span>Brain Memory</span>
            <span className="px-1.5 py-0.2 rounded-full bg-slate-800 text-slate-300 text-xs">
              {ruleCount}
            </span>
          </button>
        </nav>

        {/* Action Controls */}
        <div className="flex items-center gap-3">
          {/* Status Pill */}
          <div className="hidden lg:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs">
            <span
              className={`w-2 h-2 rounded-full ${
                isRunning
                  ? 'bg-amber-400 animate-pulse'
                  : isAuto
                  ? 'bg-emerald-400'
                  : 'bg-slate-500'
              }`}
            />
            <span className="text-slate-300 font-medium">
              {isRunning
                ? `Running: ${currentStep}`
                : isAuto
                ? 'Autonomous Loop Active'
                : 'Idle Ready'}
            </span>
          </div>

          {/* Autonomous Mode Switch */}
          <button
            onClick={onToggleAutonomous}
            className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-semibold border transition-all ${
              isAuto
                ? 'bg-emerald-500/15 border-emerald-500/40 text-emerald-400 hover:bg-emerald-500/25'
                : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-slate-200 hover:bg-slate-800'
            }`}
            title="Automatically run cycles every 2 minutes and learn continuously"
          >
            {isAuto ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
            <span>Auto Loop</span>
          </button>

          {/* Single Loop Trigger */}
          <button
            onClick={() => onTriggerRun()}
            disabled={isRunning}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold text-white shadow-lg transition-all ${
              isRunning
                ? 'bg-slate-800 cursor-not-allowed opacity-60 text-slate-400'
                : 'bg-gradient-to-r from-purple-600 via-pink-600 to-amber-500 hover:from-purple-500 hover:to-amber-400 shadow-purple-600/25 hover:shadow-purple-600/40'
            }`}
          >
            <RotateCw className={`w-3.5 h-3.5 ${isRunning ? 'animate-spin' : ''}`} />
            <span>{isRunning ? 'Processing...' : 'Run Single Loop'}</span>
          </button>

          {/* Settings */}
          <button
            onClick={onOpenSettings}
            className="p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            title="Settings & Ollama Model"
          >
            <Settings className="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>
  );
}
