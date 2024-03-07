<script>
	import { writable } from "svelte/store";
  
	const ads = writable({ kijiji: [], amazon: [], ebay: [] }); // store the ads
	const loading = writable({ kijiji: false, amazon: false, ebay: false }); // store the loading state
  
	let userSearch = "";
	let userLocation = "";
  
	async function fetchAdsForService(serviceName, url) {
	  loading.update(current => ({ ...current, [serviceName]: true }));
	  try {
		const response = await fetch(url);
		const data = await response.json();
		ads.update(currentAds => ({
		  ...currentAds,
		  [serviceName]: data.ads,
		}));
	  } catch (error) {
		console.error(`Error fetching ${serviceName} ads:`, error);
	  }
	  loading.update(current => ({ ...current, [serviceName]: false }));
	}
  
	function fetchAds() {
	  if (!userSearch) return;
	  fetchAdsForService('kijiji', `http://127.0.0.1:8000/kijiji/?user_search=${encodeURIComponent(userSearch)}&user_location=${encodeURIComponent(userLocation)}`);
	  fetchAdsForService('amazon', `http://127.0.0.1:8000/amazon/?user_search=${encodeURIComponent(userSearch)}&user_postal_code=${encodeURIComponent(userLocation)}`);
	  fetchAdsForService('ebay', `http://127.0.0.1:8000/ebay/?user_search=${encodeURIComponent(userSearch)}`);
	}
  </script>
  
  <div class="max-w-md mx-auto mt-10">
	<div class="flex items-center border-b border-teal-500 py-2">
	  <input class="appearance-none bg-transparent border-none w-full text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none" type="text" placeholder="Search..." bind:value={userSearch} />
	  <input class="appearance-none bg-transparent border-none w-full text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none" type="text" placeholder="Location or Postal Code" bind:value={userLocation} />
	  <button class="flex-shrink-0 bg-teal-500 hover:bg-teal-700 border-teal-500 hover:border-teal-700 text-sm border-4 text-white py-1 px-2 rounded" on:click={fetchAds}>
		Search
	  </button>
	</div>
  </div>
  
  {#each Object.keys($ads) as serviceName}
	{#if $loading[serviceName]}
	  <p class="text-center mt-5 text-lg text-blue-500">Loading {serviceName} ads...</p>
	{:else}
	  <div class="mt-5">
		<h2 class="text-xl font-bold text-center text-gray-800 mb-4">{serviceName.toUpperCase()} Ads</h2>
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
		  {#each $ads[serviceName] as ad (ad.title)}
			<div class="border rounded-lg p-4 shadow-lg">
			  <p class="font-semibold text-lg text-blue-700">{ad.title}</p>
			  {#if ad.description}<p class="text-gray-600">{ad.description}</p>{/if}
			  {#if ad.image_link || ad.image_links}<img src="{ad.image_link || ad.image_links[0]}" alt="{ad.title}" class="max-h-32 my-2">{/if}
			  <a href="{ad.link}" target="_blank" class="text-indigo-600 hover:text-indigo-800 visited:text-purple-600">View</a>
			</div>
		  {/each}
		</div>
	  </div>
	{/if}
  {/each}
  
  <style>
	/* may add custom here mayb */
  </style>