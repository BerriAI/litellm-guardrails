<script lang="ts">
  export let categories: string[] = [];
  export let selectedCategory: string = "";

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

  function formatCategory(category: string): string {
    return category
      .split("-")
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");
  }
</script>

<div class="dropdown-wrapper">
  <select
    bind:value={selectedCategory}
    class="category-select"
    aria-label="Filter by category"
  >
    <option value="">All Categories</option>
    {#each categories as category}
      <option value={category}>
        {getCategoryIcon(category)} {formatCategory(category)}
      </option>
    {/each}
  </select>
</div>

<style>
  .dropdown-wrapper {
    position: relative;
    min-width: 180px;
  }

  .category-select {
    width: 100%;
    padding: 0.875rem 1rem;
    font-size: 1rem;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    background-color: var(--bg-color);
    color: var(--text-color);
    cursor: pointer;
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%236b7280' d='M2.5 4.5L6 8L9.5 4.5'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 1rem center;
    padding-right: 2.5rem;
    transition: border-color 0.2s;
  }

  .category-select:hover {
    border-color: var(--muted-color);
  }

  .category-select:focus {
    outline: none;
    border-color: var(--litellm-primary, #6366f1);
  }
</style>
