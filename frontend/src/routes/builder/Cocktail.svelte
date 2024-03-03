<script>
  import { onMount } from "svelte";
  import { push } from "svelte-spa-router";
  import { selectedItems, searchQuery } from "../../lib/store";
  import { search } from "../../lib/search";
  import fastapi from "../../lib/api"  
  import Error from "../../components/Error.svelte"
  import Image from "../../components/Image.svelte";

  let cocktails = [];
  let filteredCocktails;

  let total = 0;
  let isLoaded = false;
  let error = {detail:[]};
  let imagePath_GCP = "https://storage.googleapis.com/acbo-images/"

    async function get_cocktail_by_spirit_material() {
      let url = '/api/cocktails/'
      let params = { 
        "spirits": $selectedItems['spirits'],
        "materials": $selectedItems['materials']
      }
      fastapi('get', url, params, 
          (json) => { 
              total = json.total
              cocktails = json.items
              cocktails.forEach(cocktail => {
                cocktail.imagePath = imagePath_GCP + "Cocktail/" + cocktail.name + ".jpg";
              });
              filteredCocktails = cocktails;
          }, 
          (json_error) => { 
              error = json_error
          }
      )
    isLoaded = true;
  }


  function toggleCard(name) {
    push('/cocktail/' + name)
  }

  onMount(() => {
    get_cocktail_by_spirit_material();
  })
    
  
  $: {
    filteredCocktails = search($searchQuery, cocktails);
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
    <p>검색된 칵테일 수 : { filteredCocktails.length }</p>
  </div>
  <Error error={error} margin="mt-3"/>
  <div class="row row-cols-2 row row-cols-xs-2 row-cols-sm-3 row-cols-md-3 row-cols-lg-4 g-3">
    {#each filteredCocktails as { name, name_ko, usage_count, imagePath }}
      <div class="col">
        <button on:click="{ toggleCard(name) }" style="background: none; border: none; padding: 0; cursor: pointer;">
          <div class="card shadow-sm">
            <div class="" style="min-width: 162.35px; min-height: 162.35px;">
              <Image src={imagePath} img_class="img-fluid rounded card-img-top" width="100%" height="100%"/>
            </div>
            <div class="card-body"  style="text-align: center;">
              <p class="card-text">{name_ko}<br>
              <small class="text-body-secondary">{name}</small></p>
            </div>
          </div>
        </button>
      </div>
    {/each}
  </div>
</div>
{/if}