import React, { useState, useEffect } from 'react';
import { X, Check, Cpu, Share2, Volume2, Sparkles } from 'lucide-react';
import { api } from '../services/api';

export default function SettingsModal({ onClose, onSaved }) {
  const [settings, setSettings] = useState(null);
  const [selectedModel, setSelectedModel] = useState('');
  const [youtubeMode, setYoutubeMode] = useState('simulated');
  const [ttsVoice, setTtsVoice] = useState('en-US-ChristopherNeural');
  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    async function fetchSettings() {
      try {
        const data = await api.getSettings();
        setSettings(data);
        setSelectedModel(data.ollama_configured_model || 'gemma4');
        setYoutubeMode(data.youtube_mode || 'simulated');
        setTtsVoice(data.tts_voice || 'en-US-ChristopherNeural');
      } catch (err) {
        console.error('Failed to load settings', err);
      }
    }
    fetchSettings();
  }, []);

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      await api.updateSettings({
        ollama_model: selectedModel,
        youtube_mode: youtubeMode,
        tts_voice: ttsVoice
      });
      setSuccess(true);
      setTimeout(() => {
        setSuccess(false);
        if (onSaved) onSaved();
        onClose();
      }, 1000);
    } catch (err) {
      console.error('Failed to save settings', err);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
      <div className="absolute inset-0" onClick={onClose} />

      <div className="relative z-10 w-full max-w-lg bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-2xl">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-5">
          <div className="flex items-center gap-2">
            <Cpu className="w-5 h-5 text-purple-400" />
            <h3 className="font-extrabold text-lg text-white">ViralLoop System Config</h3>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-full hover:bg-slate-800 text-slate-400 hover:text-white transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSave} className="space-y-5">
          {/* Ollama Local LLM Model */}
          <div className="space-y-1.5">
            <label className="text-xs font-bold text-slate-300 flex items-center justify-between">
              <span>Local LLM Engine (Ollama)</span>
              <span className="text-[10px] text-purple-400 font-mono">localhost:11434</span>
            </label>
            <select
              value={selectedModel}
              onChange={(e) => setSelectedModel(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-white focus:outline-none focus:border-purple-500 font-mono"
            >
              {settings?.available_models?.map((model) => (
                <option key={model} value={model}>
                  {model} {model.includes('gemma') ? '⭐ (Gemma Recommended)' : ''}
                </option>
              )) || (
                <>
                  <option value="gemma4">gemma4 (Active)</option>
                  <option value="gemma:2b">gemma:2b</option>
                  <option value="qwen2.5:3b">qwen2.5:3b</option>
                </>
              )}
            </select>
            <p className="text-[11px] text-slate-500">
              Powers all viral topic selection, 3-second hook crafting, and evolutionary reflection.
            </p>
          </div>

          {/* YouTube Publishing Mode */}
          <div className="space-y-1.5">
            <label className="text-xs font-bold text-slate-300">
              YouTube Shorts Publishing Mode
            </label>
            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => setYoutubeMode('simulated')}
                className={`p-3 rounded-xl border text-left transition-all ${
                  youtubeMode === 'simulated'
                    ? 'bg-purple-950/40 border-purple-500 text-white'
                    : 'bg-slate-950 border-slate-800 text-slate-400 hover:text-slate-300'
                }`}
              >
                <div className="text-xs font-bold">Simulator (Hackathon)</div>
                <div className="text-[10px] text-slate-400 mt-1">Instant demo URLs & simulated growth metrics</div>
              </button>

              <button
                type="button"
                onClick={() => setYoutubeMode('live')}
                className={`p-3 rounded-xl border text-left transition-all ${
                  youtubeMode === 'live'
                    ? 'bg-purple-950/40 border-purple-500 text-white'
                    : 'bg-slate-950 border-slate-800 text-slate-400 hover:text-slate-300'
                }`}
              >
                <div className="text-xs font-bold">Live YouTube API</div>
                <div className="text-[10px] text-slate-400 mt-1">OAuth 2.0 via Google Cloud Data API v3</div>
              </button>
            </div>
          </div>

          {/* TTS Neural Voice */}
          <div className="space-y-1.5">
            <label className="text-xs font-bold text-slate-300">
              Neural Voiceover Actor (Edge-TTS)
            </label>
            <select
              value={ttsVoice}
              onChange={(e) => setTtsVoice(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-white focus:outline-none focus:border-purple-500 font-mono"
            >
              <option value="en-US-ChristopherNeural">en-US-ChristopherNeural (High Energy Male)</option>
              <option value="en-US-JennyNeural">en-US-JennyNeural (Engaging Female)</option>
              <option value="en-US-GuyNeural">en-US-GuyNeural (Direct Narrator)</option>
              <option value="en-GB-SoniaNeural">en-GB-SoniaNeural (British Storyteller)</option>
            </select>
          </div>

          {/* Submit Button */}
          <div className="pt-3 border-t border-slate-800 flex justify-end gap-3">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold transition-colors"
            >
              Cancel
            </button>

            <button
              type="submit"
              disabled={saving}
              className="px-5 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-bold flex items-center gap-2 transition-all shadow-lg shadow-purple-600/30"
            >
              {success ? (
                <>
                  <Check className="w-4 h-4 text-white" />
                  <span>Saved!</span>
                </>
              ) : (
                <span>Save Configuration</span>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
