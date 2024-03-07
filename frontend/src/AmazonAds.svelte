<script>
    import { writable } from 'svelte/store';
  
    export let userSearch;
    export let userLocation;
    let ads = writable([]);
    let loading = false; // Local loading state
  
    export async function fetchAds() {
      if (!userSearch) return;
      loading = true; // Start loading
      try {
        const response = await fetch(`http://127.0.0.1:8000/amazon/?user_search=${encodeURIComponent(userSearch)}&user_postal_code=${encodeURIComponent(userLocation)}`);
        const data = await response.json();
        ads.set(data.ads);
      } catch (error) {
        console.error('Error fetching Amazon ads:', error);
      } finally {
        loading = false; // Stop loading whether there was an error or not
      }
    }
  </script>

<h3 class="text-lg font-semibold text-center mt-6">Amazon Ads</h3>
{#if $ads.length > 0}
  <div class="ads-container mt-4">
    {#each $ads as ad (ad.link)}
      <div class="ad bg-gray-100 rounded-lg p-4 shadow my-2">
        <div class="ad-image">
          <img src={ad.image_link || 'src/assets/image_not_found.jpg'} alt={ad.title} class="rounded w-32 h-auto">
        </div>
        <div class="ad-info mt-2">
          <p class="ad-title font-bold">{ad.title}</p>
          <p class="ad-price">{ad.price}</p>
          <a href={"https://www.Amazon.ca" + ad.link} target="_blank" class="text-blue-500 hover:underline">View Listing</a>
        </div>
      </div>
    {/each}
  </div>
{:else}
    {#if loading}
        <p class="text-center text-gray-500">Loading...</p>
    {:else}
        <p class="text-center text-gray-500">No results found.</p>
    {/if}
{/if}

<style>
  .ad-image img {
    max-width: 100%;
    height: auto;
    display: block;
    object-fit: cover;
  }
</style>