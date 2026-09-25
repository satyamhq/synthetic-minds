<template>
  <div class="not-found-container">
    <div class="not-found-content">
      <div class="error-badge">404 ERROR</div>
      <h1 class="error-title">{{ t('notFound.title') }}</h1>
      <p class="error-description">
        {{ t('notFound.description') }}
      </p>
      <div class="action-buttons">
        <router-link to="/" class="btn-primary">
          {{ t('notFound.returnHome') }}
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<style scoped>
.not-found-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #0f1117;
  color: #f3f4f6;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  padding: 24px;
}

.not-found-content {
  text-align: center;
  max-width: 480px;
}

.error-badge {
  display: inline-block;
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: #ff6b35;
  background: rgba(255, 107, 53, 0.12);
  border: 1px solid rgba(255, 107, 53, 0.3);
  border-radius: 9999px;
  padding: 6px 14px;
  margin-bottom: 24px;
}

.error-title {
  font-size: 32px;
  font-weight: 700;
  letter-spacing: -0.02em;
  margin: 0 0 16px 0;
  color: #ffffff;
}

.error-description {
  font-size: 15px;
  color: #9ca3af;
  line-height: 1.6;
  margin: 0 0 32px 0;
}

.action-buttons {
  display: flex;
  justify-content: center;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 12px 24px;
  background: #ffffff;
  color: #0f1117;
  font-weight: 600;
  font-size: 14px;
  border-radius: 8px;
  text-decoration: none;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background: #e5e7eb;
  transform: translateY(-1px);
}
</style>
