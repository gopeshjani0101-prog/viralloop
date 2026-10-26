import React from 'react';
import { 
  BarChart3, 
  TrendingUp, 
  Eye, 
  ThumbsUp, 
  MessageSquare, 
  Sparkles, 
  RotateCw,
  Award
} from 'lucide-react';

export default function AnalyticsCharts({ analytics, onRefresh, isRefreshing }) {
  if (!analytics) return null;

  const {
    total_videos = 0,
    total_views = 0,
    total_likes = 0,
    total_comments = 0,
    avg_retention = 0,
    engagement_rate = 0,
    top_video = null,
    timeline = []
  } = analytics;

  const maxViews = Math.max(...timeline.map(t => t.views), 100);

  return (
    <div className="space-y-6">
      {/* Top Banner Controls */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white tracking-wide">
            Channel Performance & Growth Telemetry
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Real-time YouTube Shorts analytics fed directly into the autonomous learning loop
          </p>
        </div>

        <button
          onClick={onRefresh}
          disabled={isRefreshing}
          className="flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-900 border border-slate-800 hover:bg-slate-800 text-slate-300 text-xs font-semibold transition-all disabled:opacity-50"
        >
          <RotateCw className={`w-3.5 h-3.5 ${isRefreshing ? 'animate-spin' : ''}`} />
          <span>Refresh Metrics</span>
        </button>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 backdrop-blur-md">
          <div className="flex items-center justify-between text-slate-400 text-xs mb-2">
            <span>Total Video Views</span>
            <Eye className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-2xl font-black font-mono text-white">
            {total_views.toLocaleString()}
          </div>
          <div className="text-[11px] text-emerald-400 mt-1 font-medium flex items-center gap-1">
            <TrendingUp className="w-3 h-3" />
            <span>Across {total_videos} generated shorts</span>
          </div>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 backdrop-blur-md">
          <div className="flex items-center justify-between text-slate-400 text-xs mb-2">
            <span>Avg Viewer Retention</span>
            <TrendingUp className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-black font-mono text-emerald-400">
            {avg_retention}%
          </div>
          <div className="text-[11px] text-slate-400 mt-1">
            Industry benchmark: &gt;70%
          </div>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 backdrop-blur-md">
          <div className="flex items-center justify-between text-slate-400 text-xs mb-2">
            <span>Total Likes</span>
            <ThumbsUp className="w-4 h-4 text-pink-400" />
          </div>
          <div className="text-2xl font-black font-mono text-white">
            {total_likes.toLocaleString()}
          </div>
          <div className="text-[11px] text-pink-400 mt-1 font-medium">
            {engagement_rate}% Engagement rate
          </div>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 backdrop-blur-md">
          <div className="flex items-center justify-between text-slate-400 text-xs mb-2">
            <span>Total Comments</span>
            <MessageSquare className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-2xl font-black font-mono text-white">
            {total_comments.toLocaleString()}
          </div>
          <div className="text-[11px] text-cyan-400 mt-1 font-medium">
            Debate & virality driver
          </div>
        </div>
      </div>

      {/* Visual Timeline Bar Chart */}
      <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 backdrop-blur-md">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-2">
            <BarChart3 className="w-4 h-4 text-purple-400" />
            <h3 className="font-bold text-sm text-white">Views Velocity Across Video Cycles</h3>
          </div>
          <span className="text-xs text-slate-400 font-mono">Normalized scale</span>
        </div>

        {timeline.length === 0 ? (
          <div className="text-slate-500 text-xs py-8 text-center italic">
            No videos generated yet. Trigger a pipeline loop to view velocity chart.
          </div>
        ) : (
          <div className="space-y-3">
            {timeline.map((item, idx) => {
              const widthPct = Math.max(8, (item.views / maxViews) * 100);
              return (
                <div key={idx} className="space-y-1">
                  <div className="flex items-center justify-between text-xs text-slate-300">
                    <span className="truncate max-w-[280px] font-medium">{item.title}</span>
                    <span className="font-mono text-purple-300 font-semibold">{item.views.toLocaleString()} views ({item.retention}% ret)</span>
                  </div>
                  <div className="w-full h-3 rounded-full bg-slate-950 overflow-hidden border border-slate-800/80">
                    <div
                      className="h-full bg-gradient-to-r from-purple-600 via-pink-500 to-amber-400 rounded-full transition-all duration-500"
                      style={{ width: `${widthPct}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Top Performer Showcase Card */}
      {top_video && (
        <div className="p-6 rounded-2xl bg-gradient-to-r from-purple-950/40 via-slate-900 to-pink-950/30 border border-purple-500/30 flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-amber-400 text-xs font-bold uppercase tracking-wider">
              <Award className="w-4 h-4" />
              <span>Current Channel Champion</span>
            </div>
            <h4 className="text-lg font-extrabold text-white">
              {top_video.title}
            </h4>
            <p className="text-xs text-slate-300 italic">
              Hook: "{top_video.hook}"
            </p>
          </div>

          <div className="flex items-center gap-4 bg-slate-950/80 px-5 py-3 rounded-xl border border-slate-800">
            <div className="text-center">
              <div className="text-xs text-slate-400">Views</div>
              <div className="font-mono font-bold text-white text-base">{top_video.views.toLocaleString()}</div>
            </div>
            <div className="w-px h-8 bg-slate-800" />
            <div className="text-center">
              <div className="text-xs text-slate-400">Retention</div>
              <div className="font-mono font-bold text-emerald-400 text-base">{top_video.retention_rate}%</div>
            </div>
            <div className="w-px h-8 bg-slate-800" />
            <div className="text-center">
              <div className="text-xs text-slate-400">Likes</div>
              <div className="font-mono font-bold text-pink-400 text-base">{top_video.likes.toLocaleString()}</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
