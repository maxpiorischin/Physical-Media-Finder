<script>
  import KijijiAds from './KijijiAds.svelte';
  import EbayAds from './EbayAds.svelte';
  import AmazonAds from './AmazonAds.svelte';

  let userSearch = '';
  let userLocation = '';
  let kijiji;
  let ebay;
  let amazon;
</script>

<div class="flex flex-col items-center justify-center p-4">
  <input
    type="text"
    placeholder="Search..."
    bind:value={userSearch}
    class="input input-bordered input-primary w-full max-w-xs"
  />
  <input
    type="text"
    placeholder="Location (Postal Code for Amazon)"
    bind:value={userLocation}
    class="input input-bordered input-primary w-full max-w-xs mt-2"
  />
  <button class="btn btn-primary mt-2" on:click={() => {
    kijiji.fetchAds();
    ebay.fetchAds();
    amazon.fetchAds();
  }}>Search</button>
</div>
<AmazonAds bind:this={amazon} {userSearch} {userLocation}/>
<EbayAds bind:this={ebay} {userSearch} />
<KijijiAds bind:this={kijiji} {userSearch} {userLocation} />
