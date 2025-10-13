// frontend/src/components/AgentForm.jsx
import React, { useState, useEffect } from 'react';
import Input from './common/Input';
import Button from './common/Button';
import useAgentStore from '../store/agentStore';
import { getAgentOptions } from '../services/agentApi';

const AgentForm = ({ onFormSubmit }) => {
  const [formData, setFormData] = useState({
    name: '',
    system_prompt: '',
    voice_id: 'default_voice',
    llm_provider: 'gemini',
    llm_model: 'gemini-1.5-flash',
    tts_voice_id: '21m00Tcm4TlvDq8ikWAM',
    stt_provider: 'deepgram',
  });

  const [options, setOptions] = useState({
    llm_providers: [],
    stt_providers: [],
    tts_voices: []
  });

  const createAgent = useAgentStore((state) => state.createAgent);
  const loading = useAgentStore((state) => state.loading);

  // Load available options on mount
  useEffect(() => {
    const loadOptions = async () => {
      try {
        const data = await getAgentOptions();
        setOptions(data);
      } catch (error) {
        console.error('Failed to load agent options:', error);
      }
    };
    loadOptions();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => {
      const updated = { ...prev, [name]: value };
      
      // Auto-select first model when provider changes
      if (name === 'llm_provider') {
        const provider = options.llm_providers.find(p => p.id === value);
        if (provider && provider.models.length > 0) {
          updated.llm_model = provider.models[0].id;
        }
      }
      
      return updated;
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await createAgent(formData);
    setFormData({ 
      name: '', 
      system_prompt: '', 
      voice_id: 'default_voice',
      llm_provider: 'gemini',
      llm_model: 'gemini-1.5-flash',
      tts_voice_id: '21m00Tcm4TlvDq8ikWAM',
      stt_provider: 'deepgram',
    }); // Reset form
    if (onFormSubmit) {
      onFormSubmit(); // Callback to close modal or refresh list
    }
  };

  // Get available models for the selected LLM provider
  const availableModels = options.llm_providers
    .find(p => p.id === formData.llm_provider)?.models || [];

  return (
    <form onSubmit={handleSubmit} className="card">
      <h2>Create New Agent</h2>
      
      <Input
        label="Agent Name"
        name="name"
        value={formData.name}
        onChange={handleChange}
        required
      />
      
      <div className="form-group">
        <label htmlFor="system_prompt">System Prompt</label>
        <textarea
          id="system_prompt"
          name="system_prompt"
          value={formData.system_prompt}
          onChange={handleChange}
          required
          rows="8"
          className="textarea"
          placeholder="You are a helpful AI assistant specialized in..."
        />
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="llm_provider">LLM Provider</label>
          <select
            id="llm_provider"
            name="llm_provider"
            value={formData.llm_provider}
            onChange={handleChange}
            className="select"
            required
          >
            {options.llm_providers.map(provider => (
              <option key={provider.id} value={provider.id}>
                {provider.name}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="llm_model">LLM Model</label>
          <select
            id="llm_model"
            name="llm_model"
            value={formData.llm_model}
            onChange={handleChange}
            className="select"
            required
          >
            {availableModels.map(model => (
              <option key={model.id} value={model.id}>
                {model.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="tts_voice_id">Voice</label>
          <select
            id="tts_voice_id"
            name="tts_voice_id"
            value={formData.tts_voice_id}
            onChange={handleChange}
            className="select"
            required
          >
            {options.tts_voices.map(voice => (
              <option key={voice.id} value={voice.id}>
                {voice.name}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="stt_provider">Speech Recognition</label>
          <select
            id="stt_provider"
            name="stt_provider"
            value={formData.stt_provider}
            onChange={handleChange}
            className="select"
            required
          >
            {options.stt_providers.map(provider => (
              <option key={provider.id} value={provider.id}>
                {provider.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      <Input
        label="Voice ID (Legacy)"
        name="voice_id"
        value={formData.voice_id}
        onChange={handleChange}
        required
      />
      
      <Button type="submit" disabled={loading}>
        {loading ? 'Creating...' : 'Create Agent'}
      </Button>
    </form>
  );
};

export default AgentForm;