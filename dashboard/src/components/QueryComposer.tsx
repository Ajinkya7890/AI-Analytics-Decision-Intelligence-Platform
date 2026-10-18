import React, { useRef, useEffect } from 'react';
import { Send, Loader2, Sparkles, X, AlertTriangle } from 'lucide-react';

interface QueryComposerProps {
  question: string;
  setQuestion: (q: string) => void;
  onSubmit: (e?: React.FormEvent) => void;
  loading: boolean;
  error: string | null;
  onClearError: () => void;
}

export const QueryComposer: React.FC<QueryComposerProps> = ({
  question,
  setQuestion,
  onSubmit,
  loading,
  error,
  onClearError,
}) => {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 180)}px`;
    }
  }, [question]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      if (!loading && question.trim()) {
        onSubmit();
      }
    }
  };

  return (
    <div className="space-y-3">
      <div className="relative bg-background-card border border-border focus-within:border-accent focus-within:ring-1 focus-within:ring-accent rounded-xl shadow-panel transition-all">
        <div className="p-3.5 pb-2">
          <textarea
            ref={textareaRef}
            value={question}
            onChange={(e) => {
              setQuestion(e.target.value);
              if (error) onClearError();
            }}
            onKeyDown={handleKeyDown}
            disabled={loading}
            placeholder="Ask your data in natural language... (e.g. Which categories generated the highest revenue?)"
            rows={2}
            className="w-full bg-transparent text-content-primary placeholder-content-muted text-sm resize-none focus:outline-none leading-relaxed disabled:opacity-50"
          />
        </div>

        <div className="flex items-center justify-between px-3.5 py-2.5 border-t border-border-subtle/60 bg-background-card/50 rounded-b-xl">
          <div className="flex items-center space-x-2 text-[11px] text-content-muted">
            <Sparkles className="w-3.5 h-3.5 text-accent" />
            <span>Press <kbd className="px-1.5 py-0.5 rounded bg-background-surface border border-border-subtle font-mono text-[10px]">Ctrl</kbd> + <kbd className="px-1.5 py-0.5 rounded bg-background-surface border border-border-subtle font-mono text-[10px]">Enter</kbd> to run</span>
          </div>

          <div className="flex items-center space-x-2">
            {question && (
              <button
                type="button"
                onClick={() => {
                  setQuestion('');
                  if (error) onClearError();
                }}
                disabled={loading}
                className="p-1.5 text-content-secondary hover:text-content-primary rounded hover:bg-background-hover transition-colors text-xs"
                title="Clear question"
              >
                <X className="w-4 h-4" />
              </button>
            )}

            <button
              type="button"
              onClick={() => onSubmit()}
              disabled={loading || !question.trim()}
              className="px-4 py-2 bg-accent hover:bg-accent-hover text-white text-xs font-semibold rounded-lg transition-all flex items-center space-x-2 shadow-sm disabled:opacity-40 disabled:cursor-not-allowed"
            >
              {loading ? (
                <>
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  <span>Analyzing...</span>
                </>
              ) : (
                <>
                  <Send className="w-3.5 h-3.5" />
                  <span>Run Analysis</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {error && (
        <div className="p-3 bg-status-error-bg border border-status-error/30 rounded-xl flex items-start space-x-3 text-xs text-status-error animate-fadeIn">
          <AlertTriangle className="w-4 h-4 flex-shrink-0 mt-0.5" />
          <div className="flex-1">
            <span className="font-semibold block mb-0.5">Analysis Failed</span>
            <p className="text-content-primary/90 leading-relaxed">{error}</p>
          </div>
          <button
            onClick={onClearError}
            className="text-content-secondary hover:text-content-primary p-0.5"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        </div>
      )}
    </div>
  );
};
