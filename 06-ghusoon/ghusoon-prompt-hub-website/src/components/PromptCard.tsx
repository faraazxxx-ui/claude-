import { useState } from "react";
import { toast } from "sonner";
import { motion, AnimatePresence } from "framer-motion";
import type { PromptData } from "@/lib/promptData";
import { Check, Copy, ChevronDown, ChevronUp, Shield } from "lucide-react";

interface PromptCardProps {
  prompt: PromptData;
  index: number;
}

export default function PromptCard({ prompt, index }: PromptCardProps) {
  const [expanded, setExpanded] = useState(false);
  const [copied, setCopied] = useState(false);
  const [showFixes, setShowFixes] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(prompt.prompt);
      setCopied(true);
      toast.success(`${prompt.platform} prompt copied to clipboard`, {
        description: "Ready to paste into the platform",
      });
      setTimeout(() => setCopied(false), 2000);
    } catch {
      toast.error("Failed to copy");
    }
  };

  const categoryColors: Record<string, string> = {
    anthropic: "bg-[#D4A017]/15 text-[#D4A017] border-[#D4A017]/30",
    xai: "bg-[#556B2F]/15 text-[#556B2F] border-[#556B2F]/30",
    perplexity: "bg-[#1A1A1A]/10 text-[#1A1A1A] border-[#1A1A1A]/20",
    google: "bg-[#D4A017]/10 text-[#8B6914] border-[#D4A017]/20",
  };

  const severityLabels: Record<string, { label: string; className: string }> = {
    critical: { label: "Critical Fix", className: "severity-critical" },
    high: { label: "High Fix", className: "severity-high" },
    medium: { label: "Medium Fix", className: "severity-medium" },
  };

  const sev = severityLabels[prompt.severity];

  return (
    <motion.article
      initial={{ opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-50px" }}
      transition={{ duration: 0.5, delay: index * 0.05 }}
      className="group relative"
    >
      <div className="bg-[#FDFAF3] border border-[#D4A017]/20 rounded-sm overflow-hidden transition-shadow duration-300 hover:shadow-[0_4px_24px_rgba(212,160,23,0.12)]">
        {/* Header */}
        <div className="p-6 pb-4">
          <div className="flex items-start justify-between gap-4 mb-3">
            <div className="flex items-center gap-3">
              <span className="text-2xl" role="img" aria-label={prompt.platform}>
                {prompt.icon}
              </span>
              <div>
                <h3
                  className="text-xl font-bold text-[#1A1A1A]"
                  style={{ fontFamily: "var(--font-display)" }}
                >
                  {prompt.id}. {prompt.platform}
                </h3>
                <p className="text-sm text-[#1A1A1A]/60 mt-0.5" style={{ fontFamily: "var(--font-body)" }}>
                  {prompt.description}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2 shrink-0">
              <span className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-sm ${sev.className}`}>
                {sev.label}
              </span>
              <span className={`text-[10px] font-medium uppercase tracking-wider px-2 py-0.5 rounded-sm border ${categoryColors[prompt.category]}`}>
                {prompt.category}
              </span>
            </div>
          </div>

          <div className="gold-rule my-4" />

          {/* Prompt Preview / Full */}
          <div className="relative">
            <div className={`prompt-block text-[13px] leading-relaxed ${expanded ? "" : "max-h-[200px] overflow-hidden"}`}>
              {prompt.prompt}
            </div>
            {!expanded && (
              <div className="absolute bottom-0 left-0 right-0 h-20 bg-gradient-to-t from-[#1A1A1A] to-transparent rounded-b-sm" />
            )}
          </div>

          {/* Actions */}
          <div className="flex items-center gap-3 mt-4">
            <button
              onClick={() => setExpanded(!expanded)}
              className="flex items-center gap-1.5 text-sm font-medium text-[#556B2F] hover:text-[#D4A017] transition-colors"
              style={{ fontFamily: "var(--font-body)" }}
            >
              {expanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
              {expanded ? "Collapse" : "Expand Full Prompt"}
            </button>

            <button
              onClick={handleCopy}
              className="flex items-center gap-1.5 text-sm font-medium text-[#1A1A1A]/70 hover:text-[#D4A017] transition-colors ml-auto"
              style={{ fontFamily: "var(--font-body)" }}
            >
              {copied ? <Check size={16} className="text-[#556B2F]" /> : <Copy size={16} />}
              {copied ? "Copied!" : "Copy Prompt"}
            </button>

            <button
              onClick={() => setShowFixes(!showFixes)}
              className="flex items-center gap-1.5 text-sm font-medium text-[#1A1A1A]/70 hover:text-[#D4A017] transition-colors"
              style={{ fontFamily: "var(--font-body)" }}
            >
              <Shield size={16} />
              Red Team
            </button>
          </div>
        </div>

        {/* Red Team Analysis Drawer */}
        <AnimatePresence>
          {showFixes && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: "auto", opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.3 }}
              className="overflow-hidden"
            >
              <div className="px-6 pb-6 pt-2 border-t border-[#D4A017]/15 bg-[#FDF5E6]/50">
                <h4
                  className="text-sm font-bold text-[#1A1A1A] mb-2 uppercase tracking-wider"
                  style={{ fontFamily: "var(--font-body)" }}
                >
                  Why This Works
                </h4>
                <p className="text-sm text-[#1A1A1A]/70 mb-4 leading-relaxed" style={{ fontFamily: "var(--font-body)" }}>
                  {prompt.whyItWorks}
                </p>
                <h4
                  className="text-sm font-bold text-[#1A1A1A] mb-2 uppercase tracking-wider"
                  style={{ fontFamily: "var(--font-body)" }}
                >
                  Red Team Fixes Applied
                </h4>
                <ul className="space-y-1.5">
                  {prompt.redTeamFixes.map((fix, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-[#1A1A1A]/70" style={{ fontFamily: "var(--font-body)" }}>
                      <span className="text-[#D4A017] mt-0.5 shrink-0">\u2713</span>
                      {fix}
                    </li>
                  ))}
                </ul>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.article>
  );
}
