import React, { useRef, useState, useEffect } from 'react';
import { 
  X, 
  ExternalLink, 
  ThumbsUp, 
  Eye, 
  MessageSquare, 
  Sparkles, 
  TrendingUp, 
  Volume2, 
  VolumeX,
  Play,
  Pause,
  Headphones
} from 'lucide-react';

export default function VideoPlayerModal({ video, onClose }) {
  const videoRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(true);
  const [isMuted, setIsMuted] = useState(false);

  if (!video) return null;

  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.muted = false;
      videoRef.current.play().catch(() => {
        // Autoplay policy prevented unmuted playback, so start muted and show unmute hint
        if (videoRef.current) {
          videoRef.current.muted = true;
          setIsMuted(true);
          videoRef.current.play();
        }
      });
    }
  }, [video]);

  const togglePlay = () => {
    if (!videoRef.current) return;
    if (isPlaying) {
      videoRef.current.pause();
      setIsPlaying(false);
    } else {
      videoRef.current.play();
      setIsPlaying(true);
    }
  };

  const toggleMute = () => {
    if (!videoRef.current) return;
    const nextMuted = !videoRef.current.muted;
    videoRef.current.muted = nextMuted;
    setIsMuted(nextMuted);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md">
      {/* Click outside to close */}
      <div className="absolute inset-0" onClick={onClose} />

      {/* Modal Card */}
      <div className="relative z-10 w-full max-w-4xl bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden shadow-2xl flex flex-col md:flex-row max-h-[92vh]">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 z-30 p-2 rounded-full bg-slate-950/80 hover:bg-slate-800 text-slate-300 hover:text-white transition-colors border border-slate-700/60"
        >
          <X className="w-5 h-5" />
        </button>

        {/* 9:16 Vertical Video Player (Left Side) */}
        <div className="relative bg-black flex items-center justify-center w-full md:w-[420px] aspect-[9/16] max-h-[85vh] overflow-hidden select-none">
          <video
            ref={videoRef}
            src={video.video_url}
            autoPlay
            loop
            controls
            playsInline
            className="w-full h-full object-contain"
          />

          {/* Unmute floating banner if muted by browser autoplay policy */}
          {isMuted && (
            <button
              onClick={toggleMute}
              className="absolute top-4 left-4 z-20 flex items-center gap-2 px-3 py-1.5 rounded-full bg-purple-600 hover:bg-purple-500 text-white text-xs font-bold shadow-lg animate-pulse"
            >
              <VolumeX className="w-4 h-4" />
              <span>Click to Unmute Voice</span>
            </button>
          )}
        </div>

        {/* Video Telemetry & Script Details (Right Side) */}
        <div className="flex-1 p-6 flex flex-col justify-between overflow-y-auto bg-slate-900/95 space-y-5">
          <div className="space-y-4">
            <div>
              <div className="flex items-center gap-2 mb-1.5">
                <span className="px-2.5 py-0.5 rounded-full bg-purple-500/20 border border-purple-500/40 text-purple-300 text-xs font-semibold">
                  YouTube Short
                </span>
                <span className="px-2.5 py-0.5 rounded-full bg-amber-500/20 border border-amber-500/40 text-amber-300 text-xs font-bold flex items-center gap-1">
                  <Sparkles className="w-3 h-3" />
                  Virality: {video.virality_score}
                </span>
              </div>
              <h2 className="text-xl font-extrabold text-white leading-tight">
                {video.title}
              </h2>
            </div>

            {/* Performance Stats Grid */}
            <div className="grid grid-cols-2 gap-3">
              <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                <div className="flex items-center gap-1.5 text-xs text-slate-400 mb-1">
                  <Eye className="w-3.5 h-3.5 text-purple-400" />
                  <span>Views</span>
                </div>
                <div className="text-lg font-bold font-mono text-white">
                  {video.views?.toLocaleString()}
                </div>
              </div>

              <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                <div className="flex items-center gap-1.5 text-xs text-slate-400 mb-1">
                  <TrendingUp className="w-3.5 h-3.5 text-emerald-400" />
                  <span>Viewer Retention</span>
                </div>
                <div className="text-lg font-bold font-mono text-emerald-400">
                  {video.retention_rate}%
                </div>
              </div>

              <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                <div className="flex items-center gap-1.5 text-xs text-slate-400 mb-1">
                  <ThumbsUp className="w-3.5 h-3.5 text-pink-400" />
                  <span>Likes</span>
                </div>
                <div className="text-lg font-bold font-mono text-white">
                  {video.likes?.toLocaleString()}
                </div>
              </div>

              <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                <div className="flex items-center gap-1.5 text-xs text-slate-400 mb-1">
                  <MessageSquare className="w-3.5 h-3.5 text-cyan-400" />
                  <span>Comments</span>
                </div>
                <div className="text-lg font-bold font-mono text-white">
                  {video.comments?.toLocaleString()}
                </div>
              </div>
            </div>

            {/* Hook & Narration Script */}
            <div className="space-y-3">
              <div className="p-3 rounded-xl bg-purple-950/20 border border-purple-500/30">
                <div className="text-[11px] font-bold text-purple-400 uppercase tracking-wider mb-1">
                  Initial 3s Retention Hook
                </div>
                <p className="text-xs text-purple-200 font-medium italic">
                  "{video.hook}"
                </p>
              </div>

              <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">
                    Full Narration Script (Gemma 4)
                  </span>
                  <span className="text-[10px] text-purple-400 font-mono">
                    {video.duration ? `${video.duration.toFixed(1)}s` : ''}
                  </span>
                </div>
                <p className="text-xs text-slate-300 leading-relaxed font-sans">
                  {video.script}
                </p>
              </div>
            </div>

            {/* Tags */}
            <div className="flex flex-wrap gap-1.5">
              {video.tags && video.tags.map((tag, idx) => (
                <span
                  key={idx}
                  className="px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 text-xs font-mono"
                >
                  {tag}
                </span>
              ))}
            </div>
          </div>

          {/* External Action Button */}
          {video.youtube_url && (
            <a
              href={video.youtube_url}
              target="_blank"
              rel="noopener noreferrer"
              className="w-full py-3 rounded-xl bg-red-600 hover:bg-red-500 text-white font-bold text-xs flex items-center justify-center gap-2 transition-colors shadow-lg shadow-red-600/25"
            >
              <ExternalLink className="w-4 h-4" />
              <span>Watch on YouTube Shorts</span>
            </a>
          )}
        </div>
      </div>
    </div>
  );
}
