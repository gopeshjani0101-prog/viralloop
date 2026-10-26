import React from 'react';
import { Play, Eye, ThumbsUp, Flame, ExternalLink, MessageSquare } from 'lucide-react';

export default function VideoCard({ video, onPlay }) {
  const formatNumber = (num) => {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toString();
  };

  return (
    <div className="group rounded-2xl border border-slate-800 bg-slate-900/60 overflow-hidden hover:border-purple-500/50 hover:shadow-xl hover:shadow-purple-500/10 transition-all flex flex-col">
      {/* 9:16 Thumbnail Preview Container */}
      <div 
        onClick={() => onPlay(video)}
        className="relative w-full aspect-[9/16] max-h-72 bg-slate-950 overflow-hidden cursor-pointer"
      >
        {video.thumbnail_url ? (
          <img
            src={video.thumbnail_url}
            alt={video.title}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
            onError={(e) => {
              e.target.style.display = 'none';
            }}
          />
        ) : null}

        {/* Fallback pattern if thumbnail not loaded */}
        <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-900/40 to-transparent pointer-events-none" />

        {/* Play hover overlay */}
        <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity bg-black/40 backdrop-blur-xs">
          <div className="w-12 h-12 rounded-full bg-purple-600/90 text-white flex items-center justify-center shadow-lg transform group-hover:scale-110 transition-transform">
            <Play className="w-5 h-5 fill-white ml-0.5" />
          </div>
        </div>

        {/* Duration badge */}
        <div className="absolute bottom-2.5 right-2.5 px-2 py-0.5 rounded-md bg-black/80 text-[11px] font-mono font-medium text-slate-200">
          {video.duration ? `${video.duration.toFixed(1)}s` : 'Short'}
        </div>

        {/* Virality score badge */}
        <div className="absolute top-2.5 left-2.5 flex items-center gap-1 px-2 py-0.5 rounded-md bg-amber-500/90 text-[11px] font-bold text-slate-950 shadow-md">
          <Flame className="w-3.5 h-3.5 fill-slate-950" />
          <span>{video.virality_score} Virality</span>
        </div>
      </div>

      {/* Video Info Content */}
      <div className="p-4 flex-1 flex flex-col justify-between space-y-3">
        <div>
          <h3 className="font-bold text-sm text-slate-100 line-clamp-2 group-hover:text-purple-300 transition-colors">
            {video.title}
          </h3>
          <p className="text-[11px] text-slate-400 italic line-clamp-2 mt-1.5 bg-slate-950/60 p-2 rounded-lg border border-slate-800/80">
            "{video.hook}"
          </p>
        </div>

        {/* Stats Row */}
        <div className="pt-2 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
          <div className="flex items-center gap-3">
            <span className="flex items-center gap-1 font-mono text-slate-300" title="Views">
              <Eye className="w-3.5 h-3.5 text-purple-400" />
              {formatNumber(video.views)}
            </span>
            <span className="flex items-center gap-1 font-mono text-slate-300" title="Likes">
              <ThumbsUp className="w-3.5 h-3.5 text-pink-400" />
              {formatNumber(video.likes)}
            </span>
          </div>

          <div className="flex items-center gap-1 font-mono font-bold text-emerald-400 text-[11px]">
            <span>{video.retention_rate}% Ret</span>
          </div>
        </div>

        {/* Actions Button */}
        <div className="flex items-center gap-2 pt-1">
          <button
            onClick={() => onPlay(video)}
            className="flex-1 py-1.5 rounded-lg bg-purple-600/20 hover:bg-purple-600/30 border border-purple-500/30 text-purple-300 text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors"
          >
            <Play className="w-3 h-3 fill-purple-300" />
            <span>Play Short</span>
          </button>

          {video.youtube_url && (
            <a
              href={video.youtube_url}
              target="_blank"
              rel="noopener noreferrer"
              className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition-colors"
              title="Open YouTube Shorts"
            >
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          )}
        </div>
      </div>
    </div>
  );
}
