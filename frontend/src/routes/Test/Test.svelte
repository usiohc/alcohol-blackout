<script>
    import { onMount } from "svelte";
    import { push } from "svelte-spa-router";
	// import { Storage } from '@google-cloud/storage';

	let isOk = false;
	let isSuccess;

	$:isSuccess = isOk ? '' : 'success-modal';
	
	function test() {
		console.log('test')
		isOk = true;
		push('/')
	}

	let imageUrl;

	let data = [
    	{ id: 1, imageUrl: '/acbo-images/Cocktail/Aperol%20Spritz.jpg', image:'' },
    	{ id: 2, imageUrl: '/acbo-images/Cocktail/Aperol%20Spritz.jpg', image:'' },
    	{ id: 3, imageUrl: '/acbo-images/Cocktail/Aperol%20Spritz.jpg', image:'' },
		// Add more images as needed
	];


	async function loadImage(url) {
		const image = new Image();
		image.crossOrigin = "Anonymous";
		await new Promise((resolve, reject) => {
		image.onload = resolve;
		image.onerror = reject;
		image.src = url;
		});
		return image;
  	}

	async function loadImages() {
		for (let i = 0; i < data.length; i++) {
		const imageUrl = data[i].imageUrl;
		const image = await loadImage(imageUrl);
		data[i].image = await getImageAsBase64(image);
		}
  	}

	async function getImageAsBase64(image) {
		const canvas = document.createElement('canvas');
		const ctx = canvas.getContext('2d');
		canvas.width = image.width;
		canvas.height = image.height;
		ctx.drawImage(image, 0, 0);
		return canvas.toDataURL('image/jpeg');
	}

  loadImages(); // 이미지 로딩 함수 호출

	// onMount(() => {
    //     fetch('/acbo-images/Cocktail/Aperol Spritz.jpg', {
	// 		method: 'GET',
	// 		headers: {
	// 			'Content-Type': 'image/jpeg',
	// 		},
	// 	})
    //         .then(response => {
	// 			response.blob();
	// 			console.log(response)
	// 		})
    //         .then(blob => {
	// 			console.log(blob)
    //             imageUrl = window.URL.createObjectURL(blob);
	// 			console.log(imageUrl)
    //         });
    // })

</script>

<!-- <img src={imageUrl} class="img-fluid rounded card-img-top" width="100%" height="100%" alt="..."> -->
<!-- {#each data as { id, imageUrl }}
  {#await loadImage(imageUrl) then image}
    <img src={image.src} alt={`Image ${id}`} class="img-fluid" />
  {/await}
{/each} -->
{#each data as { id, image }}
  <img src={image} alt={`Image ${id}`} class="img-fluid" />
{/each}

<div class="modal fade" id='{isSuccess}' tabindex="-1" aria-hidden="true">
	<div class="modal-dialog">
	  <div class="modal-content">
		<div class="modal-header">
		  <h5 class="modal-title">회원가입 완료</h5>
		  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
		</div>
		<div class="modal-body">
		  <p>메일</p>
		</div>
		<div class="modal-footer">
		  <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
		</div>
	  </div>
	</div>
</div>

<button type="button" class="btn btn-primary" on:click={ test } data-bs-toggle="modal" data-bs-target='#{isSuccess}'>
	회원가입
</button>