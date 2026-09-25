<template>
  <div class="light-enterprise-home">
    <!-- Header Navigation (Public Information Architecture: Strictly NO signup/login) -->
    <header class="app-header">
      <div class="header-left">
        <a href="#hero" class="brand" @click.prevent="scrollToSection('hero')">
          {{ $t('nav.brand') }}
        </a>
      </div>

      <nav class="header-center" aria-label="Main Navigation">
        <a href="#simulation" class="nav-item" @click.prevent="scrollToSection('simulation')">{{ $t('nav.simulation') }}</a>
        <a href="#use-cases" class="nav-item" @click.prevent="scrollToSection('use-cases')">{{ $t('nav.useCases') }}</a>
        <a href="#research" class="nav-item" @click.prevent="scrollToSection('research')">{{ $t('nav.research') }}</a>
        <a href="#about" class="nav-item" @click.prevent="scrollToSection('about')">{{ $t('nav.about') }}</a>
      </nav>

      <div class="header-right">
        <LanguageSwitcher />
        <div class="step-divider" aria-hidden="true"></div>
        <a 
          href="https://github.com/satyamhq/synthetic-minds" 
          target="_blank" 
          rel="noopener noreferrer" 
          class="github-link"
          aria-label="GitHub Repository"
        >
          {{ $t('nav.github') }}
        </a>
        <button class="header-btn secondary" @click="openConsultModal">
          {{ $t('nav.contact') }}
        </button>
        <button class="header-btn primary" @click="scrollToSection('simulation')">
          {{ $t('nav.explore') }}
        </button>

        <!-- Mobile Menu Toggle -->
        <button 
          class="mobile-menu-btn" 
          :class="{ 'active': isMobileMenuOpen }" 
          @click="isMobileMenuOpen = !isMobileMenuOpen"
          aria-label="Toggle Navigation"
        >
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>

      <!-- Mobile Dropdown Menu -->
      <div v-if="isMobileMenuOpen" class="mobile-dropdown">
        <a href="#simulation" class="mobile-item" @click="handleMobileNav('simulation')">{{ $t('nav.simulation') }}</a>
        <a href="#use-cases" class="mobile-item" @click="handleMobileNav('use-cases')">{{ $t('nav.useCases') }}</a>
        <a href="#research" class="mobile-item" @click="handleMobileNav('research')">{{ $t('nav.research') }}</a>
        <a href="#about" class="mobile-item" @click="handleMobileNav('about')">{{ $t('nav.about') }}</a>
        <a 
          href="https://github.com/satyamhq/synthetic-minds" 
          target="_blank" 
          rel="noopener noreferrer" 
          class="mobile-item"
        >
          {{ $t('nav.github') }} ↗
        </a>
        <div class="mobile-actions">
          <button class="mobile-btn" @click="handleMobileConsult">{{ $t('nav.contact') }}</button>
          <button class="mobile-btn dark" @click="handleMobileNav('simulation')">{{ $t('nav.explore') }}</button>
        </div>
      </div>
    </header>

    <!-- Main Content Container -->
    <main class="page-container">
      <!-- 1. Hero Section -->
      <section id="hero" class="hero-section">
        <div class="hero-inner">
          <div class="eyebrow-tag">
            {{ $t('home.eyebrow') }}
          </div>

          <h1 class="hero-headline">
            {{ $t('home.title') }}
          </h1>

          <p class="hero-supporting">
            {{ $t('home.subtitle') }}
          </p>

          <div class="hero-cta-row">
            <button class="btn-black" @click="scrollToSection('simulation')">
              {{ $t('home.primaryCta') }}
            </button>
            <button class="btn-white" @click="scrollToSection('how-it-works')">
              {{ $t('home.secondaryCta') }}
            </button>
            <a 
              href="https://github.com/satyamhq/synthetic-minds" 
              target="_blank" 
              rel="noopener noreferrer" 
              class="hero-github-link"
            >
              {{ $t('home.viewGithub') }}
            </a>
          </div>

          <!-- Hero Inquiry Preview Card (Aaru-inspired minimalist decision console, zero technical jargon) -->
          <div class="hero-inquiry-card">
            <div class="inquiry-card-header">
              <div class="inquiry-status">
                <span class="status-dot"></span>
                <span class="mono-label">DECISION SIMULATION ENVIRONMENT</span>
              </div>
              <span class="inquiry-badge">AUTONOMOUS POPULATIONS</span>
            </div>
            <div class="inquiry-body">
              <div class="inquiry-prompt-row">
                <span class="inquiry-prompt-prefix">SAMPLE INQUIRY</span>
                <span class="inquiry-prompt-text">"How might enterprise buyers respond if annual seat pricing increases by 18% during contract renewal?"</span>
              </div>
              <div class="inquiry-response-grid">
                <div class="response-chip">
                  <div class="chip-top">
                    <span class="chip-dot"></span>
                    <span class="chip-label">COHORT 01 — CORE ENTERPRISE</span>
                  </div>
                  <span class="chip-val">Low churn risk; 82% retention under multi-year stability commitments</span>
                </div>
                <div class="response-chip highlight">
                  <div class="chip-top">
                    <span class="chip-dot orange"></span>
                    <span class="chip-label">COHORT 02 — MID-MARKET GROWTH</span>
                  </div>
                  <span class="chip-val">Sensitivity spike; 34% substitution friction toward self-hosted alternatives</span>
                </div>
              </div>
            </div>
            <div class="inquiry-footer">
              <span class="inquiry-footnote">Model-based behavioral exploration across synthetic demographic cohorts</span>
              <button class="inquiry-action-link" @click="scrollToSection('simulation')">
                Explore in Studio ↓
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- 2. The Problem Section -->
      <section id="problem" class="content-section border-top">
        <div class="section-grid-2col">
          <div class="section-col-left">
            <span class="section-pill">{{ $t('home.problem.tag') }}</span>
            <h2 class="section-title">{{ $t('home.problem.title') }}</h2>
          </div>
          <div class="section-col-right">
            <p class="body-lead">{{ $t('home.problem.lead') }}</p>
            <div class="limitations-grid">
              <div class="limitation-item">
                <span class="limit-num">01</span>
                <h4 class="limit-title">Surveys & Focus Groups</h4>
                <p class="limit-desc">Capture declared intent in an artificial questionnaire setting—frequently disconnecting from actual choice under real trade-offs and peer dynamics.</p>
              </div>
              <div class="limitation-item">
                <span class="limit-num">02</span>
                <h4 class="limit-title">Historical Analytics</h4>
                <p class="limit-desc">Record what occurred under previous conditions that may no longer apply once pricing, competitor strategies, or market narratives change.</p>
              </div>
              <div class="limitation-item">
                <span class="limit-num">03</span>
                <h4 class="limit-title">Static Assumptions</h4>
                <p class="limit-desc">Treat target audiences as passive spreadsheets rather than adaptive networks of individuals responding to shifting variables.</p>
              </div>
              <div class="limitation-item">
                <span class="limit-num">04</span>
                <h4 class="limit-title">Stated Preferences</h4>
                <p class="limit-desc">Miss the emergent behavioral cascades, viral skepticism, and adoption inertia that determine real-world market outcomes.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 3. Core Positioning & The Core Idea -->
      <section id="positioning" class="content-section border-top bg-subtle">
        <div class="section-grid-2col">
          <div class="section-col-left">
            <span class="section-pill">{{ $t('home.coreIdea.tag') }}</span>
            <h2 class="section-title">{{ $t('home.coreIdea.title') }}</h2>
          </div>
          <div class="section-col-right">
            <p class="body-lead">{{ $t('home.coreIdea.copy') }}</p>
            
            <!-- Real-world context → Synthetic population → Environment → Scenario → AI agents → Behavior → Insights -->
            <div class="core-flow-container">
              <div class="core-flow-header">
                <span class="mono-label">BEHAVIORAL SIMULATION PIPELINE</span>
              </div>
              <div class="core-flow-steps">
                <div class="core-step">
                  <span class="core-step-badge">01</span>
                  <span class="core-step-text">{{ $t('home.coreIdea.flow.s1') }}</span>
                </div>
                <span class="core-arrow">→</span>
                <div class="core-step">
                  <span class="core-step-badge">02</span>
                  <span class="core-step-text">{{ $t('home.coreIdea.flow.s2') }}</span>
                </div>
                <span class="core-arrow">→</span>
                <div class="core-step">
                  <span class="core-step-badge">03</span>
                  <span class="core-step-text">{{ $t('home.coreIdea.flow.s3') }}</span>
                </div>
                <span class="core-arrow">→</span>
                <div class="core-step">
                  <span class="core-step-badge">04</span>
                  <span class="core-step-text">{{ $t('home.coreIdea.flow.s4') }}</span>
                </div>
                <span class="core-arrow">→</span>
                <div class="core-step">
                  <span class="core-step-badge">05</span>
                  <span class="core-step-text">{{ $t('home.coreIdea.flow.s5') }}</span>
                </div>
                <span class="core-arrow">→</span>
                <div class="core-step">
                  <span class="core-step-badge">06</span>
                  <span class="core-step-text">{{ $t('home.coreIdea.flow.s6') }}</span>
                </div>
                <span class="core-arrow">→</span>
                <div class="core-step highlight">
                  <span class="core-step-badge">07</span>
                  <span class="core-step-text">{{ $t('home.coreIdea.flow.s7') }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 4. How It Works Section (4 Disciplined Steps) -->
      <section id="how-it-works" class="content-section border-top">
        <div class="section-head-center">
          <span class="section-pill">{{ $t('home.howItWorks.tag') }}</span>
          <h2 class="section-title">{{ $t('home.howItWorks.title') }}</h2>
          <p class="section-subtitle">{{ $t('home.howItWorks.subtitle') }}</p>
        </div>

        <div class="how-it-works-grid">
          <div class="step-card">
            <div class="step-card-num">01</div>
            <h3 class="step-card-title">{{ $t('home.howItWorks.step01Title') }}</h3>
            <p class="step-card-desc">{{ $t('home.howItWorks.step01Desc') }}</p>
          </div>

          <div class="step-card">
            <div class="step-card-num">02</div>
            <h3 class="step-card-title">{{ $t('home.howItWorks.step02Title') }}</h3>
            <p class="step-card-desc">{{ $t('home.howItWorks.step02Desc') }}</p>
          </div>

          <div class="step-card">
            <div class="step-card-num">03</div>
            <h3 class="step-card-title">{{ $t('home.howItWorks.step03Title') }}</h3>
            <p class="step-card-desc">{{ $t('home.howItWorks.step03Desc') }}</p>
          </div>

          <div class="step-card">
            <div class="step-card-num">04</div>
            <h3 class="step-card-title">{{ $t('home.howItWorks.step04Title') }}</h3>
            <p class="step-card-desc">{{ $t('home.howItWorks.step04Desc') }}</p>
          </div>
        </div>
      </section>

      <!-- 5. Use Cases Section (8 Authentic Areas with Real Questions) -->
      <section id="use-cases" class="content-section border-top bg-subtle">
        <div class="section-head-center">
          <span class="section-pill">{{ $t('home.useCases.tag') }}</span>
          <h2 class="section-title">{{ $t('home.useCases.title') }}</h2>
          <p class="section-subtitle">{{ $t('home.useCases.subtitle') }}</p>
        </div>

        <div class="use-cases-grid">
          <div 
            v-for="(uc, idx) in useCasesList" 
            :key="idx" 
            class="use-case-card"
          >
            <div class="uc-header">
              <span class="uc-tag">{{ uc.tag }}</span>
              <h3 class="uc-title">{{ $t(uc.titleKey) }}</h3>
            </div>
            <p class="uc-desc">{{ $t(uc.descKey) }}</p>
            <div class="uc-inquiry-box" @click="loadUseCaseQuestion(uc)">
              <span class="uc-inquiry-tag">INQUIRY</span>
              <p class="uc-inquiry-text">“{{ $t(uc.qKey) }}”</p>
              <span class="uc-inquiry-cta">Test this scenario ↗</span>
            </div>
          </div>
        </div>
      </section>

      <!-- 6. Questions Section (Decision Inquiries) -->
      <section id="questions" class="content-section border-top">
        <div class="section-head-center">
          <span class="section-pill">{{ $t('home.questions.tag') }}</span>
          <h2 class="section-title">{{ $t('home.questions.title') }}</h2>
          <p class="section-subtitle">{{ $t('home.questions.subtitle') }}</p>
        </div>

        <div class="questions-grid">
          <div 
            v-for="(item, idx) in questionsList" 
            :key="idx" 
            class="question-pill-card"
            @click="loadQuestionIntoStudio(item)"
          >
            <div class="q-icon">?</div>
            <div class="q-content">
              <div class="q-category">{{ item.category }}</div>
              <h3 class="q-title">{{ $t(item.q) }}</h3>
              <p class="q-desc">{{ $t(item.a) }}</p>
            </div>
            <div class="q-arrow" aria-hidden="true">↗</div>
          </div>
        </div>
      </section>

      <!-- 7. Differentiation Section -->
      <section id="differentiation" class="content-section border-top bg-subtle">
        <div class="section-head-center">
          <span class="section-pill">{{ $t('home.differentiation.tag') }}</span>
          <h2 class="section-title">{{ $t('home.differentiation.headline') }}</h2>
          <p class="section-subtitle">{{ $t('home.differentiation.subtitle') }}</p>
        </div>

        <div class="differentiation-grid">
          <!-- Card 1: Surveys -->
          <div class="diff-card">
            <div class="diff-header">
              <span class="diff-num">01</span>
              <span class="diff-type muted">{{ $t('home.differentiation.card1Type') }}</span>
            </div>
            <h3 class="diff-title">{{ $t('home.differentiation.card1Title') }}</h3>
            <p class="diff-desc">{{ $t('home.differentiation.card1Desc') }}</p>
          </div>

          <!-- Card 2: Analytics -->
          <div class="diff-card">
            <div class="diff-header">
              <span class="diff-num">02</span>
              <span class="diff-type muted">{{ $t('home.differentiation.card2Type') }}</span>
            </div>
            <h3 class="diff-title">{{ $t('home.differentiation.card2Title') }}</h3>
            <p class="diff-desc">{{ $t('home.differentiation.card2Desc') }}</p>
          </div>

          <!-- Card 3: Simulation -->
          <div class="diff-card active-diff">
            <div class="diff-header">
              <span class="diff-num">03</span>
              <span class="diff-type highlight">{{ $t('home.differentiation.card3Type') }}</span>
            </div>
            <h3 class="diff-title">{{ $t('home.differentiation.card3Title') }}</h3>
            <p class="diff-desc">{{ $t('home.differentiation.card3Desc') }}</p>
          </div>
        </div>

        <div class="disclaimer-banner">
          <span class="disclaimer-badge">NOTE</span>
          <p class="disclaimer-text">{{ $t('home.differentiation.disclaimer') }}</p>
        </div>
      </section>

      <!-- 8. Simulation Section (Visual Flow + Studio Workbench) -->
      <section id="simulation" class="content-section border-top">
        <div class="section-head-center">
          <span class="section-pill">{{ $t('home.simulationStudio.tag') }}</span>
          <h2 class="section-title">{{ $t('home.simulationStudio.title') }}</h2>
          <p class="section-subtitle">{{ $t('home.simulationStudio.subtitle') }}</p>
        </div>

        <!-- Visual Flow: Real-World Data → Population → Environment → Scenario → AI Agents → Behavior → Insights -->
        <div class="simulation-pipeline-card">
          <div class="pipeline-header">
            <span class="mono-label">{{ $t('home.visualFlow.tag') }}</span>
            <span class="pipeline-status">
              <span class="status-dot"></span> Active Simulation Flow
            </span>
          </div>
          
          <div class="pipeline-steps">
            <div 
              v-for="(step, sIdx) in flowSteps" 
              :key="sIdx" 
              class="pipeline-step-wrap"
            >
              <div 
                class="pipeline-step"
                :class="{ 
                  'decision-step': sIdx === 6, 
                  'active-step': activeFlowStep === sIdx 
                }"
                @mouseenter="activeFlowStep = sIdx"
                @click="activeFlowStep = sIdx"
              >
                <span class="step-badge" :class="{ 'decision-badge': sIdx === 6 }">0{{ sIdx + 1 }}</span>
                <span class="step-name" :class="{ 'decision-name': sIdx === 6 }">{{ $t(step.labelKey) }}</span>
              </div>
              <div v-if="sIdx < flowSteps.length - 1" class="pipeline-arrow" aria-hidden="true">→</div>
            </div>
          </div>

          <!-- Interactive Step Inspector -->
          <div class="pipeline-detail-bar">
            <span class="detail-badge">STEP 0{{ activeFlowStep + 1 }}</span>
            <span class="detail-label">{{ $t(flowSteps[activeFlowStep].labelKey) }}:</span>
            <span class="detail-text">{{ $t(flowSteps[activeFlowStep].descKey) }}</span>
          </div>
        </div>

        <div class="studio-container">
          <div class="studio-card">
            <!-- Scenario Prompt Textarea -->
            <div class="studio-field">
              <div class="field-header">
                <label class="field-label" for="studio-requirement-input">{{ $t('home.simulationStudio.promptLabel') }}</label>
                <span class="field-badge required">Required</span>
              </div>
              <textarea 
                id="studio-requirement-input"
                v-model="formData.simulationRequirement"
                class="studio-textarea"
                rows="4"
                :placeholder="$t('home.simulationStudio.promptPlaceholder')"
              ></textarea>
            </div>

            <!-- Optional File Upload Dropzone -->
            <div class="studio-field">
              <div class="field-header">
                <label class="field-label">{{ $t('home.simulationStudio.uploadLabel') }}</label>
                <span class="field-badge optional">{{ $t('home.simulationStudio.noFilesNote') }}</span>
              </div>
              <p class="field-subtext">{{ $t('home.simulationStudio.uploadSubtext') }}</p>

              <div 
                class="dropzone"
                :class="{ 'drag-over': isDragOver }"
                @click="triggerFileInput"
                @dragover.prevent="isDragOver = true"
                @dragleave.prevent="isDragOver = false"
                @drop.prevent="handleDrop"
                role="button"
                tabindex="0"
                aria-label="Upload files dropzone"
                @keydown.enter="triggerFileInput"
              >
                <input 
                  type="file" 
                  ref="fileInput" 
                  multiple 
                  accept=".pdf,.md,.txt" 
                  class="hidden-file-input" 
                  @change="handleFileSelect"
                />
                <div class="dropzone-inner">
                  <div class="upload-icon" aria-hidden="true">↑</div>
                  <div class="drop-text">{{ $t('home.simulationStudio.dragToUpload') }}</div>
                  <div class="drop-types">PDF, Markdown, TXT (optional context)</div>
                </div>
              </div>

              <!-- Selected Files List -->
              <div v-if="files.length > 0" class="file-list">
                <div class="file-list-title">
                  {{ $t('home.simulationStudio.selectedFiles', { count: files.length }) }}
                </div>
                <div v-for="(file, idx) in files" :key="idx" class="file-item">
                  <span class="file-name">{{ file.name }}</span>
                  <button type="button" class="file-remove" @click="removeFile(idx)" aria-label="Remove file">✕</button>
                </div>
              </div>
            </div>

            <!-- Studio Action Bar -->
            <div class="studio-actions">
              <button 
                class="studio-launch-btn"
                :disabled="!canSubmit || loading"
                @click="startSimulation"
              >
                <span v-if="!loading">{{ $t('home.simulationStudio.startEngine') }}</span>
                <span v-else>{{ $t('home.simulationStudio.initializing') }}</span>
              </button>
            </div>
          </div>

          <!-- History Database Component -->
          <div class="studio-history-card">
            <div class="history-card-header">
              <span class="mono-label">{{ $t('home.simulationStudio.recentSimulations') }}</span>
            </div>
            <HistoryDatabase />
          </div>
        </div>
      </section>

      <!-- 9. Research & Scientific Integrity Section -->
      <section id="research" class="content-section border-top bg-subtle">
        <div class="section-grid-2col">
          <div class="section-col-left">
            <span class="section-pill">{{ $t('home.research.tag') }}</span>
            <h2 class="section-title">{{ $t('home.research.title') }}</h2>
          </div>
          <div class="section-col-right">
            <p class="body-lead">{{ $t('home.research.copy') }}</p>
            <div class="research-pillars">
              <div class="pillar-item">
                <h4 class="pillar-title">{{ $t('home.research.point1Title') }}</h4>
                <p class="pillar-desc">{{ $t('home.research.point1Desc') }}</p>
              </div>
              <div class="pillar-item">
                <h4 class="pillar-title">{{ $t('home.research.point2Title') }}</h4>
                <p class="pillar-desc">{{ $t('home.research.point2Desc') }}</p>
              </div>
              <div class="pillar-item">
                <h4 class="pillar-title">{{ $t('home.research.point3Title') }}</h4>
                <p class="pillar-desc">{{ $t('home.research.point3Desc') }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 10. About Section -->
      <section id="about" class="content-section border-top">
        <div class="section-grid-2col">
          <div class="section-col-left">
            <span class="section-pill">{{ $t('home.about.tag') }}</span>
            <h2 class="section-title">{{ $t('home.about.title') }}</h2>
          </div>
          <div class="section-col-right">
            <p class="body-lead">{{ $t('home.about.copy') }}</p>
          </div>
        </div>
      </section>

      <!-- 11. Final Call to Action -->
      <section class="content-section border-top bg-subtle">
        <div class="cta-banner">
          <h2 class="cta-title">{{ $t('home.cta.title') }}</h2>
          <p class="cta-subtitle">{{ $t('home.cta.supporting') }}</p>
          <div class="cta-buttons">
            <button class="btn-black" @click="scrollToSection('simulation')">
              {{ $t('home.cta.primary') }}
            </button>
            <button class="btn-white" @click="openConsultModal">
              {{ $t('home.cta.secondary') }}
            </button>
          </div>
        </div>
      </section>
    </main>

    <!-- Footer -->
    <footer class="app-footer">
      <div class="footer-grid">
        <div class="footer-col-brand">
          <div class="footer-brand">{{ $t('nav.brand') }}</div>
          <p class="footer-tagline">{{ $t('home.title') }}</p>
          <p class="footer-desc">{{ $t('meta.description') }}</p>
        </div>

        <div class="footer-col">
          <div class="footer-col-title">{{ $t('nav.simulation') }}</div>
          <a href="#simulation" @click.prevent="scrollToSection('simulation')">{{ $t('home.simulationStudio.title') }}</a>
          <a href="#how-it-works" @click.prevent="scrollToSection('how-it-works')">{{ $t('nav.howItWorks') }}</a>
          <a href="#questions" @click.prevent="scrollToSection('questions')">{{ $t('home.questions.tag') }}</a>
        </div>

        <div class="footer-col">
          <div class="footer-col-title">{{ $t('nav.useCases') }}</div>
          <a href="#use-cases" @click.prevent="scrollToSection('use-cases')">{{ $t('home.useCases.c1Title') }}</a>
          <a href="#use-cases" @click.prevent="scrollToSection('use-cases')">{{ $t('home.useCases.c2Title') }}</a>
          <a href="#use-cases" @click.prevent="scrollToSection('use-cases')">{{ $t('home.useCases.c5Title') }}</a>
        </div>

        <div class="footer-col">
          <div class="footer-col-title">{{ $t('nav.about') }}</div>
          <a href="#about" @click.prevent="scrollToSection('about')">{{ $t('nav.about') }}</a>
          <a href="#research" @click.prevent="scrollToSection('research')">{{ $t('nav.research') }}</a>
          <a href="#contact" @click.prevent="openConsultModal">{{ $t('nav.contact') }}</a>
          <a href="https://github.com/satyamhq/synthetic-minds" target="_blank" rel="noopener noreferrer">{{ $t('nav.github') }}</a>
        </div>
      </div>

      <div class="footer-bottom">
        <div class="copyright">
          © {{ currentYear }} SYNTHETIC MINDS. All rights reserved.
        </div>
        <div class="footer-links">
          <span>AI Simulation for Complex Decisions</span>
        </div>
      </div>
    </footer>

    <!-- Contact / Briefing Modal -->
    <div v-if="showConsultModal" class="modal-overlay" @click="closeConsultModal" role="dialog" aria-modal="true" aria-labelledby="consult-modal-title">
      <div class="modal-dialog" @click.stop>
        <button class="modal-close" @click="closeConsultModal" aria-label="Close modal">×</button>

        <div v-if="!consultSubmitted">
          <div class="modal-head">
            <h3 id="consult-modal-title" class="modal-title">{{ $t('home.contactModal.title') }}</h3>
            <p class="modal-sub">{{ $t('home.contactModal.subtitle') }}</p>
          </div>

          <form class="modal-form" @submit.prevent="submitConsultRequest">
            <div class="form-field">
              <label for="consult-name">{{ $t('home.contactModal.nameLabel') }} *</label>
              <input id="consult-name" v-model="consultForm.name" type="text" required placeholder="Alex Miller" />
            </div>

            <div class="form-field">
              <label for="consult-email">{{ $t('home.contactModal.emailLabel') }} *</label>
              <input id="consult-email" v-model="consultForm.email" type="email" required placeholder="alex@organization.com" />
            </div>

            <div class="form-field">
              <label for="consult-company">{{ $t('home.contactModal.companyLabel') }} *</label>
              <input id="consult-company" v-model="consultForm.company" type="text" required placeholder="Organization Name" />
            </div>

            <div class="form-field">
              <label for="consult-objective">{{ $t('home.contactModal.objectiveLabel') }} *</label>
              <textarea id="consult-objective" v-model="consultForm.objective" rows="3" required placeholder="Describe your decision scenario or research objectives..."></textarea>
            </div>

            <button type="submit" class="modal-submit-btn" :disabled="isSubmittingConsult">
              <span v-if="!isSubmittingConsult">{{ $t('home.contactModal.submit') }}</span>
              <span v-else>{{ $t('home.contactModal.submitting') }}</span>
            </button>
          </form>
        </div>

        <div v-else class="modal-success">
          <div class="success-icon" aria-hidden="true">✓</div>
          <h3>{{ $t('home.contactModal.successTitle') }}</h3>
          <p>{{ $t('home.contactModal.successDesc') }}</p>
          <button class="modal-submit-btn" @click="closeConsultModal">
            {{ $t('home.contactModal.close') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import HistoryDatabase from '../components/HistoryDatabase.vue'
import LanguageSwitcher from '../components/LanguageSwitcher.vue'
import { setPendingUpload } from '../store/pendingUpload'

const { t } = useI18n()
const router = useRouter()
const currentYear = new Date().getFullYear()

// Navigation & Mobile menu
const isMobileMenuOpen = ref(false)
const scrollToSection = (id) => {
  const el = document.getElementById(id)
  if (el) {
    el.scrollIntoView({ behavior: 'smooth' })
  }
}
const handleMobileNav = (id) => {
  isMobileMenuOpen.value = false
  scrollToSection(id)
}
const handleMobileConsult = () => {
  isMobileMenuOpen.value = false
  openConsultModal()
}

// Visual Flow Steps (Real-World Data → Population → Environment → Scenario → AI Agents → Behavior → Insights)
const activeFlowStep = ref(0)
const flowSteps = [
  { labelKey: 'home.visualFlow.step1', descKey: 'home.visualFlow.step1Desc' },
  { labelKey: 'home.visualFlow.step2', descKey: 'home.visualFlow.step2Desc' },
  { labelKey: 'home.visualFlow.step3', descKey: 'home.visualFlow.step3Desc' },
  { labelKey: 'home.visualFlow.step4', descKey: 'home.visualFlow.step4Desc' },
  { labelKey: 'home.visualFlow.step5', descKey: 'home.visualFlow.step5Desc' },
  { labelKey: 'home.visualFlow.step6', descKey: 'home.visualFlow.step6Desc' },
  { labelKey: 'home.visualFlow.step7', descKey: 'home.visualFlow.step7Desc' }
]

// Use Cases List with investigation questions
const useCasesList = [
  { tag: '01', titleKey: 'home.useCases.c1Title', descKey: 'home.useCases.c1Desc', qKey: 'home.useCases.c1Q' },
  { tag: '02', titleKey: 'home.useCases.c2Title', descKey: 'home.useCases.c2Desc', qKey: 'home.useCases.c2Q' },
  { tag: '03', titleKey: 'home.useCases.c3Title', descKey: 'home.useCases.c3Desc', qKey: 'home.useCases.c3Q' },
  { tag: '04', titleKey: 'home.useCases.c4Title', descKey: 'home.useCases.c4Desc', qKey: 'home.useCases.c4Q' },
  { tag: '05', titleKey: 'home.useCases.c5Title', descKey: 'home.useCases.c5Desc', qKey: 'home.useCases.c5Q' },
  { tag: '06', titleKey: 'home.useCases.c6Title', descKey: 'home.useCases.c6Desc', qKey: 'home.useCases.c6Q' },
  { tag: '07', titleKey: 'home.useCases.c7Title', descKey: 'home.useCases.c7Desc', qKey: 'home.useCases.c7Q' },
  { tag: '08', titleKey: 'home.useCases.c8Title', descKey: 'home.useCases.c8Desc', qKey: 'home.useCases.c8Q' }
]

const loadUseCaseQuestion = (uc) => {
  const qStr = t(uc.qKey)
  formData.value.simulationRequirement = qStr
  scrollToSection('simulation')
  nextTick(() => {
    const textarea = document.getElementById('studio-requirement-input')
    if (textarea) {
      textarea.focus()
    }
  })
}

// Studio form data (files are optional!)
const formData = ref({
  simulationRequirement: ''
})
const files = ref([])
const loading = ref(false)
const isDragOver = ref(false)
const fileInput = ref(null)

// Works with or without files!
const canSubmit = computed(() => {
  return formData.value.simulationRequirement.trim() !== ''
})

const triggerFileInput = () => {
  if (!loading.value) {
    fileInput.value?.click()
  }
}

const handleFileSelect = (event) => {
  const selectedFiles = Array.from(event.target.files)
  addFiles(selectedFiles)
}

const handleDrop = (e) => {
  isDragOver.value = false
  if (loading.value) return
  const droppedFiles = Array.from(e.dataTransfer.files)
  addFiles(droppedFiles)
}

const addFiles = (newFiles) => {
  const validFiles = newFiles.filter(file => {
    const ext = file.name.split('.').pop().toLowerCase()
    return ['pdf', 'md', 'txt'].includes(ext)
  })
  files.value.push(...validFiles)
}

const removeFile = (index) => {
  files.value.splice(index, 1)
}

const startSimulation = () => {
  if (!canSubmit.value || loading.value) return

  setPendingUpload(files.value, formData.value.simulationRequirement)

  router.push({
    name: 'Process',
    params: { projectId: 'new' }
  })
}

// Questions list
const questionsList = [
  { category: 'PRODUCT INNOVATION', q: 'home.questions.q1', a: 'home.questions.a1' },
  { category: 'PRICING DYNAMICS', q: 'home.questions.q2', a: 'home.questions.a2' },
  { category: 'COMPETITOR RESPONSE', q: 'home.questions.q3', a: 'home.questions.a3' },
  { category: 'AUDIENCE SEGMENTATION', q: 'home.questions.q4', a: 'home.questions.a4' },
  { category: 'MARKET CONDITIONS', q: 'home.questions.q5', a: 'home.questions.a5' },
  { category: 'STRATEGIC RESILIENCE', q: 'home.questions.q6', a: 'home.questions.a6' }
]

const loadQuestionIntoStudio = (item) => {
  const questionText = t(item.q)
  formData.value.simulationRequirement = questionText
  scrollToSection('simulation')
  nextTick(() => {
    const textarea = document.getElementById('studio-requirement-input')
    if (textarea) {
      textarea.focus()
    }
  })
}

// Contact Modal
const showConsultModal = ref(false)
const isSubmittingConsult = ref(false)
const consultSubmitted = ref(false)
const consultForm = ref({
  name: '',
  email: '',
  company: '',
  objective: ''
})

const openConsultModal = () => {
  showConsultModal.value = true
  consultSubmitted.value = false
}

const closeConsultModal = () => {
  showConsultModal.value = false
}

const submitConsultRequest = () => {
  isSubmittingConsult.value = true
  setTimeout(() => {
    isSubmittingConsult.value = false
    consultSubmitted.value = true
  }, 700)
}
</script>

<style scoped>
/* ==========================================================================
   PURE WHITE THEME STYLING (Aaru-inspired minimalist design system)
   ========================================================================== */

.light-enterprise-home {
  min-height: 100vh;
  background-color: #FFFFFF;
  color: #000000;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  display: flex;
  flex-direction: column;
}

/* Header (Clean, White, Fixed, Monospace / Modern Minimalist) */
.app-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 56px;
  background-color: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid #EAEAEA;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  z-index: 1000;
}

.header-left {
  display: flex;
  align-items: center;
}

.brand {
  font-family: 'JetBrains Mono', monospace;
  font-size: 15px;
  font-weight: 800;
  letter-spacing: 0.06em;
  color: #000000;
  text-decoration: none;
  cursor: pointer;
}

.header-center {
  display: flex;
  align-items: center;
  gap: 28px;
}

.nav-item {
  font-size: 13px;
  font-weight: 500;
  color: #555555;
  text-decoration: none;
  transition: color 0.15s ease;
}

.nav-item:hover {
  color: #000000;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.step-divider {
  width: 1px;
  height: 18px;
  background-color: #EAEAEA;
}

.github-link {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  font-weight: 600;
  color: #444444;
  text-decoration: none;
  padding: 6px 10px;
  border-radius: 4px;
  transition: all 0.15s ease;
}

.github-link:hover {
  color: #000000;
  background-color: #F5F5F5;
}

.header-btn {
  font-size: 12px;
  font-weight: 600;
  padding: 7px 14px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.15s ease;
  border: 1px solid transparent;
}

.header-btn.secondary {
  background-color: #FFFFFF;
  border-color: #EAEAEA;
  color: #000000;
}

.header-btn.secondary:hover {
  background-color: #F8F9FA;
  border-color: #CCCCCC;
}

.header-btn.primary {
  background-color: #000000;
  color: #FFFFFF;
}

.header-btn.primary:hover {
  background-color: #222222;
}

/* Mobile Nav Button */
.mobile-menu-btn {
  display: none;
  flex-direction: column;
  justify-content: space-around;
  width: 28px;
  height: 24px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 2px;
}

.mobile-menu-btn span {
  width: 100%;
  height: 2px;
  background-color: #000000;
  transition: all 0.2s ease;
}

.mobile-dropdown {
  position: absolute;
  top: 56px;
  left: 0;
  right: 0;
  background-color: #FFFFFF;
  border-bottom: 1px solid #EAEAEA;
  padding: 16px 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
}

.mobile-item {
  font-size: 14px;
  font-weight: 500;
  color: #333333;
  text-decoration: none;
  padding: 8px 0;
  border-bottom: 1px solid #F5F5F5;
}

.mobile-actions {
  display: flex;
  gap: 12px;
  margin-top: 8px;
}

.mobile-btn {
  flex: 1;
  padding: 10px;
  font-size: 13px;
  font-weight: 600;
  border-radius: 4px;
  border: 1px solid #EAEAEA;
  background-color: #FFFFFF;
  cursor: pointer;
}

.mobile-btn.dark {
  background-color: #000000;
  color: #FFFFFF;
  border-color: #000000;
}

/* Main Container */
.page-container {
  margin-top: 56px;
  flex: 1;
}

/* Hero Section */
.hero-section {
  padding: 96px 24px 72px;
  display: flex;
  justify-content: center;
  background-color: #FFFFFF;
}

.hero-inner {
  max-width: 1040px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.eyebrow-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #000000;
  background-color: #F4F4F5;
  border: 1px solid #E4E4E7;
  padding: 5px 12px;
  border-radius: 999px;
  margin-bottom: 24px;
}

.hero-headline {
  font-family: 'Space Grotesk', -apple-system, sans-serif;
  font-size: 56px;
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.03em;
  color: #000000;
  margin: 0 0 24px;
  max-width: 860px;
}

.hero-supporting {
  font-size: 18px;
  line-height: 1.6;
  color: #555555;
  max-width: 760px;
  margin: 0 0 36px;
}

.hero-cta-row {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 48px;
  flex-wrap: wrap;
  justify-content: center;
}

.btn-black {
  background-color: #000000;
  color: #FFFFFF;
  font-size: 14px;
  font-weight: 600;
  padding: 12px 24px;
  border-radius: 4px;
  border: 1px solid #000000;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-black:hover {
  background-color: #222222;
}

.btn-white {
  background-color: #FFFFFF;
  color: #000000;
  font-size: 14px;
  font-weight: 600;
  padding: 12px 24px;
  border-radius: 4px;
  border: 1px solid #EAEAEA;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-white:hover {
  background-color: #F8F9FA;
  border-color: #CCCCCC;
}

.hero-github-link {
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  font-weight: 600;
  color: #555555;
  text-decoration: none;
  padding: 12px 18px;
  border-radius: 4px;
  transition: all 0.15s ease;
}

.hero-github-link:hover {
  color: #000000;
}

/* Hero Inquiry Preview Card (Clean, intellectual decision preview) */
.hero-inquiry-card {
  width: 100%;
  max-width: 880px;
  background-color: #FFFFFF;
  border: 1px solid #EAEAEA;
  border-radius: 8px;
  padding: 24px 28px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.03);
  text-align: left;
}

.inquiry-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 14px;
  border-bottom: 1px solid #F0F0F0;
  margin-bottom: 16px;
}

.inquiry-status {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-dot {
  width: 7px;
  height: 7px;
  background-color: #10B981;
  border-radius: 50%;
}

.inquiry-badge {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  font-weight: 700;
  color: #666666;
  background-color: #F4F4F5;
  padding: 2px 8px;
  border-radius: 3px;
  text-transform: uppercase;
}

.inquiry-prompt-row {
  display: flex;
  gap: 12px;
  align-items: baseline;
  margin-bottom: 16px;
}

.inquiry-prompt-prefix {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 700;
  color: #000000;
  background-color: #EFEFEF;
  padding: 2px 6px;
  border-radius: 3px;
  flex-shrink: 0;
}

.inquiry-prompt-text {
  font-size: 15px;
  font-weight: 600;
  color: #111111;
  line-height: 1.5;
}

.inquiry-response-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin-bottom: 16px;
}

.response-chip {
  background-color: #FAFAFA;
  border: 1px solid #EAEAEA;
  border-radius: 6px;
  padding: 12px 16px;
}

.response-chip.highlight {
  border-color: #E0E0E0;
  background-color: #F8F9FA;
}

.chip-top {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 6px;
}

.chip-dot {
  width: 6px;
  height: 6px;
  background-color: #10B981;
  border-radius: 50%;
}

.chip-dot.orange {
  background-color: #F59E0B;
}

.chip-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  font-weight: 700;
  color: #666666;
  letter-spacing: 0.05em;
}

.chip-val {
  font-size: 13px;
  color: #333333;
  line-height: 1.4;
  display: block;
}

.inquiry-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 14px;
  border-top: 1px solid #F0F0F0;
}

.inquiry-footnote {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: #777777;
}

.inquiry-action-link {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  font-weight: 700;
  color: #000000;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  text-decoration: underline;
  transition: opacity 0.15s ease;
}

.inquiry-action-link:hover {
  opacity: 0.7;
}

/* Content Sections General */
.content-section {
  padding: 80px 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.border-top {
  border-top: 1px solid #EAEAEA;
}

.bg-subtle {
  background-color: #FAFAFA;
}

.section-head-center {
  max-width: 800px;
  text-align: center;
  margin-bottom: 48px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.section-pill {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #666666;
  background-color: #F0F0F0;
  padding: 4px 10px;
  border-radius: 4px;
  margin-bottom: 16px;
}

.section-title {
  font-family: 'Space Grotesk', -apple-system, sans-serif;
  font-size: 36px;
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.02em;
  color: #000000;
  margin: 0 0 16px;
}

.section-subtitle {
  font-size: 16px;
  color: #666666;
  line-height: 1.6;
  margin: 0;
}

.section-grid-2col {
  max-width: 1040px;
  width: 100%;
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 48px;
}

.section-col-left {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.section-col-right {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.body-lead {
  font-size: 18px;
  line-height: 1.7;
  color: #333333;
  margin: 0;
}

/* Limitations Grid in Problem Section */
.limitations-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-top: 8px;
}

.limitation-item {
  background-color: #FAFAFA;
  border: 1px solid #EAEAEA;
  border-radius: 6px;
  padding: 18px;
  display: flex;
  flex-direction: column;
}

.limit-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 700;
  color: #888888;
  margin-bottom: 8px;
}

.limit-title {
  font-size: 14px;
  font-weight: 700;
  color: #000000;
  margin: 0 0 6px;
}

.limit-desc {
  font-size: 12px;
  line-height: 1.5;
  color: #666666;
  margin: 0;
}

/* Core Flow Pipeline Container */
.core-flow-container {
  background-color: #FFFFFF;
  border: 1px solid #EAEAEA;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.02);
}

.core-flow-header {
  padding-bottom: 12px;
  border-bottom: 1px solid #F0F0F0;
  margin-bottom: 14px;
}

.core-flow-steps {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.core-step {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background-color: #F8F9FA;
  border: 1px solid #EAEAEA;
  border-radius: 4px;
  padding: 6px 10px;
}

.core-step.highlight {
  background-color: #000000;
  border-color: #000000;
}

.core-step-badge {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  font-weight: 700;
  color: #888888;
}

.core-step.highlight .core-step-badge {
  color: #AAAAAA;
}

.core-step-text {
  font-size: 12px;
  font-weight: 600;
  color: #111111;
}

.core-step.highlight .core-step-text {
  color: #FFFFFF;
}

.core-arrow {
  color: #CCCCCC;
  font-size: 13px;
}

/* How It Works Grid */
.how-it-works-grid {
  max-width: 1040px;
  width: 100%;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.step-card {
  background-color: #FFFFFF;
  border: 1px solid #EAEAEA;
  border-radius: 8px;
  padding: 28px 20px;
  display: flex;
  flex-direction: column;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.step-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.04);
}

.step-card-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 20px;
  font-weight: 800;
  color: #000000;
  margin-bottom: 16px;
}

.step-card-title {
  font-size: 16px;
  font-weight: 700;
  color: #000000;
  margin: 0 0 10px;
}

.step-card-desc {
  font-size: 13px;
  line-height: 1.6;
  color: #666666;
  margin: 0;
}

/* Use Cases Grid (8 cards) */
.use-cases-grid {
  max-width: 1040px;
  width: 100%;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.use-case-card {
  background-color: #FFFFFF;
  border: 1px solid #EAEAEA;
  border-radius: 8px;
  padding: 22px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.use-case-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.04);
}

.uc-header {
  display: flex;
  align-items: baseline;
  gap: 8px;
  margin-bottom: 10px;
}

.uc-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 700;
  color: #888888;
}

.uc-title {
  font-size: 15px;
  font-weight: 700;
  color: #000000;
  margin: 0;
}

.uc-desc {
  font-size: 13px;
  line-height: 1.5;
  color: #666666;
  margin: 0 0 16px;
}

.uc-inquiry-box {
  background-color: #FAFAFA;
  border: 1px dashed #E0E0E0;
  border-radius: 6px;
  padding: 10px 12px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.uc-inquiry-box:hover {
  background-color: #F4F4F5;
  border-color: #000000;
}

.uc-inquiry-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px;
  font-weight: 700;
  color: #888888;
  letter-spacing: 0.06em;
  display: block;
  margin-bottom: 4px;
}

.uc-inquiry-text {
  font-size: 12px;
  font-weight: 600;
  color: #222222;
  margin: 0 0 4px;
  line-height: 1.35;
}

.uc-inquiry-cta {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  font-weight: 700;
  color: #000000;
}

/* Questions Grid */
.questions-grid {
  max-width: 1040px;
  width: 100%;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.question-pill-card {
  background-color: #FFFFFF;
  border: 1px solid #EAEAEA;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  align-items: flex-start;
  gap: 14px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.question-pill-card:hover {
  border-color: #000000;
  background-color: #FAFAFA;
}

.q-icon {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  font-weight: 700;
  background-color: #F0F0F0;
  color: #000000;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  flex-shrink: 0;
}

.q-content {
  flex: 1;
}

.q-category {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #888888;
  margin-bottom: 4px;
}

.q-title {
  font-size: 15px;
  font-weight: 700;
  color: #000000;
  margin: 0 0 6px;
  line-height: 1.4;
}

.q-desc {
  font-size: 13px;
  color: #666666;
  line-height: 1.5;
  margin: 0;
}

.q-arrow {
  color: #AAAAAA;
  font-size: 16px;
  transition: transform 0.15s ease;
}

.question-pill-card:hover .q-arrow {
  color: #000000;
  transform: translate(2px, -2px);
}

/* Differentiation Section */
.differentiation-grid {
  max-width: 1040px;
  width: 100%;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 32px;
}

.diff-card {
  background-color: #FFFFFF;
  border: 1px solid #EAEAEA;
  border-radius: 8px;
  padding: 28px 24px;
  display: flex;
  flex-direction: column;
}

.diff-card.active-diff {
  border-color: #000000;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.05);
}

.diff-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.diff-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  font-weight: 700;
  color: #999999;
}

.diff-type {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  padding: 3px 8px;
  border-radius: 4px;
}

.diff-type.muted {
  background-color: #F4F4F5;
  color: #666666;
}

.diff-type.highlight {
  background-color: #000000;
  color: #FFFFFF;
}

.diff-title {
  font-size: 18px;
  font-weight: 700;
  color: #000000;
  margin: 0 0 12px;
}

.diff-desc {
  font-size: 14px;
  line-height: 1.6;
  color: #666666;
  margin: 0;
}

.disclaimer-banner {
  max-width: 1040px;
  width: 100%;
  background-color: #FFFFFF;
  border: 1px solid #EAEAEA;
  border-radius: 6px;
  padding: 14px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.disclaimer-badge {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  font-weight: 700;
  color: #000000;
  background-color: #EAEAEA;
  padding: 3px 6px;
  border-radius: 3px;
}

.disclaimer-text {
  font-size: 13px;
  color: #555555;
  margin: 0;
  line-height: 1.5;
}

/* Simulation Section Pipeline Card (7 Steps) */
.simulation-pipeline-card {
  max-width: 1040px;
  width: 100%;
  background-color: #FFFFFF;
  border: 1px solid #EAEAEA;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
  margin-bottom: 24px;
}

.pipeline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 16px;
  border-bottom: 1px solid #F0F0F0;
  margin-bottom: 20px;
}

.mono-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #666666;
  text-transform: uppercase;
}

.pipeline-status {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 600;
  color: #10B981;
}

.pipeline-steps {
  display: flex;
  align-items: center;
  justify-content: space-between;
  overflow-x: auto;
  padding-bottom: 12px;
  gap: 4px;
}

.pipeline-step-wrap {
  display: flex;
  align-items: center;
  gap: 6px;
}

.pipeline-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12px 14px;
  background-color: #F8F9FA;
  border: 1px solid #EAEAEA;
  border-radius: 6px;
  min-width: 106px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.pipeline-step:hover,
.pipeline-step.active-step {
  border-color: #000000;
  background-color: #FFFFFF;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.step-badge {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  font-weight: 700;
  color: #888888;
  margin-bottom: 4px;
}

.step-name {
  font-size: 12px;
  font-weight: 600;
  color: #111111;
  white-space: nowrap;
}

.pipeline-arrow {
  color: #CCCCCC;
  font-weight: 600;
  font-size: 14px;
}

.decision-step {
  background-color: #000000;
  border-color: #000000;
}

.decision-badge {
  color: #999999;
}

.decision-name {
  color: #FFFFFF;
}

.decision-step:hover,
.decision-step.active-step {
  background-color: #1A1A1A;
  border-color: #000000;
}

.pipeline-detail-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  padding-top: 14px;
  border-top: 1px solid #F0F0F0;
  font-size: 13px;
  line-height: 1.5;
}

.detail-badge {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  font-weight: 700;
  background-color: #000000;
  color: #FFFFFF;
  padding: 2px 6px;
  border-radius: 3px;
}

.detail-label {
  font-weight: 700;
  color: #000000;
}

.detail-text {
  color: #555555;
}

/* Simulation Studio Section */
.studio-container {
  max-width: 1040px;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.studio-card {
  background-color: #FFFFFF;
  border: 1px solid #EAEAEA;
  border-radius: 8px;
  padding: 32px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
}

.studio-field {
  margin-bottom: 24px;
}

.field-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.field-label {
  font-size: 14px;
  font-weight: 700;
  color: #000000;
}

.field-badge {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  padding: 2px 6px;
  border-radius: 3px;
}

.field-badge.required {
  background-color: #FEE2E2;
  color: #DC2626;
}

.field-badge.optional {
  background-color: #F3F4F6;
  color: #6B7280;
}

.field-subtext {
  font-size: 12px;
  color: #666666;
  margin: 0 0 10px;
}

.studio-textarea {
  width: 100%;
  border: 1px solid #EAEAEA;
  border-radius: 6px;
  padding: 14px;
  font-size: 14px;
  font-family: inherit;
  color: #000000;
  background-color: #FFFFFF;
  resize: vertical;
  outline: none;
  transition: border-color 0.15s ease;
  box-sizing: border-box;
}

.studio-textarea:focus {
  border-color: #000000;
}

.dropzone {
  border: 1px dashed #CCCCCC;
  border-radius: 6px;
  padding: 24px;
  text-align: center;
  cursor: pointer;
  background-color: #FAFAFA;
  transition: all 0.15s ease;
}

.dropzone:hover, .dropzone.drag-over {
  border-color: #000000;
  background-color: #F5F5F5;
}

.hidden-file-input {
  display: none;
}

.upload-icon {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 6px;
}

.drop-text {
  font-size: 13px;
  font-weight: 600;
  color: #111111;
  margin-bottom: 4px;
}

.drop-types {
  font-size: 11px;
  color: #777777;
}

.file-list {
  margin-top: 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.file-list-title {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 700;
  color: #555555;
}

.file-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #F8F9FA;
  border: 1px solid #EAEAEA;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 12px;
}

.file-remove {
  background: transparent;
  border: none;
  cursor: pointer;
  color: #888888;
  font-size: 12px;
}

.file-remove:hover {
  color: #000000;
}

.studio-actions {
  display: flex;
  justify-content: flex-end;
}

.studio-launch-btn {
  background-color: #000000;
  color: #FFFFFF;
  border: 1px solid #000000;
  font-size: 14px;
  font-weight: 600;
  padding: 12px 28px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.studio-launch-btn:hover:not(:disabled) {
  background-color: #222222;
}

.studio-launch-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.studio-history-card {
  background-color: #FFFFFF;
  border: 1px solid #EAEAEA;
  border-radius: 8px;
  padding: 24px;
}

.history-card-header {
  padding-bottom: 12px;
  border-bottom: 1px solid #F0F0F0;
  margin-bottom: 16px;
}

/* Research Pillars */
.research-pillars {
  display: flex;
  flex-direction: column;
  gap: 18px;
  margin-top: 12px;
}

.pillar-item {
  border-left: 2px solid #000000;
  padding-left: 16px;
}

.pillar-title {
  font-size: 15px;
  font-weight: 700;
  color: #000000;
  margin: 0 0 6px;
}

.pillar-desc {
  font-size: 13px;
  line-height: 1.6;
  color: #666666;
  margin: 0;
}

/* Final CTA Banner */
.cta-banner {
  max-width: 860px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 20px;
}

.cta-title {
  font-family: 'Space Grotesk', -apple-system, sans-serif;
  font-size: 40px;
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.02em;
  color: #000000;
  margin: 0 0 16px;
}

.cta-subtitle {
  font-size: 18px;
  color: #666666;
  margin: 0 0 32px;
  max-width: 600px;
}

.cta-buttons {
  display: flex;
  gap: 14px;
}

/* Footer */
.app-footer {
  border-top: 1px solid #EAEAEA;
  background-color: #FFFFFF;
  padding: 64px 24px 32px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.footer-grid {
  max-width: 1040px;
  width: 100%;
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 40px;
  margin-bottom: 48px;
}

.footer-brand {
  font-family: 'JetBrains Mono', monospace;
  font-size: 16px;
  font-weight: 800;
  letter-spacing: 0.05em;
  color: #000000;
  margin-bottom: 12px;
}

.footer-tagline {
  font-size: 14px;
  font-weight: 600;
  color: #333333;
  margin: 0 0 8px;
}

.footer-desc {
  font-size: 13px;
  line-height: 1.6;
  color: #777777;
  max-width: 320px;
  margin: 0;
}

.footer-col-title {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #000000;
  margin-bottom: 16px;
}

.footer-col {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.footer-col a {
  font-size: 13px;
  color: #666666;
  text-decoration: none;
  transition: color 0.15s ease;
}

.footer-col a:hover {
  color: #000000;
}

.footer-bottom {
  max-width: 1040px;
  width: 100%;
  border-top: 1px solid #F0F0F0;
  padding-top: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: #888888;
}

.footer-links {
  display: flex;
  gap: 8px;
}

/* Consultation / Contact Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
}

.modal-dialog {
  background-color: #FFFFFF;
  border: 1px solid #EAEAEA;
  border-radius: 8px;
  max-width: 480px;
  width: 100%;
  padding: 32px;
  position: relative;
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.1);
}

.modal-close {
  position: absolute;
  top: 16px;
  right: 16px;
  background: transparent;
  border: none;
  font-size: 20px;
  color: #888888;
  cursor: pointer;
}

.modal-close:hover {
  color: #000000;
}

.modal-head {
  margin-bottom: 20px;
}

.modal-title {
  font-size: 20px;
  font-weight: 700;
  color: #000000;
  margin: 0 0 6px;
}

.modal-sub {
  font-size: 13px;
  color: #666666;
  margin: 0;
  line-height: 1.5;
}

.modal-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-field label {
  font-size: 12px;
  font-weight: 700;
  color: #222222;
}

.form-field input, .form-field textarea {
  border: 1px solid #EAEAEA;
  border-radius: 4px;
  padding: 10px 12px;
  font-size: 13px;
  outline: none;
  box-sizing: border-box;
}

.form-field input:focus, .form-field textarea:focus {
  border-color: #000000;
}

.modal-submit-btn {
  background-color: #000000;
  color: #FFFFFF;
  border: 1px solid #000000;
  padding: 12px;
  font-size: 13px;
  font-weight: 600;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 6px;
}

.modal-submit-btn:disabled {
  opacity: 0.5;
}

.modal-success {
  text-align: center;
  padding: 20px 0;
}

.success-icon {
  font-size: 32px;
  color: #10B981;
  margin-bottom: 12px;
}

.modal-success h3 {
  font-size: 18px;
  margin: 0 0 8px;
}

.modal-success p {
  font-size: 13px;
  color: #666666;
  margin: 0 0 20px;
}

/* Responsive Media Queries (Testing 1440px / 1280px / 1024px / 768px / 430px / 390px / 375px) */
@media (max-width: 1024px) {
  .use-cases-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .how-it-works-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .differentiation-grid {
    grid-template-columns: 1fr;
  }

  .footer-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 768px) {
  .header-center {
    display: none;
  }

  .mobile-menu-btn {
    display: flex;
  }

  .hero-headline {
    font-size: 38px;
  }

  .section-grid-2col {
    grid-template-columns: 1fr;
    gap: 24px;
  }

  .limitations-grid {
    grid-template-columns: 1fr;
  }

  .inquiry-response-grid {
    grid-template-columns: 1fr;
  }

  .questions-grid {
    grid-template-columns: 1fr;
  }

  .use-cases-grid {
    grid-template-columns: 1fr;
  }

  .how-it-works-grid {
    grid-template-columns: 1fr;
  }

  .footer-grid {
    grid-template-columns: 1fr;
  }

  .footer-bottom {
    flex-direction: column;
    gap: 12px;
    text-align: center;
  }

  .pipeline-steps {
    flex-wrap: wrap;
    justify-content: center;
  }

  .pipeline-step-wrap {
    margin-bottom: 6px;
  }
}

@media (max-width: 430px) {
  .hero-section {
    padding: 72px 16px 48px;
  }

  .hero-headline {
    font-size: 32px;
  }

  .hero-supporting {
    font-size: 16px;
  }

  .content-section {
    padding: 60px 16px;
  }

  .section-title {
    font-size: 28px;
  }

  .cta-title {
    font-size: 30px;
  }

  .studio-card {
    padding: 20px 16px;
  }

  .hero-inquiry-card {
    padding: 18px 16px;
  }
}
</style>
