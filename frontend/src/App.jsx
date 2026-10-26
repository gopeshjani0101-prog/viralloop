import React, { useState, useEffect, useRef } from 'react';
import confetti from 'canvas-confetti';
import { api } from './services/api';
import Navbar from './components/Navbar';
import PipelineVisualizer from './components/PipelineVisualizer';
import VideoCard from './components/VideoCard';
import VideoPlayerModal from './components/VideoPlayerModal';
import AnalyticsCharts from './components/AnalyticsCharts';
import LearningMemory from './components/LearningMemory';
import SettingsModal from './components/SettingsModal';
import { Sparkles, Video, Flame, Film } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('studio');
  const [pipelineStatus, setPipelineStatus] = useState(null);
  const [videos, setVideos] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [insights, setInsights] = useState([]);
  const [activeVideo, setActiveVideo] = useState(null);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isRefreshing, setIsRefreshing] = useState(false);

  const prevCompletedRunId = useRef(null);

  // Poll status and refresh data
  const loadData = async () => {
    try {
      const [statusData, videoList, analyticsData, insightList] = await Promise.all([
        api.getPipelineStatus(),
        api.getVideos(),
        api.getAnalyticsOverview(),
        api.getLearningInsights()
      ]);

      setPipelineStatus(statusData);
      setVideos(videoList);
      setAnalytics(analyticsData);
      setInsights(insightList);

      // Trigger celebration confetti when new run completes
      const currentRun = statusData?.current_run;
      if (
        currentRun &&
        currentRun.status === 'completed' &&
        currentRun.id !== prevCompletedRunId.current
      ) {
        prevCompletedRunId.current = currentRun.id;
        confetti({
          particleCount: 80,
          spread: 70,
          origin: { y: 0.6 }
        });
      }
    } catch (err) {
      console.error('Error fetching dashboard data:', err);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 2500);
    return () => clearInterval(interval);
  }, []);

  const handleTriggerRun = async (customTopic = null) => {
    try {
      await api.triggerPipelineRun(customTopic);
      await loadData();
    } catch (err) {
      console.error('Failed to trigger pipeline run:', err);
    }
  };

  const handleToggleAutonomous = async () => {
    try {
      if (pipelineStatus?.autonomous_mode) {
        await api.stopAutonomous();
      } else {
        await api.startAutonomous(90);
      }
      await loadData();
    } catch (err) {
      console.error('Failed to toggle autonomous mode:', err);
    }
  };

  const handleRefreshAnalytics = async () => {
    setIsRefreshing(true);
    try {
      await api.refreshAnalytics();
      await loadData();
    } catch (err) {
      console.error('Failed to refresh metrics:', err);
    } finally {
      setIsRefreshing(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      {/* Top Navbar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        pipelineStatus={pipelineStatus}
        onTriggerRun={handleTriggerRun}
        onToggleAutonomous={handleToggleAutonomous}
        onOpenSettings={() => setIsSettingsOpen(true)}
        videoCount={videos.length}
        ruleCount={insights.length}
      />

      {/* Main Content Body */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-6">
        {/* TAB 1: Live Studio */}
        {activeTab === 'studio' && (
          <div className="space-y-8">
            <PipelineVisualizer
              pipelineStatus={pipelineStatus}
              onTriggerRun={handleTriggerRun}
            />

            {/* Generated Shorts Live Gallery */}
            <div className="space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
                <div className="flex items-center gap-2">
                  <Flame className="w-5 h-5 text-amber-400" />
                  <h3 className="text-base font-bold text-white">
                    Recently Generated Viral Shorts ({videos.length})
                  </h3>
                </div>
                <button
                  onClick={() => setActiveTab('library')}
                  className="text-xs text-purple-400 hover:text-purple-300 font-semibold"
                >
                  View All Library →
                </button>
              </div>

              {videos.length === 0 ? (
                <div className="p-12 text-center rounded-2xl border border-dashed border-slate-800 bg-slate-900/30">
                  <Film className="w-10 h-10 text-slate-600 mx-auto mb-3" />
                  <h4 className="font-bold text-slate-300 text-sm">No videos generated yet</h4>
                  <p className="text-xs text-slate-500 mt-1 max-w-md mx-auto">
                    Click "Run Single Loop" or inject a custom topic in the pipeline bar above to generate your first Short.
                  </p>
                </div>
              ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                  {videos.slice(0, 8).map((video) => (
                    <VideoCard
                      key={video.id}
                      video={video}
                      onPlay={(v) => setActiveVideo(v)}
                    />
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {/* TAB 2: Library */}
        {activeTab === 'library' && (
          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-bold text-white tracking-wide">
                YouTube Shorts Library ({videos.length})
              </h2>
              <p className="text-xs text-slate-400 mt-0.5">
                All autonomously produced 9:16 vertical videos rendered with FFmpeg burned subtitles
              </p>
            </div>

            {videos.length === 0 ? (
              <div className="p-12 text-center rounded-2xl border border-dashed border-slate-800 bg-slate-900/30">
                <Video className="w-10 h-10 text-slate-600 mx-auto mb-3" />
                <h4 className="font-bold text-slate-300 text-sm">Library is empty</h4>
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                {videos.map((video) => (
                  <VideoCard
                    key={video.id}
                    video={video}
                    onPlay={(v) => setActiveVideo(v)}
                  />
                ))}
              </div>
            )}
          </div>
        )}

        {/* TAB 3: Analytics */}
        {activeTab === 'analytics' && (
          <AnalyticsCharts
            analytics={analytics}
            onRefresh={handleRefreshAnalytics}
            isRefreshing={isRefreshing}
          />
        )}

        {/* TAB 4: Agent Brain */}
        {activeTab === 'learning' && (
          <LearningMemory insights={insights} />
        )}
      </main>

      {/* Video Player Modal */}
      {activeVideo && (
        <VideoPlayerModal
          video={activeVideo}
          onClose={() => setActiveVideo(null)}
        />
      )}

      {/* Settings Modal */}
      {isSettingsOpen && (
        <SettingsModal
          onClose={() => setIsSettingsOpen(false)}
          onSaved={loadData}
        />
      )}

      {/* Footer */}
      <footer className="border-t border-slate-850 bg-slate-950/80 py-4 px-6 text-center text-xs text-slate-500">
        ViralLoop Autonomous Pipeline • Powered by local Ollama (Gemma 4), Edge-TTS, and FFmpeg Compositing
      </footer>
    </div>
  );
}
