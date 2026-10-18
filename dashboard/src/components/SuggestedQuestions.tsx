import React from 'react';
import { ArrowUpRight, TrendingUp, BarChart3, Clock, DollarSign, AlertCircle } from 'lucide-react';

interface SuggestedQuestionsProps {
  onSelectQuestion: (question: string) => void;
  disabled?: boolean;
}

interface QuestionItem {
  question: string;
  category: 'Ranking' | 'Trend' | 'Logistics' | 'Financial';
  icon: React.ComponentType<{ className?: string }>;
}

const VERIFIED_SUGGESTIONS: QuestionItem[] = [
  {
    question: 'Which categories generated the highest revenue?',
    category: 'Ranking',
    icon: BarChart3,
  },
  {
    question: 'What were the top 5 products by revenue?',
    category: 'Ranking',
    icon: BarChart3,
  },
  {
    question: 'What was our monthly revenue?',
    category: 'Trend',
    icon: TrendingUp,
  },
  {
    question: 'Which sellers generated the highest revenue in 2017?',
    category: 'Ranking',
    icon: BarChart3,
  },
  {
    question: 'What is the average delivery time?',
    category: 'Logistics',
    icon: Clock,
  },
  {
    question: 'What is the on-time delivery rate?',
    category: 'Logistics',
    icon: Clock,
  },
  {
    question: 'What was our revenue in 2017?',
    category: 'Financial',
    icon: DollarSign,
  },
  {
    question: 'Why did revenue decrease in 2018?',
    category: 'Trend',
    icon: AlertCircle,
  },
];

export const SuggestedQuestions: React.FC<SuggestedQuestionsProps> = ({
  onSelectQuestion,
  disabled,
}) => {
  return (
    <div className="space-y-2.5">
      <div className="flex items-center justify-between">
        <span className="text-xs font-medium text-content-secondary uppercase tracking-wider">
          Suggested Analytical Queries
        </span>
        <span className="text-[11px] text-content-muted">
          8 verified against database
        </span>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2.5">
        {VERIFIED_SUGGESTIONS.map((item, index) => {
          const Icon = item.icon;
          return (
            <button
              key={index}
              onClick={() => onSelectQuestion(item.question)}
              disabled={disabled}
              className="p-3 bg-background-card hover:bg-background-hover border border-border-subtle hover:border-accent/40 rounded-xl text-left transition-all group flex flex-col justify-between space-y-2 shadow-sm disabled:opacity-50 disabled:pointer-events-none"
            >
              <div className="flex items-center justify-between w-full">
                <span className="inline-flex items-center space-x-1 px-1.5 py-0.5 rounded text-[10px] font-medium bg-background-surface text-accent border border-accent/20">
                  <Icon className="w-3 h-3" />
                  <span>{item.category}</span>
                </span>
                <ArrowUpRight className="w-3.5 h-3.5 text-content-muted group-hover:text-accent group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
              </div>
              <p className="text-xs text-content-primary font-medium group-hover:text-white line-clamp-2">
                {item.question}
              </p>
            </button>
          );
        })}
      </div>
    </div>
  );
};
