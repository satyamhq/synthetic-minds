# Third-Party Notices and Attribution

Synthetic Minds incorporates, builds upon, or interfaces with open-source software and services. This document contains notices, attributions, and licensing details for those third-party components.

---

## 1. Upstream Project Attribution

**Synthetic Minds** is a derived and rebranded software platform originally based upon the open-source **MiroFish** project.

- **Original Project:** MiroFish
- **Original Authors:** 666ghj & the MiroFish Team
- **Upstream Repository:** [https://github.com/666ghj/MiroFish](https://github.com/666ghj/MiroFish)
- **Original License:** GNU Affero General Public License v3.0 (AGPL-3.0)

We gratefully acknowledge the pioneering architecture, research, and engineering contributed by 666ghj and the original MiroFish contributors. All modifications, refactoring, rebranding, and localization to English/Hindi in this repository are maintained by [satyamhq](https://github.com/satyamhq/synthetic-minds).

---

## 2. Key Frameworks and Engine Dependencies

### OpenAI Python SDK
- **Project:** OpenAI Python Client (`openai`)
- **Authors:** OpenAI
- **Repository:** [https://github.com/openai/openai-python](https://github.com/openai/openai-python)
- **License:** Apache License 2.0
- **Notice:** Used as the exclusive LLM provider integration for autonomous agent reasoning, persona generation, and ReACT report synthesis.

### CAMEL-AI & OASIS (Open Agent Social Interaction Simulations)
- **Project:** OASIS (Social media multi-agent simulation engine)
- **Authors:** CAMEL-AI Team
- **Repository:** [https://github.com/camel-ai/oasis](https://github.com/camel-ai/oasis)
- **License:** Apache License 2.0
- **Notice:** Synthetic Minds uses the OASIS simulation framework for autonomous agent modeling in digital sandbox environments.

### Zep Cloud
- **Project:** Zep Cloud SDK (`zep-cloud`)
- **Authors:** Zep Inc.
- **Repository:** [https://github.com/getzep/zep-python](https://github.com/getzep/zep-python)
- **License:** Apache License 2.0
- **Notice:** Used for temporal memory graphs and GraphRAG persistence.

### Vue.js Ecosystem
- **Project:** Vue.js, Vue Router, Vue I18n
- **Authors:** Evan You and the Vue Community
- **Repository:** [https://github.com/vuejs/core](https://github.com/vuejs/core)
- **License:** MIT License

### D3.js
- **Project:** D3.js (Data-Driven Documents)
- **Authors:** Mike Bostock and D3 contributors
- **Repository:** [https://github.com/d3/d3](https://github.com/d3/d3)
- **License:** ISC License

### Flask Ecosystem
- **Project:** Flask, Flask-CORS, Werkzeug
- **Authors:** Pallets Community & Armin Ronacher
- **Repository:** [https://github.com/pallets/flask](https://github.com/pallets/flask)
- **License:** BSD-3-Clause License

### PyMuPDF
- **Project:** PyMuPDF (fitz)
- **Authors:** Artifex Software, Inc.
- **License:** GNU AGPL v3.0 / Commercial License

---

## 3. License Summaries

### MIT License
Used by Synthetic Minds, Vue.js, and various JavaScript libraries:
```
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

### Apache License 2.0
Used by CAMEL-AI, OASIS, and Zep Cloud:
```
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
