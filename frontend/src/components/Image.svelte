<script>
	import { onMount } from 'svelte'
	export let src;
    export let img_class;
    export let width;
    export let height;

	let loaded = false;
	let failed = false;
	let loading = false;

	$: {
        loaded = false;
        failed = false;
        loading = false;
        loadImage(src);
    }

    const EXPIRATION_DURATION = 10 * 60 * 1000; // minutes * seconds * milliseconds

    async function cacheImage(url) {
        const cache = await caches.open('image-cache');
        const response = await fetch(url, { mode: 'no-cors' });
        // if (!response.ok) {
        //     throw new Error('Network response was not ok');
        // }
        // if (response.status !== 200) {
        //     return
        //     throw new Error('Network response was not ok');
        // }
		await cache.put(url, response.clone());
		
        // Save the current time and expiration duration as metadata.
        const expirationData = JSON.parse(localStorage.getItem('image-cache-expiration-duration')) || {};
        expirationData[url] = Date.now() + EXPIRATION_DURATION;
        localStorage.setItem('image-cache-expiration-duration', JSON.stringify(expirationData));
    }

    async function getCachedImage(url) {
        const cache = await caches.open('image-cache');
        const response = await cache.match(url);
        if (response) {
            // Check the metadata to see if the image is still valid.
            const expirationData = JSON.parse(localStorage.getItem('image-cache-expiration-duration')) || {};
            if (expirationData[url] && Date.now() < expirationData[url]) {
                return response.url;
            }

            // If the image is not valid, remove it from the cache.
            await cache.delete(url);
        }
        throw new Error('Image is not in cache or expired');
    }

	async function loadImage(url) {
        try {
			const img = new Image();
            img.src = await getCachedImage(url);
            loaded = true;
        } catch (error) {
            const img = new Image();
            img.src = url;
            loading = true;

            img.onload = async () => {
                loading = false;
                loaded = true;
                try {
                    await cacheImage(url);
                } catch (error) {
                    console.error(`Failed to cache image at ${url}: ${error}`);
                }
            };

            img.onerror = () => {
                loading = false;
                failed = true;
            };
        }
    }

	// // og
	// onMount(() => {
	// 	const img = new Image();
	// 	img.src = src;
	// 	loading = true;

	// 	img.onload = () => {
	// 			loading = false;
	// 			loaded = true;
	// 	};
	// 	img.onerror = () => {
	// 			loading = false;
	// 			failed = true;
	// 	};
	// })
</script>


{#if loaded}
	<img {src} class="{img_class}" width="{width}" height="{height}" alt="..." />
{:else if failed}
	<img src='img/noImage.jpg' class="{img_class}" width="{width}" height="{height}" alt="Not Found" />
{:else if loading}
    <div class="d-flex justify-content-center">
        <div class="spinner-border mt-5 p-4 text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
        </div>
  </div>
{/if}
