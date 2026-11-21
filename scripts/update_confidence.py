import re

def update_confidence_section():
    file_path = 'about/index.html'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define the new HTML markup for section confidence
    new_confidence_html = '''<section class="section confidence"><div class="w-layout-blockcontainer container w-container"><div class="confidence-wrapper"><div class="confidence-top-wrap"><div class="confidence-left-wrap"><div animation="fade-one" class="confidence-sub-title-wrap"><div data-wf--section-sub-title--variant="gray" class="section-sub-title w-variant-da0b81eb-ef6f-7786-e1c2-2810d345cc81">ENGINEERING INTELLIGENCE</div></div><div animation="heading" class="confidence-title-wrap"><h2 data-wf--section-title--variant="two" class="section-title w-variant-a1c41d54-f4a0-ff01-86fc-643e3a321238">See how engineers think under pressure</h2></div></div><div animation="fade-two" class="confidence-right-wrap"><p data-wf--global-details--variant="base" class="global-details">We evaluate how engineers design systems, solve problems, and respond when things break — using evidence from real engineering work.</p></div></div><div class="confidence-wrap"><div class="confidence-grid-wrap">

          <!-- Card 1: Architecture -->
          <div animation="fade-three" data-wf--confidence-card--variant="base" class="confidence-card">
            <div class="confidence-card-visual">
              <div class="arch-topology-widget">
                <div class="arch-top-row">
                  <span class="arch-tag">SYSTEM TOPOLOGY</span>
                  <span class="arch-pulse"><span class="pulse-dot-green"></span> 99.98% Healthy</span>
                </div>
                <div class="arch-canvas">
                  <div class="arch-node-gateway">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
                    <span>Edge API Gateway</span>
                  </div>
                  <svg class="arch-connector-svg" viewBox="0 0 160 20" fill="none">
                    <path d="M80 0v6 M80 6H26v14 M80 6h54v14 M80 6h54v14" stroke="rgba(25,24,20,0.18)" stroke-width="1.2" stroke-dasharray="2 2"/>
                  </svg>
                  <div class="arch-pods-row">
                    <div class="arch-pod">
                      <span>Auth / Edge</span>
                      <small>p99 &lt; 12ms</small>
                    </div>
                    <div class="arch-pod">
                      <span>Worker Pods</span>
                      <small>Decoupled</small>
                    </div>
                    <div class="arch-pod">
                      <span>Postgres</span>
                      <small>ACID Sync</small>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="confidence-card-btm-wrap">
              <div class="confidence-card-header">
                <h3 class="confidence-card-title">Architecture</h3>
                <span class="confidence-score-badge">88%</span>
              </div>
              <p class="confidence-card-details">Designs modular, low-debt architectures that scale under heavy production load.</p>
            </div>
          </div>

          <!-- Card 2: Root-Cause Analysis -->
          <div animation="fade-three" data-wf--confidence-card--variant="blue" class="confidence-card w-variant-ca1e33b9-993c-a4af-99f2-8e46f98ff451">
            <div class="confidence-card-visual">
              <div class="rca-widget">
                <div class="rca-top-row">
                  <span class="rca-tag">TRIAL #04 TELEMETRY</span>
                  <span class="rca-iso-badge"><span class="pulse-dot-green"></span> Isolated</span>
                </div>
                <div class="rca-compare-box">
                  <div class="rca-metric-col">
                    <span class="rca-num-old">142m</span>
                    <small>Standard MTTR</small>
                  </div>
                  <div class="rca-arrow">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                  </div>
                  <div class="rca-metric-col">
                    <span class="rca-num-new">14.5m</span>
                    <small>Candidate Speed</small>
                  </div>
                </div>
                <div class="rca-bottom-bar">
                  <span>10x faster diagnosis</span>
                  <span>91% accuracy</span>
                </div>
              </div>
            </div>
            <div class="confidence-card-btm-wrap">
              <div class="confidence-card-header">
                <h3 class="confidence-card-title">Root-Cause Analysis</h3>
                <span class="confidence-score-badge">91%</span>
              </div>
              <p class="confidence-card-details">Isolates bugs at the root. Reduces average diagnosis time from 142m to 14.5m.</p>
            </div>
          </div>

          <!-- Card 3: Radar Chart Graphic -->
          <div animation="fade-four" id="w-node-_022832c3-0bf8-ec2a-caf5-7c7d8411df64-8a159b38" class="confidence-image-wrap">
            <img src="../images/nimo-engineering-intelligence-radar.webp" loading="lazy" alt="NIMO 5-Axis Engineering Intelligence Radar" class="confidence-image">
          </div>

          <!-- Card 4: Five dimensions -->
          <div animation="fade-five" id="w-node-_253d24ca-b5e3-4f93-e357-6d9f99be4989-8a159b38" class="confidence-details-card">
            <div class="confidence-details-wrap">
              <h3 class="confidence-details-headline">Five dimensions. One engineering profile.</h3>
              <p class="confidence-details-desc">We evaluate engineers across realistic distributed systems challenges — synthesizing raw code telemetry into a unified, evidence-backed radar profile.</p>
              <div class="confidence-evidence-badge">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M20 6L9 17l-5-5"/></svg>
                <span>100% telemetry-backed evidence</span>
              </div>
            </div>
            <div class="confidence-dimensions-list">
              <div class="dim-row">
                <span class="dim-name">Architecture</span>
                <div class="dim-bar-wrap"><div class="dim-bar-fill" style="width: 88%;"></div></div>
                <span class="dim-val">88%</span>
              </div>
              <div class="dim-row">
                <span class="dim-name">Root-Cause Analysis</span>
                <div class="dim-bar-wrap"><div class="dim-bar-fill green" style="width: 91%;"></div></div>
                <span class="dim-val">91%</span>
              </div>
              <div class="dim-row">
                <span class="dim-name">Incident Response</span>
                <div class="dim-bar-wrap"><div class="dim-bar-fill" style="width: 89%;"></div></div>
                <span class="dim-val">89%</span>
              </div>
              <div class="dim-row">
                <span class="dim-name">Idea Generation</span>
                <div class="dim-bar-wrap"><div class="dim-bar-fill blue" style="width: 86%;"></div></div>
                <span class="dim-val">86%</span>
              </div>
              <div class="dim-row">
                <span class="dim-name">Code Review</span>
                <div class="dim-bar-wrap"><div class="dim-bar-fill blue" style="width: 85%;"></div></div>
                <span class="dim-val">85%</span>
              </div>
            </div>
          </div>

          <!-- Card 5: Incident Response -->
          <div animation="fade-three" data-wf--confidence-card--variant="base" class="confidence-card">
            <div class="confidence-card-visual">
              <div class="inc-widget">
                <div class="inc-top-row">
                  <span class="inc-tag">● CHAOS OUTAGE</span>
                  <span class="inc-clock">00:04:18</span>
                </div>
                <div class="inc-timeline">
                  <div class="inc-node">
                    <div class="inc-dot">✓</div>
                    <span>Injected</span>
                  </div>
                  <div class="inc-line"></div>
                  <div class="inc-node">
                    <div class="inc-dot">✓</div>
                    <span>Isolated</span>
                  </div>
                  <div class="inc-line active"></div>
                  <div class="inc-node">
                    <div class="inc-dot pulse">●</div>
                    <span>Mitigated</span>
                  </div>
                </div>
                <div class="inc-footer">
                  <span>Postmortem generated</span>
                  <span>89% composure</span>
                </div>
              </div>
            </div>
            <div class="confidence-card-btm-wrap">
              <div class="confidence-card-header">
                <h3 class="confidence-card-title">Incident Response</h3>
                <span class="confidence-score-badge">89%</span>
              </div>
              <p class="confidence-card-details">Maintains composure during outages with rapid triage and clear postmortems.</p>
            </div>
          </div>

          <!-- Card 6: Code Review -->
          <div animation="fade-three" data-wf--confidence-card--variant="blue" class="confidence-card w-variant-ca1e33b9-993c-a4af-99f2-8e46f98ff451">
            <div class="confidence-card-visual">
              <div class="cr-widget">
                <div class="cr-top-row">
                  <div class="cr-pr-pill">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="18" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><path d="M13 6h3a2 2 0 0 1 2 2v7M6 9v12"/></svg>
                    <span>PR #284 Critique</span>
                  </div>
                  <div class="cr-diff">
                    <span class="diff-plus">+48</span><span class="diff-minus">-12</span>
                  </div>
                </div>
                <div class="cr-checklist">
                  <div class="cr-check-row">
                    <span class="cr-icon-check">✓</span>
                    <span>AST Complexity: Low Debt</span>
                  </div>
                  <div class="cr-check-row">
                    <span class="cr-icon-check">✓</span>
                    <span>Async race condition caught</span>
                  </div>
                  <div class="cr-check-row">
                    <span class="cr-icon-check">✓</span>
                    <span>100% test coverage preserved</span>
                  </div>
                </div>
                <div class="cr-footer">
                  <span>Live commit diff benchmark</span>
                  <span>85% rigor</span>
                </div>
              </div>
            </div>
            <div class="confidence-card-btm-wrap">
              <div class="confidence-card-header">
                <h3 class="confidence-card-title">Code Review</h3>
                <span class="confidence-score-badge">85%</span>
              </div>
              <p class="confidence-card-details">Delivers thorough async PR critiques tied directly to live commit benchmarks.</p>
            </div>
          </div>

        </div></div></div></div></section>'''

    # Pattern to match the existing section confidence
    section_pattern = r'<section class=\"section confidence\">.*?</section>'
    if not re.search(section_pattern, content):
        print("ERROR: <section class=\"section confidence\"> not found!")
        return False

    content = re.sub(section_pattern, new_confidence_html, content, count=1)

    # Now add the enhanced CSS stylesheet before </head> if not already present
    css_content = '''<style id="confidence-enhanced-css">
/* ========================================================
   ENGINEERING INTELLIGENCE (CONFIDENCE) SECTION POLISH
   ======================================================== */
.section.confidence {
  position: relative;
  overflow: hidden;
  padding-top: var(--_gap---gap-12xl, 80px);
  padding-bottom: var(--_gap---gap-12xl, 80px);
}

.confidence-grid-wrap {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-gap: 20px;
  align-items: stretch;
}

/* Base Card Styling */
.confidence-card {
  min-height: 400px;
  height: 100%;
  padding: 24px;
  border-radius: 20px;
  background-color: #f7f6f2;
  border: 1px solid rgba(25, 24, 20, 0.08);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-sizing: border-box;
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.2s ease;
  position: relative;
  overflow: hidden;
}

.confidence-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 16px 36px -12px rgba(25, 24, 20, 0.08);
  border-color: rgba(25, 24, 20, 0.16);
}

/* Light Blue Card Variant */
.confidence-card.w-variant-ca1e33b9-993c-a4af-99f2-8e46f98ff451 {
  background-color: #edf5fe;
  border-color: rgba(37, 99, 235, 0.12);
}

.confidence-card.w-variant-ca1e33b9-993c-a4af-99f2-8e46f98ff451:hover {
  border-color: rgba(37, 99, 235, 0.25);
  box-shadow: 0 16px 36px -12px rgba(37, 99, 235, 0.1);
}

/* Micro-UI Asset Container */
.confidence-card-visual {
  width: 100%;
  height: 172px;
  border-radius: 14px;
  background-color: #ffffff;
  border: 1px solid rgba(25, 24, 20, 0.06);
  padding: 16px 14px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
  box-shadow: 0 2px 8px rgba(25, 24, 20, 0.03);
  user-select: none;
}

.confidence-card.w-variant-ca1e33b9-993c-a4af-99f2-8e46f98ff451 .confidence-card-visual {
  border-color: rgba(37, 99, 235, 0.1);
}

/* Card Bottom Content */
.confidence-card-btm-wrap {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 20px;
}

.confidence-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.confidence-card-title {
  font-family: var(--_font-family---primary-font, "Instrument Sans", sans-serif);
  font-size: 19px;
  font-weight: 600;
  color: #191814;
  letter-spacing: -0.02em;
  margin: 0;
  line-height: 1.25;
}

.confidence-score-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-family: var(--_font-family---secondary-font, "Space Mono", monospace);
  font-size: 12px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 999px;
  background-color: rgba(25, 24, 20, 0.06);
  color: #191814;
  white-space: nowrap;
  letter-spacing: -0.02em;
  flex-shrink: 0;
}

.confidence-card.w-variant-ca1e33b9-993c-a4af-99f2-8e46f98ff451 .confidence-score-badge {
  background-color: rgba(37, 99, 235, 0.1);
  color: #1d4ed8;
}

.confidence-card-details {
  font-family: var(--_font-family---primary-font, "Instrument Sans", sans-serif);
  font-size: 14px;
  line-height: 1.5;
  color: #585752;
  margin: 0;
}

/* Card 3: Radar Graphic Wrap */
.confidence-image-wrap {
  border-radius: 20px;
  overflow: hidden;
  border: 1px solid rgba(25, 24, 20, 0.08);
  box-shadow: 0 16px 40px -12px rgba(16, 24, 40, 0.08);
  background-color: #ffffff;
  display: flex;
  align-items: stretch;
  min-height: 400px;
  box-sizing: border-box;
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.confidence-image-wrap:hover {
  transform: translateY(-3px);
  box-shadow: 0 20px 48px -12px rgba(16, 24, 40, 0.12);
}

.confidence-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* Card 4: Five Dimensions Card */
.confidence-details-card {
  background-color: #ffffff;
  border-radius: 20px;
  border: 1px solid rgba(25, 24, 20, 0.08);
  padding: 30px 32px;
  box-shadow: 0 16px 40px -12px rgba(16, 24, 40, 0.06);
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 32px;
  min-height: 400px;
  box-sizing: border-box;
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.confidence-details-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 20px 48px -12px rgba(16, 24, 40, 0.1);
}

.confidence-details-wrap {
  flex: 1 1 50%;
  max-width: none;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.confidence-details-headline {
  font-family: var(--_font-family---primary-font, "Instrument Sans", sans-serif);
  font-size: 24px;
  font-weight: 600;
  line-height: 1.25;
  margin: 0 0 12px 0;
  color: #191814;
  letter-spacing: -0.02em;
}

.confidence-details-desc {
  font-family: var(--_font-family---primary-font, "Instrument Sans", sans-serif);
  font-size: 14.5px;
  line-height: 1.55;
  color: #585752;
  margin: 0 0 18px 0;
}

.confidence-evidence-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-family: var(--_font-family---secondary-font, "Space Mono", monospace);
  font-size: 12px;
  color: #166534;
  background-color: #dcfce7;
  padding: 5px 12px;
  border-radius: 999px;
  width: fit-content;
  border: 1px solid rgba(22, 101, 52, 0.15);
}

/* Dimensions Scorecard in Card 4 */
.confidence-dimensions-list {
  flex: 1 1 50%;
  display: flex;
  flex-direction: column;
  gap: 11px;
  background-color: #f7f6f2;
  border-radius: 14px;
  padding: 18px 20px;
  border: 1px solid rgba(25, 24, 20, 0.06);
}

.dim-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.dim-name {
  font-family: var(--_font-family---primary-font, "Instrument Sans", sans-serif);
  font-size: 13px;
  font-weight: 500;
  color: #2b2a27;
  min-width: 135px;
}

.dim-bar-wrap {
  flex: 1;
  height: 6px;
  background-color: rgba(25, 24, 20, 0.08);
  border-radius: 999px;
  overflow: hidden;
}

.dim-bar-fill {
  height: 100%;
  border-radius: 999px;
  background-color: #191814;
}

.dim-bar-fill.blue {
  background-color: #2563eb;
}

.dim-bar-fill.green {
  background-color: #10b981;
}

.dim-val {
  font-family: var(--_font-family---secondary-font, "Space Mono", monospace);
  font-size: 12px;
  font-weight: 600;
  color: #191814;
  min-width: 32px;
  text-align: right;
}

/* Micro-Telemetry Widgets */
/* 1. Architecture Topology */
.arch-topology-widget {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.arch-top-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 6px;
  border-bottom: 1px solid rgba(25, 24, 20, 0.06);
}
.arch-tag {
  font-family: var(--_font-family---secondary-font, "Space Mono", monospace);
  font-size: 10px;
  color: #71716b;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.arch-pulse {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-family: var(--_font-family---secondary-font, "Space Mono", monospace);
  font-size: 10.5px;
  color: #059669;
  font-weight: 600;
}
.pulse-dot-green {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: #10b981;
  display: inline-block;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
}
.arch-canvas {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
  padding: 6px 0;
}
.arch-node-gateway {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  background-color: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: 6px;
  font-family: var(--_font-family---secondary-font, "Space Mono", monospace);
  font-size: 11px;
  color: #166534;
  font-weight: 600;
}
.arch-connector-svg {
  width: 100%;
  height: 20px;
  margin: 2px 0;
}
.arch-pods-row {
  display: flex;
  width: 100%;
  justify-content: space-between;
  gap: 6px;
}
.arch-pod {
  flex: 1;
  background-color: #faf9f6;
  border: 1px solid rgba(25, 24, 20, 0.08);
  border-radius: 6px;
  padding: 4px 6px;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 1px;
}
.arch-pod span {
  font-family: var(--_font-family---primary-font, "Instrument Sans", sans-serif);
  font-size: 11px;
  font-weight: 600;
  color: #191814;
}
.arch-pod small {
  font-family: var(--_font-family---secondary-font, "Space Mono", monospace);
  font-size: 9.5px;
  color: #71716b;
}

/* 2. Root-Cause Speed Widget */
.rca-widget {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.rca-top-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 6px;
  border-bottom: 1px solid rgba(37, 99, 235, 0.08);
}
.rca-tag {
  font-family: var(--_font-family---secondary-font, "Space Mono", monospace);
  font-size: 10px;
  color: #2563eb;
  font-weight: 600;
  letter-spacing: 0.03em;
}
.rca-iso-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-family: var(--_font-family---secondary-font, "Space Mono", monospace);
  font-size: 10.5px;
  color: #059669;
  font-weight: 600;
}
.rca-compare-box {
  background-color: #f8fafc;
  border: 1px solid rgba(37, 99, 235, 0.1);
  border-radius: 10px;
  padding: 10px 12px;
  display: flex;
  align-items: center;
  justify-content: space-around;
  margin: 4px 0;
}
.rca-metric-col {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}
.rca-num-old {
  font-family: var(--_font-family---secondary-font, "Space Mono", monospace);
  font-size: 16px;
  font-weight: 600;
  color: #94a3b8;
  text-decoration: line-through;
}
.rca-num-new {
  font-family: var(--_font-family---secondary-font, "Space Mono", monospace);
  font-size: 18px;
  font-weight: 700;
  color: #10b981;
}
.rca-metric-col small {
  font-family: var(--_font-family---primary-font, "Instrument Sans", sans-serif);
  font-size: 11px;
  color: #64748b;
}
.rca-bottom-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-family: var(--_font-family---secondary-font, "Space Mono", monospace);
  font-size: 10.5px;
  color: #1e40af;
  background-color: #eff6ff;
  padding: 4px 8px;
  border-radius: 6px;
}

/* 3. Incident Response Widget */
.inc-widget {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.inc-top-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 6px;
  border-bottom: 1px solid rgba(25, 24, 20, 0.06);
}
.inc-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-family: var(--_font-family---secondary-font, "Space Mono", monospace);
  font-size: 10px;
  color: #b45309;
  font-weight: 600;
  background-color: #fef3c7;
  padding: 2px 6px;
  border-radius: 4px;
}
.inc-clock {
  font-family: var(--_font-family---secondary-font, "Space Mono", monospace);
  font-size: 11px;
  color: #191814;
  font-weight: 600;
}
.inc-timeline {
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  padding: 8px 4px;
}
.inc-node {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  z-index: 2;
}
.inc-dot {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background-color: #10b981;
  color: #ffffff;
  font-size: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}
.inc-dot.pulse {
  background-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.2);
}
.inc-node span {
  font-family: var(--_font-family---primary-font, "Instrument Sans", sans-serif);
  font-size: 10.5px;
  color: #4b5563;
  font-weight: 500;
}
.inc-line {
  flex: 1;
  height: 2px;
  background-color: #10b981;
  margin: 0 4px 18px 4px;
}
.inc-line.active {
  background-color: #2563eb;
}
.inc-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-family: var(--_font-family---secondary-font, "Space Mono", monospace);
  font-size: 10.5px;
  color: #166534;
  background-color: #f0fdf4;
  padding: 4px 8px;
  border-radius: 6px;
  border: 1px solid #dcfce7;
}

/* 4. Code Review Diff Widget */
.cr-widget {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.cr-top-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 6px;
  border-bottom: 1px solid rgba(37, 99, 235, 0.08);
}
.cr-pr-pill {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-family: var(--_font-family---secondary-font, "Space Mono", monospace);
  font-size: 10.5px;
  color: #1d4ed8;
  font-weight: 600;
}
.cr-diff {
  font-family: var(--_font-family---secondary-font, "Space Mono", monospace);
  font-size: 10.5px;
  font-weight: 600;
}
.diff-plus { color: #10b981; }
.diff-minus { color: #ef4444; margin-left: 2px; }
.cr-checklist {
  display: flex;
  flex-direction: column;
  gap: 5px;
  padding: 4px 0;
}
.cr-check-row {
  display: flex;
  align-items: center;
  gap: 6px;
  font-family: var(--_font-family---primary-font, "Instrument Sans", sans-serif);
  font-size: 11.5px;
  color: #334155;
}
.cr-icon-check {
  color: #10b981;
  font-weight: 700;
  font-size: 12px;
}
.cr-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-family: var(--_font-family---secondary-font, "Space Mono", monospace);
  font-size: 10.5px;
  color: #1e40af;
  background-color: #eff6ff;
  padding: 4px 8px;
  border-radius: 6px;
}

/* Responsive Breakpoints */
@media screen and (max-width: 991px) {
  .confidence-grid-wrap {
    grid-template-columns: 1fr 1fr !important;
    grid-gap: 18px;
  }
  .confidence-card,
  .confidence-image-wrap,
  .confidence-details-card {
    min-height: 360px;
  }
  .confidence-details-card {
    flex-direction: column;
    align-items: stretch;
    padding: 24px;
    gap: 20px;
  }
  .confidence-dimensions-list {
    width: 100%;
    box-sizing: border-box;
  }
}

@media screen and (max-width: 767px) {
  .confidence-grid-wrap {
    grid-template-columns: 1fr !important;
    grid-gap: 16px;
  }
  .confidence-card,
  .confidence-image-wrap,
  .confidence-details-card {
    min-height: auto;
    padding: 20px;
  }
  .confidence-card-visual {
    height: 155px;
  }
  .confidence-details-card {
    padding: 20px;
  }
}
</style>'''

    if 'id="confidence-enhanced-css"' in content:
        # Replace existing
        content = re.sub(r'<style id="confidence-enhanced-css">.*?</style>', css_content, content, flags=re.DOTALL)
    else:
        # Insert right before </head>
        content = content.replace('</head>', css_content + '\n</head>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Successfully updated about/index.html with enhanced confidence section and CSS!")
    return True

if __name__ == '__main__':
    update_confidence_section()
