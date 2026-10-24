import { useState, useMemo } from "react";
import { motion } from "framer-motion";
import { prompts, nodalNetwork, redTeamSummary } from "@/lib/promptData";
import PromptCard from "@/components/PromptCard";
import { Search, Filter, AlertTriangle, CheckCircle2, ArrowDown } from "lucide-react";

const HERO_IMG = "https://d2xsxph8kpxj0f.cloudfront.net/310519663364046860/XcLnFM2QvGnZZLo6dDqVoZ/hero-botanical-ear9rnEWUBwyPA9rVHST77.webp";
const OLIVE_IMG = "https://d2xsxph8kpxj0f.cloudfront.net/310519663364046860/XcLnFM2QvGnZZLo6dDqVoZ/section-olive-e5Qn9JWcmtEVLP7UimFbFf.webp";
const PATTERN_IMG = "https://d2xsxph8kpxj0f.cloudfront.net/310519663364046860/XcLnFM2QvGnZZLo6dDqVoZ/pattern-geometric-c4Hhtha5gPWA9HofEX9M7W.webp";
const NODAL_IMG = "https://d2xsxph8kpxj0f.cloudfront.net/310519663364046860/XcLnFM2QvGnZZLo6dDqVoZ/nodal-network-M5zhmtr6U3XSVjtzVRoLsW.webp";

type CategoryFilter = "all" | "anthropic" | "xai" | "perplexity" | "google";

export default function Home() {
  const [searchQuery, setSearchQuery] = useState("");
  const [categoryFilter, setCategoryFilter] = useState<CategoryFilter>("all");

  const filteredPrompts = useMemo(() => {
    return prompts.filter((p) => {
      const matchesSearch =
        searchQuery === "" ||
        p.platform.toLowerCase().includes(searchQuery.toLowerCase()) ||
        p.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
        p.prompt.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesCategory =
        categoryFilter === "all" || p.category === categoryFilter;
      return matchesSearch && matchesCategory;
    });
  }, [searchQuery, categoryFilter]);

  const categories: { value: CategoryFilter; label: string }[] = [
    { value: "all", label: "All Platforms" },
    { value: "anthropic", label: "Anthropic" },
    { value: "xai", label: "xAI" },
    { value: "perplexity", label: "Perplexity" },
    { value: "google", label: "Google" },
  ];

  return (
    <div className="min-h-screen bg-[#FDF5E6]">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-[#FDF5E6]/90 backdrop-blur-md border-b border-[#D4A017]/15">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full bg-[#1A1A1A] flex items-center justify-center">
                <span className="text-[#D4A017] text-sm font-bold" style={{ fontFamily: "var(--font-display)" }}>G</span>
              </div>
              <span className="text-lg font-bold text-[#1A1A1A]" style={{ fontFamily: "var(--font-display)" }}>
                Ghusoon Prompt Hub
              </span>
            </div>
            <div className="hidden md:flex items-center gap-6">
              <a href="#prompts" className="text-sm text-[#1A1A1A]/60 hover:text-[#D4A017] transition-colors" style={{ fontFamily: "var(--font-body)" }}>
                Prompts
              </a>
              <a href="#nodal-network" className="text-sm text-[#1A1A1A]/60 hover:text-[#D4A017] transition-colors" style={{ fontFamily: "var(--font-body)" }}>
                Nodal Network
              </a>
              <a href="#red-team" className="text-sm text-[#1A1A1A]/60 hover:text-[#D4A017] transition-colors" style={{ fontFamily: "var(--font-body)" }}>
                Red Team
              </a>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative pt-16 overflow-hidden">
        <div className="relative min-h-[85vh] flex items-center">
          {/* Background Image */}
          <div className="absolute inset-0">
            <img
              src={HERO_IMG}
              alt="Botanical apothecary illustration"
              className="w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-r from-[#FDF5E6]/95 via-[#FDF5E6]/80 to-[#FDF5E6]/40" />
          </div>

          <div className="relative max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="max-w-2xl"
            >
              <p className="text-sm uppercase tracking-[0.3em] text-[#556B2F] mb-4 font-medium" style={{ fontFamily: "var(--font-body)" }}>
                Version 2.0 &mdash; Red Team Perfected
              </p>
              <h1
                className="text-5xl sm:text-6xl lg:text-7xl font-black text-[#1A1A1A] leading-[1.05] mb-6"
                style={{ fontFamily: "var(--font-display)" }}
              >
                Perfected
                <br />
                <span className="text-[#D4A017]">Prompts</span>
                <br />
                for Ghusoon
              </h1>
              <p className="text-lg text-[#1A1A1A]/70 leading-relaxed mb-8 max-w-lg" style={{ fontFamily: "var(--font-body)" }}>
                10 platform-optimized prompts for the Ghusoon natural body care business launch.
                Each prompt has been red-teamed across 5 adversarial dimensions, with 24 weaknesses
                identified and remediated.
              </p>
              <div className="flex items-center gap-4">
                <a
                  href="#prompts"
                  className="inline-flex items-center gap-2 px-6 py-3 bg-[#1A1A1A] text-[#FDF5E6] text-sm font-medium rounded-sm hover:bg-[#333] transition-colors"
                  style={{ fontFamily: "var(--font-body)" }}
                >
                  View All Prompts
                  <ArrowDown size={16} />
                </a>
                <a
                  href="#red-team"
                  className="inline-flex items-center gap-2 px-6 py-3 border border-[#D4A017]/40 text-[#1A1A1A] text-sm font-medium rounded-sm hover:border-[#D4A017] hover:bg-[#D4A017]/5 transition-colors"
                  style={{ fontFamily: "var(--font-body)" }}
                >
                  Red Team Analysis
                </a>
              </div>
            </motion.div>
          </div>
        </div>

        {/* Stats Bar */}
        <div className="relative bg-[#1A1A1A] text-[#FDF5E6]">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              {[
                { value: "10", label: "Platform Prompts" },
                { value: "24", label: "Weaknesses Fixed" },
                { value: "5", label: "Red Team Dimensions" },
                { value: "v2.0", label: "Current Version" },
              ].map((stat, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 10 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.1 }}
                  className="text-center"
                >
                  <p className="text-3xl font-bold text-[#D4A017] mb-1" style={{ fontFamily: "var(--font-display)" }}>
                    {stat.value}
                  </p>
                  <p className="text-xs uppercase tracking-wider text-[#FDF5E6]/50" style={{ fontFamily: "var(--font-body)" }}>
                    {stat.label}
                  </p>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Nodal Network Section */}
      <section id="nodal-network" className="py-20 bg-[#FDF5E6]">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <p className="text-sm uppercase tracking-[0.3em] text-[#556B2F] mb-3 font-medium" style={{ fontFamily: "var(--font-body)" }}>
              Shared Context
            </p>
            <h2
              className="text-3xl sm:text-4xl font-bold text-[#1A1A1A] mb-4"
              style={{ fontFamily: "var(--font-display)" }}
            >
              Nodal Network
            </h2>
            <p className="text-[#1A1A1A]/60 max-w-2xl mb-10 leading-relaxed" style={{ fontFamily: "var(--font-body)" }}>
              The shared context extracted from all attached files and previous conversations.
              Every platform-specific prompt draws from this unified knowledge base.
            </p>
          </motion.div>

          <div className="grid lg:grid-cols-2 gap-8 items-start">
            {/* Network Visualization */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
            >
              <img
                src={NODAL_IMG}
                alt="Ghusoon nodal network visualization"
                className="w-full rounded-sm border border-[#D4A017]/20 shadow-sm"
              />
            </motion.div>

            {/* Network Table */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="space-y-0"
            >
              {nodalNetwork.map((item, i) => (
                <div
                  key={i}
                  className={`flex gap-4 py-3 px-4 ${i % 2 === 0 ? "bg-[#FDFAF3]" : "bg-transparent"} ${i === 0 ? "rounded-t-sm" : ""} ${i === nodalNetwork.length - 1 ? "rounded-b-sm" : ""}`}
                >
                  <span
                    className="text-xs uppercase tracking-wider text-[#D4A017] font-bold w-32 shrink-0 pt-0.5"
                    style={{ fontFamily: "var(--font-body)" }}
                  >
                    {item.node}
                  </span>
                  <span className="text-sm text-[#1A1A1A]/70 leading-relaxed" style={{ fontFamily: "var(--font-body)" }}>
                    {item.details}
                  </span>
                </div>
              ))}
            </motion.div>
          </div>
        </div>
      </section>

      {/* Olive Branch Divider */}
      <div className="relative h-32 overflow-hidden">
        <img
          src={OLIVE_IMG}
          alt="Olive branch illustration"
          className="w-full h-full object-cover opacity-30"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-[#FDF5E6] via-transparent to-[#FDF5E6]" />
      </div>

      {/* Prompts Section */}
      <section id="prompts" className="py-20 bg-[#FDF5E6]">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="mb-10"
          >
            <p className="text-sm uppercase tracking-[0.3em] text-[#556B2F] mb-3 font-medium" style={{ fontFamily: "var(--font-body)" }}>
              Copy &amp; Paste Ready
            </p>
            <h2
              className="text-3xl sm:text-4xl font-bold text-[#1A1A1A] mb-4"
              style={{ fontFamily: "var(--font-display)" }}
            >
              Platform-Optimized Prompts
            </h2>
            <p className="text-[#1A1A1A]/60 max-w-2xl mb-8 leading-relaxed" style={{ fontFamily: "var(--font-body)" }}>
              Each prompt is precisely engineered for its target platform&rsquo;s native DNA.
              Click &ldquo;Copy Prompt&rdquo; to grab the full text, or expand to review the complete content.
            </p>

            {/* Search & Filter */}
            <div className="flex flex-col sm:flex-row gap-3">
              <div className="relative flex-1 max-w-md">
                <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-[#1A1A1A]/30" />
                <input
                  type="text"
                  placeholder="Search prompts..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-9 pr-4 py-2.5 bg-[#FDFAF3] border border-[#D4A017]/20 rounded-sm text-sm text-[#1A1A1A] placeholder:text-[#1A1A1A]/30 focus:outline-none focus:border-[#D4A017]/50 transition-colors"
                  style={{ fontFamily: "var(--font-body)" }}
                />
              </div>
              <div className="flex items-center gap-2">
                <Filter size={14} className="text-[#1A1A1A]/40" />
                {categories.map((cat) => (
                  <button
                    key={cat.value}
                    onClick={() => setCategoryFilter(cat.value)}
                    className={`text-xs font-medium px-3 py-2 rounded-sm transition-colors ${
                      categoryFilter === cat.value
                        ? "bg-[#1A1A1A] text-[#FDF5E6]"
                        : "bg-[#FDFAF3] text-[#1A1A1A]/50 hover:text-[#1A1A1A] border border-[#D4A017]/10"
                    }`}
                    style={{ fontFamily: "var(--font-body)" }}
                  >
                    {cat.label}
                  </button>
                ))}
              </div>
            </div>
          </motion.div>

          {/* Prompt Cards */}
          <div className="space-y-6">
            {filteredPrompts.map((prompt, i) => (
              <PromptCard key={prompt.id} prompt={prompt} index={i} />
            ))}
            {filteredPrompts.length === 0 && (
              <div className="text-center py-16">
                <p className="text-[#1A1A1A]/40 text-sm" style={{ fontFamily: "var(--font-body)" }}>
                  No prompts match your search criteria.
                </p>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Red Team Analysis Section */}
      <section id="red-team" className="relative py-20">
        <div
          className="absolute inset-0 opacity-[0.04]"
          style={{ backgroundImage: `url(${PATTERN_IMG})`, backgroundSize: "400px", backgroundRepeat: "repeat" }}
        />
        <div className="absolute inset-0 bg-[#1A1A1A]" style={{ mixBlendMode: "multiply", opacity: 0.97 }} />

        <div className="relative max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <p className="text-sm uppercase tracking-[0.3em] text-[#D4A017] mb-3 font-medium" style={{ fontFamily: "var(--font-body)" }}>
              Adversarial Analysis
            </p>
            <h2
              className="text-3xl sm:text-4xl font-bold text-[#FDF5E6] mb-4"
              style={{ fontFamily: "var(--font-display)" }}
            >
              Red Team Summary
            </h2>
            <p className="text-[#FDF5E6]/50 max-w-2xl mb-10 leading-relaxed" style={{ fontFamily: "var(--font-body)" }}>
              Each prompt was tested against its platform&rsquo;s known failure modes.
              24 weaknesses were identified across 5 adversarial dimensions and all were remediated.
            </p>
          </motion.div>

          {/* Severity Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
            {[
              { label: "Critical", count: 1, icon: AlertTriangle, color: "text-red-400" },
              { label: "High", count: 9, icon: AlertTriangle, color: "text-amber-400" },
              { label: "Medium", count: 13, icon: CheckCircle2, color: "text-[#556B2F]" },
              { label: "Low", count: 1, icon: CheckCircle2, color: "text-[#D4A017]" },
            ].map((item, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 10 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="bg-[#FDF5E6]/5 border border-[#FDF5E6]/10 rounded-sm p-4"
              >
                <div className="flex items-center gap-2 mb-2">
                  <item.icon size={16} className={item.color} />
                  <span className="text-xs uppercase tracking-wider text-[#FDF5E6]/40" style={{ fontFamily: "var(--font-body)" }}>
                    {item.label}
                  </span>
                </div>
                <p className="text-3xl font-bold text-[#FDF5E6]" style={{ fontFamily: "var(--font-display)" }}>
                  {item.count}
                </p>
              </motion.div>
            ))}
          </div>

          {/* Red Team Table */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="overflow-x-auto"
          >
            <table className="w-full text-sm" style={{ fontFamily: "var(--font-body)" }}>
              <thead>
                <tr className="border-b border-[#D4A017]/20">
                  <th className="text-left py-3 px-4 text-[#D4A017] text-xs uppercase tracking-wider font-bold">Platform</th>
                  <th className="text-left py-3 px-4 text-[#D4A017] text-xs uppercase tracking-wider font-bold">Failure Mode Tested</th>
                  <th className="text-left py-3 px-4 text-[#D4A017] text-xs uppercase tracking-wider font-bold">Mitigation Applied</th>
                </tr>
              </thead>
              <tbody>
                {redTeamSummary.map((row, i) => (
                  <tr key={i} className="border-b border-[#FDF5E6]/5 hover:bg-[#FDF5E6]/5 transition-colors">
                    <td className="py-3 px-4 text-[#FDF5E6] font-medium whitespace-nowrap">{row.platform}</td>
                    <td className="py-3 px-4 text-[#FDF5E6]/60">{row.failureMode}</td>
                    <td className="py-3 px-4 text-[#FDF5E6]/60">{row.mitigation}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-[#1A1A1A] border-t border-[#D4A017]/10 py-12">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full bg-[#D4A017]/20 flex items-center justify-center">
                <span className="text-[#D4A017] text-sm font-bold" style={{ fontFamily: "var(--font-display)" }}>G</span>
              </div>
              <div>
                <p className="text-sm text-[#FDF5E6] font-medium" style={{ fontFamily: "var(--font-display)" }}>
                  Ghusoon Prompt Hub
                </p>
                <p className="text-xs text-[#FDF5E6]/30" style={{ fontFamily: "var(--font-body)" }}>
                  &ldquo;Ignite Your Senses&rdquo;
                </p>
              </div>
            </div>
            <p className="text-xs text-[#FDF5E6]/30" style={{ fontFamily: "var(--font-body)" }}>
              Generated by Manus AI &middot; April 5, 2026 &middot; v2.0 Red Team Edition
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
