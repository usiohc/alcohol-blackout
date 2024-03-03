<script>
  import { onMount } from "svelte";
  import { selectedItems, searchQuery } from "../../lib/store";
  import { search } from "../../lib/search";
	import fastapi from "../../lib/api";
  import Error from "../../components/Error.svelte";
  import Image from "../../components/Image.svelte";

  let materials = [];
  $: materials;
  let filteredMaterials;
  
  let total = 0;
  let isLoaded = false;
  let error = {detail:[]};
  let material_type = {
    "Liqueur": "리큐어",
    "Juice": "주스",
    "Syrup": "시럽",
    "Soda": "소다",
    "Garnish": "가니쉬",
    "Etc": "기타"
  }
  let imagePath_GCP = "https://storage.googleapis.com/acbo-images/"

	async function get_material_by_spirit() {
		let url = '/api/materials/'
    let params = { 
      "spirits": $selectedItems['spirits']
    }

    fastapi('get', url, params, 
				(json) => { 
					total = json.total
					materials = json.items
          materials.forEach(material => {
            material.imagePath = imagePath_GCP + "Material/" + material.type + "/" + material.name + ".jpg";
            material.selected = $selectedItems['materials'].includes(material.type+":"+material.name);
          }); 
          filteredMaterials = materials
          sortCard();

				}, 
				(json_error) => { 
          error = json_error
				}
		)
    
    isLoaded = true;
  }

    async function sortCard() {
      // 선택된 카드를 먼저 보여주도록 materials 배열을 정렬
      materials.sort((a, b) => b.selected - a.selected);
    }

    function toggleCard(type, name) {
        const cardIndex = materials.findIndex(card => card.type === type && card.name === name);
        materials[cardIndex].selected = !materials[cardIndex].selected;
        
        $selectedItems['materials'] = materials.filter(card => card.selected).map(card => { return card.type+":"+card.name});
    }
  
  onMount(() => {
    get_material_by_spirit();
  })
  
  $: {
    filteredMaterials = search($searchQuery, materials);
  }


</script>

{#if !isLoaded}
  <div class="d-flex justify-content-center">
    <div class="spinner-border mt-5 p-4 text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>

{:else}
<div class="px-3">
  <div class="text-center mt-3">
    <p>검색된 재료 수 : { filteredMaterials.length }</p>
  </div>
  <Error error={error} margin="mt-3"/>
  <div class="row row-cols-2 row row-cols-xs-2 row-cols-sm-3 row-cols-md-3 row-cols-lg-4 g-3">
    {#each filteredMaterials as { type, name, name_ko, imagePath, selected }}
      <div class="col">
        <button on:click={() => toggleCard(type, name)} style="background: none; border: none; padding: 0; cursor: pointer;">
          <div class="card shadow-sm" style="{selected ? 'background-color: #ddd;' : ''}">
            <div class="" style="min-width: 162.35px; min-height: 162.35px;">
              <Image src={imagePath} img_class="img-fluid rounded card-img-top" width="100%" height="100%"/>
            </div>
            <div class="card-body"  style="text-align: center;">
              <p class="card-text">{name_ko}<br>
              <small class="text-body-secondary">{material_type[type]}</small></p>
            </div>
          </div>
        </button>
      </div>
    {/each}
  </div>
</div>
{/if}