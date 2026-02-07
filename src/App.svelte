<script lang="ts">
  import { onMount } from "svelte";
  import { fly } from "svelte/transition";
  import Fuse from "fuse.js";
  import CategoryDropdown from "./CategoryDropdown.svelte";

  type Guardrail = {
    id: string;
    name: string;
    description: string;
    category: string;
    tags: string[];
    author: string;
    version: string;
    input_type: string;
    code: string;
  };

  type ResultItem = {
    refIndex: number;
    item: Guardrail;
  };

  const REPO_FULL_NAME = "BerriAI/litellm-guardrails";
  const DEFAULT_BRANCH = "main";
  const RESOURCE_PATH = "guardrails.json";

  let categories: string[] = [];
  let selectedCategory: string = "";
  let inputTypes: string[] = ["request", "response", "both"];
  let selectedInputType: string = "";

  onMount(() => {
    const urlParams = new URLSearchParams(window.location.search);
    query = urlParams.get("q") ?? "";

    fetch(
      `https://raw.githubusercontent.com/${REPO_FULL_NAME}/${DEFAULT_BRANCH}/${RESOURCE_PATH}`
    )
      .then((res) => res.json())
      .then((data) => {
        const items: Guardrail[] = Object.entries(data).map(
          ([id, v]: any) => ({ id, ...v })
        );

        categories = [...new Set(items.map((i) => i.category))].sort();

        index = new Fuse(items, {
          threshold: 0.3,
          keys: [
            { name: "name", weight: 2 },
            { name: "description", weight: 1.5 },
            { name: "tags", weight: 1 },
            "category",
          ],
        });

        results = items.map((item, refIndex) => ({ item, refIndex }));
        allItems = items;
        loading = false;
      })
      .catch(() => {
        // Fallback to local file for development
        fetch("/guardrails.json")
          .then((res) => res.json())
          .then((data) => {
            const items: Guardrail[] = Object.entries(data).map(
              ([id, v]: any) => ({ id, ...v })
            );
            categories = [...new Set(items.map((i) => i.category))].sort();
            index = new Fuse(items, {
              threshold: 0.3,
              keys: [
                { name: "name", weight: 2 },
                { name: "description", weight: 1.5 },
                { name: "tags", weight: 1 },
                "category",
              ],
            });
            results = items.map((item, refIndex) => ({ item, refIndex }));
            allItems = items;
            loading = false;
          });
      });
  });

  function getCategoryIcon(category: string): string {
    const icons: { [key: string]: string } = {
      security: "🔒",
      validation: "✅",
      moderation: "🛡️",
      "rate-limiting": "⏱️",
      content: "📝",
      formatting: "✨",
    };
    return icons[category] || "📦";
  }

  function getInputTypeLabel(type: string): string {
    const labels: { [key: string]: string } = {
      request: "Request",
      response: "Response",
      both: "Both",
    };
    return labels[type] || type;
  }

  function copyToClipboard(text: string) {
    navigator.clipboard.writeText(text);
    copiedId = text;
    setTimeout(() => (copiedId = ""), 2000);
  }

  function toggleRow(id: string) {
    if (expandedRows.has(id)) {
      expandedRows.delete(id);
    } else {
      expandedRows.add(id);
    }
    expandedRows = expandedRows;
  }

  function filterResults() {
    if (!index || !allItems) return;

    let filtered = allItems;

    // Filter by category
    if (selectedCategory) {
      filtered = filtered.filter((item) => item.category === selectedCategory);
    }

    // Filter by input type
    if (selectedInputType) {
      filtered = filtered.filter(
        (item) =>
          item.input_type === selectedInputType || item.input_type === "both"
      );
    }

    // Apply search query
    if (query) {
      const searchIndex = new Fuse(filtered, {
        threshold: 0.3,
        keys: [
          { name: "name", weight: 2 },
          { name: "description", weight: 1.5 },
          { name: "tags", weight: 1 },
          "category",
        ],
      });
      filtered = searchIndex.search(query).map((r) => r.item);
    }

    results = filtered.map((item, refIndex) => ({ item, refIndex }));
  }

  let query = "";
  let index: Fuse<Guardrail>;
  let allItems: Guardrail[] = [];
  let results: ResultItem[] = [];
  let loading = true;
  let expandedRows = new Set<string>();
  let copiedId = "";

  $: {
    if (index) {
      filterResults();
    }
  }

  $: query, selectedCategory, selectedInputType, filterResults();
</script>

<main class="container">
  <!-- Hero Section -->
  <div class="hero">
    <h1 class="hero-title">LiteLLM Guardrails Marketplace</h1>
    <p class="hero-subtitle">
      A community collection of custom code guardrails for LiteLLM. Copy, customize, and deploy to protect your LLM applications.
    </p>

    <div class="cta-buttons">
      <a
        href="https://github.com/{REPO_FULL_NAME}"
        target="_blank"
        rel="noopener noreferrer"
        class="btn btn-primary"
      >
        <svg
          width="16"
          height="16"
          viewBox="0 0 16 16"
          fill="currentColor"
          style="margin-right: 8px;"
        >
          <path
            d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"
          />
        </svg>
        Contribute a Guardrail
      </a>
      <a
        href="https://docs.litellm.ai/docs/proxy/guardrails/custom_code_guardrail"
        target="_blank"
        rel="noopener noreferrer"
        class="btn btn-secondary"
      >
        Read the Docs
      </a>
    </div>
  </div>

  <!-- Search and Filters -->
  <div class="search-section">
    <div class="search-bar-container">
      <div class="search-input-wrapper">
        <svg
          class="search-icon"
          width="20"
          height="20"
          viewBox="0 0 20 20"
          fill="none"
        >
          <circle
            cx="8.5"
            cy="8.5"
            r="5.75"
            stroke="currentColor"
            stroke-width="1.5"
          />
          <path
            d="M12.5 12.5L16.5 16.5"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linecap="round"
          />
        </svg>
        <input
          id="query"
          bind:value={query}
          type="text"
          autocomplete="off"
          name="query"
          aria-label="Search guardrails"
          placeholder="Search guardrails..."
          class="search-input"
        />
      </div>

      <CategoryDropdown bind:selectedCategory {categories} />
    </div>

    <div class="filters-row">
      <div class="filter-group">
        <label for="inputType">Input Type</label>
        <select
          id="inputType"
          bind:value={selectedInputType}
          class="filter-select"
        >
          <option value="">All Types</option>
          {#each inputTypes as type}
            <option value={type}>{getInputTypeLabel(type)}</option>
          {/each}
        </select>
      </div>
      <div class="results-count">
        <span>{results.length} guardrail{results.length !== 1 ? "s" : ""} found</span>
      </div>
    </div>
  </div>

  {#if loading}
    <div class="loading">
      <span aria-busy="true">Loading guardrails...</span>
    </div>
  {:else}
    <div class="cards-container">
      {#each results as { item } (item.id)}
        <div
          class="guardrail-card"
          class:expanded={expandedRows.has(item.id)}
          on:click={() => toggleRow(item.id)}
          on:keypress={(e) => e.key === "Enter" && toggleRow(item.id)}
          role="button"
          tabindex="0"
        >
          <div class="card-header">
            <div class="card-title-row">
              <span class="category-icon">{getCategoryIcon(item.category)}</span>
              <h3 class="card-title">{item.name}</h3>
              <span class="version-badge">v{item.version}</span>
            </div>
            <p class="card-description">{item.description}</p>
          </div>

          <div class="card-meta">
            <div class="tags">
              {#each item.tags.slice(0, 4) as tag}
                <span class="tag">{tag}</span>
              {/each}
              {#if item.tags.length > 4}
                <span class="tag tag-more">+{item.tags.length - 4}</span>
              {/if}
            </div>
            <div class="meta-right">
              <span class="input-type-badge" class:request={item.input_type === "request"} class:response={item.input_type === "response"} class:both={item.input_type === "both"}>
                {getInputTypeLabel(item.input_type)}
              </span>
            </div>
          </div>

          {#if expandedRows.has(item.id)}
            <div class="card-expanded" transition:fly={{ y: -10, duration: 200 }}>
              <div class="code-header">
                <span class="code-label">Code</span>
                <button
                  class="copy-btn"
                  on:click|stopPropagation={() => copyToClipboard(item.code)}
                >
                  {copiedId === item.code ? "✓ Copied!" : "Copy Code"}
                </button>
              </div>
              <pre class="code-block"><code>{item.code}</code></pre>
              
              <div class="usage-section">
                <span class="usage-label">Usage in config.yaml:</span>
                <pre class="usage-code"><code>litellm_settings:
  guardrails:
    - guardrail_name: "{item.id}"
      litellm_params:
        guardrail: custom_code.{item.id}
        mode: "{item.input_type === 'both' ? 'pre_call' : item.input_type === 'request' ? 'pre_call' : 'post_call'}"</code></pre>
              </div>

              <div class="card-footer">
                <span class="author">By {item.author}</span>
                <a
                  href="https://github.com/{REPO_FULL_NAME}/blob/main/guardrails/{item.id}.py"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="github-link"
                  on:click|stopPropagation
                >
                  View on GitHub →
                </a>
              </div>
            </div>
          {/if}
        </div>
      {/each}
    </div>

    {#if results.length === 0}
      <div class="no-results">
        <p>No guardrails found matching your search.</p>
        <a
          href="https://github.com/{REPO_FULL_NAME}/issues/new?template=guardrail_request.md"
          target="_blank"
          rel="noopener noreferrer"
        >
          Request a new guardrail →
        </a>
      </div>
    {/if}
  {/if}
</main>

<style>
  :root {
    --litellm-primary: #6366f1;
    --litellm-dark: #0f0f23;
    --litellm-purple: #8b5cf6;
  }

  .container {
    min-height: 100vh;
    background-color: var(--bg-color);
    color: var(--text-color);
  }

  /* Hero Section */
  .hero {
    text-align: center;
    padding: 4rem 2rem 3rem;
    max-width: 900px;
    margin: 0 auto;
  }

  .hero-title {
    font-size: 3rem;
    font-weight: 700;
    line-height: 1.1;
    margin: 0 0 1rem 0;
    color: var(--text-color);
    letter-spacing: -0.02em;
  }

  .hero-subtitle {
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--muted-color);
    margin: 0 0 2rem 0;
    max-width: 650px;
    margin-left: auto;
    margin-right: auto;
  }

  .cta-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
  }

  .btn {
    display: inline-flex;
    align-items: center;
    padding: 0.75rem 1.5rem;
    font-size: 0.9375rem;
    font-weight: 500;
    border-radius: 8px;
    text-decoration: none;
    transition: all 0.2s ease;
    border: 1px solid transparent;
  }

  .btn-primary {
    background-color: var(--litellm-primary);
    color: white;
  }

  .btn-primary:hover {
    background-color: #5558e3;
    transform: translateY(-1px);
  }

  .btn-secondary {
    background-color: transparent;
    color: var(--text-color);
    border-color: var(--border-color);
  }

  .btn-secondary:hover {
    border-color: var(--litellm-primary);
    color: var(--litellm-primary);
  }

  /* Search Section */
  .search-section {
    max-width: 1200px;
    margin: 2rem auto;
    padding: 0 2rem;
  }

  .search-bar-container {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
  }

  .search-input-wrapper {
    position: relative;
    flex: 1;
  }

  .search-icon {
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    color: var(--muted-color);
  }

  .search-input {
    width: 100%;
    padding: 0.875rem 1rem 0.875rem 3rem;
    font-size: 1rem;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    background-color: var(--bg-color);
    color: var(--text-color);
    transition: border-color 0.2s;
  }

  .search-input:focus {
    outline: none;
    border-color: var(--litellm-primary);
  }

  .filters-row {
    display: flex;
    gap: 1rem;
    align-items: center;
    justify-content: space-between;
  }

  .filter-group {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .filter-group label {
    font-size: 0.875rem;
    color: var(--muted-color);
  }

  .filter-select {
    padding: 0.5rem 1rem;
    border: 1px solid var(--border-color);
    border-radius: 6px;
    background-color: var(--bg-color);
    color: var(--text-color);
    font-size: 0.875rem;
  }

  .results-count {
    font-size: 0.875rem;
    color: var(--muted-color);
  }

  /* Cards */
  .cards-container {
    max-width: 1200px;
    margin: 2rem auto;
    padding: 0 2rem;
    display: grid;
    gap: 1rem;
  }

  .guardrail-card {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 1.25rem;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .guardrail-card:hover {
    border-color: var(--litellm-primary);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.1);
  }

  .guardrail-card.expanded {
    border-color: var(--litellm-primary);
  }

  .card-header {
    margin-bottom: 1rem;
  }

  .card-title-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
  }

  .category-icon {
    font-size: 1.25rem;
  }

  .card-title {
    font-size: 1.125rem;
    font-weight: 600;
    margin: 0;
    color: var(--text-color);
  }

  .version-badge {
    font-size: 0.75rem;
    padding: 0.125rem 0.5rem;
    background: var(--bg-tertiary);
    border-radius: 4px;
    color: var(--muted-color);
  }

  .card-description {
    font-size: 0.9375rem;
    color: var(--muted-color);
    margin: 0;
    line-height: 1.5;
  }

  .card-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .tags {
    display: flex;
    gap: 0.375rem;
    flex-wrap: wrap;
  }

  .tag {
    font-size: 0.75rem;
    padding: 0.25rem 0.5rem;
    background: var(--bg-tertiary);
    border-radius: 4px;
    color: var(--muted-color);
  }

  .tag-more {
    background: var(--litellm-primary);
    color: white;
  }

  .input-type-badge {
    font-size: 0.75rem;
    padding: 0.25rem 0.625rem;
    border-radius: 4px;
    font-weight: 500;
  }

  .input-type-badge.request {
    background: #dbeafe;
    color: #1e40af;
  }

  .input-type-badge.response {
    background: #dcfce7;
    color: #166534;
  }

  .input-type-badge.both {
    background: #f3e8ff;
    color: #7c3aed;
  }

  /* Expanded Card */
  .card-expanded {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border-color);
  }

  .code-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
  }

  .code-label,
  .usage-label {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--muted-color);
  }

  .copy-btn {
    font-size: 0.8125rem;
    padding: 0.375rem 0.75rem;
    background: var(--litellm-primary);
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.2s;
  }

  .copy-btn:hover {
    background: #5558e3;
  }

  .code-block,
  .usage-code {
    background: var(--code-bg);
    border-radius: 8px;
    padding: 1rem;
    overflow-x: auto;
    font-family: "Menlo", "Monaco", monospace;
    font-size: 0.8125rem;
    line-height: 1.6;
    margin: 0;
  }

  .code-block code,
  .usage-code code {
    color: var(--code-text);
  }

  .usage-section {
    margin-top: 1rem;
  }

  .usage-label {
    display: block;
    margin-bottom: 0.5rem;
  }

  .card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border-color);
  }

  .author {
    font-size: 0.8125rem;
    color: var(--muted-color);
  }

  .github-link {
    font-size: 0.8125rem;
    color: var(--litellm-primary);
    text-decoration: none;
  }

  .github-link:hover {
    text-decoration: underline;
  }

  /* Loading & No Results */
  .loading,
  .no-results {
    text-align: center;
    padding: 4rem 2rem;
    color: var(--muted-color);
  }

  .no-results a {
    color: var(--litellm-primary);
    text-decoration: none;
  }

  .no-results a:hover {
    text-decoration: underline;
  }

  /* Responsive */
  @media (max-width: 768px) {
    .hero-title {
      font-size: 2rem;
    }

    .search-bar-container {
      flex-direction: column;
    }

    .filters-row {
      flex-direction: column;
      align-items: flex-start;
    }

    .cards-container {
      padding: 0 1rem;
    }
  }
</style>
